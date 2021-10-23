import json

from odoo import models, fields, api


class Openg2pWorkflow(models.Model):
    _name = "openg2p.workflow"
    _description = "Workflows for OpenG2P Tasks"

    workflow_type = fields.Many2one(
        "openg2p.workflow.type",
        string="Workflow type",
    )

    curr_workflow_stage = fields.Many2one(
        comodel_name="openg2p.workflow.stage",
        string="Current workflow stage",
        readonly=True,
        store=True,
    )

    workflow_completed = fields.Boolean(
        string="Is workflow completed",
        readonly=True,
        store=True,
    )

    workflow_stage_count = fields.Integer(
        string="Workflow Stage Count",
        store=False,
        compute='_compute_fields',
    )
    curr_workflow_stage_index = fields.Integer(
        string="Current Workflow Stage Index",
        store=False,
        compute='_compute_fields',
    )
    # for storing technical details, JSONified dict for different stage details
    context = fields.Text(
        string="Context Details",
        readonly=True,
        store=True,
    )

    @api.onchange('workflow_type')
    def onchange_workflow_type(self):
        stages = self.env['openg2p.workflow.stage'].search([('id', 'in', self.workflow_type.stages.ids)])
        if stages and len(stages) > 0:
            self.workflow_stage_count = len(stages)
            self.curr_workflow_stage = stages[0]
            self.curr_workflow_stage_index = 1
        return {
            'domain': {
                'curr_workflow_stage': [('id', 'in', self.workflow_type.stages.ids)],
            }
        }

    def _compute_fields(self):
        for rec in self:
            rec.workflow_stage_count = len(rec.workflow_type.stages.ids)
            if rec.curr_workflow_stage.id:
                rec.curr_workflow_stage_index = rec.workflow_type.stages.ids.index(rec.curr_workflow_stage.id) + 1
            if not rec.context:
                rec.context = json.dumps({}, indent=2)

    def get_id_from_ext_id(self, ext_id):
        return self.env.ref(f'openg2p_task.{ext_id}').id

    def get_ext_id_from_id(self, model, id):
        res = self.env['ir.model.data'].search(['&', ('model', '=', model), ('res_id', '=', id)])
        print(res)
        if res and len(res) > 0:
            return res[0].name
        return None

    def _update_context(self, event_code, obj):
        context = json.loads(self.context)
        if isinstance(obj, list):
            ids = list(map(lambda x: x.id, obj))
        else:
            try:
                ids = obj.ids
            except:
                ids = obj.id
        context[event_code] = ids
        self.context = json.dumps(context, indent=2)

    def _update_task_list(self, task_id):
        context = json.loads(self.context)
        context['tasks'].append(task_id)
        self.context = json.dumps(context)

    def handle_intermediate_task(self):
        task_code = self.get_ext_id_from_id('openg2p.task.subtype', self.curr_workflow_stage.id)
        if task_code == 'task_subtype_regd_make_beneficiary':
            # self.env['']
            pass

    def name_get(self):
        for rec in self:
            yield rec.id, f"{rec.workflow_type.name} ({rec.id})"

    def handle_tasks(self, event_code, obj):
        subtype_id = self.get_id_from_ext_id(event_code)
        task = self.env['openg2p.task'].search(['&', ('subtype_id', '=', subtype_id), ('status_id', '=', 2)])
        if task and len(task) > 0:
            task = task[0]
            workflow = self.env['openg2p.workflow'].search([('id', '=', task.workflow_id)])
            if workflow and len(workflow) > 0:
                workflow = workflow[0]
                assert isinstance(workflow, self.__class__)
                workflow._update_context(event_code, obj)
            task.status_id = 3
            try:
                workflow.curr_workflow_stage = workflow.workflow_type.states[
                    workflow.curr_workflow_stage_index].task_subtype_id.id
                while workflow.curr_workflow_stage.intermediate:
                    workflow.handle_intermediate_task()
                next_task = self.env['openg2p.task'].create({
                    "subtype_id": workflow.curr_workflow_stage.task_subtype_id.id,
                    "workflow_id": workflow.id,
                    "status_id": 2,
                })
                workflow._update_task_list(next_task.id)
            except:
                pass

    @api.model
    def create(self, vals_list):
        res = super().create(vals_list)
        task = self.env['openg2p.task'].create({
            "subtype_id": res.curr_workflow_stage.task_subtype_id.id,
            "workflow_id": res.id,
            "status_id": 2,
        })
        res.context = json.dumps({
            self.get_ext_id_from_id('openg2p.task.subtype', res.workflow_type.stages[0].task_subtype_id.id): None,
            "tasks": [task.id],
        }, indent=2)
        return res

    def write(self, vals):
        if not self.context and vals.get('context') is None:
            vals['context'] = json.dumps({}, indent=2)
        return super().write(vals)
