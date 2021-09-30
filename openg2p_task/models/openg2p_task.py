from odoo import models, fields, api


class Openg2pTask(models.Model):
    _name = "openg2p.task"
    _description = "Task Management for OpenG2P"
    _order = "id desc"

    type_id = fields.Many2one(
        "openg2p.task.type",
        store=False,
        compute="_compute_task_type",
        readonly=True,
        string="Task Type",
    )

    subtype_id = fields.Many2one("openg2p.task.subtype", string="Task Subtype")

    # for building url
    entity_type_id = fields.Char(
        string="Entity Type",
    )

    # for building url
    entity_id = fields.Integer(
        string="Entity ID",
    )

    eta = fields.Datetime(
        string="ETA",
    )

    context = fields.Text(
        string="Context",
    )

    assignee_id = fields.Many2one(
        "res.users",
        string="Assignee",
        default=lambda self: self.env.uid,
    )

    workflow_pid = fields.Integer(string="Workflow Process")

    description = fields.Text(string="Description")

    target_url = fields.Char(string="Target URL")

    status_id = fields.Many2one(
        "openg2p.task.status",
        string="Task Status",
        group_expand="_read_group_status_ids",
    )

    createdby_id = fields.Many2one(
        "res.users",
        string="Created by",
        default=lambda self: self.env.uid,
    )

    lastmodifiedby_id = fields.Many2one(
        "res.users",
        string="Last modified by",
        default=lambda self: self.env.uid,
    )

    @api.depends("subtype_id")
    def _compute_task_type(self):
        for rec in self:
            rec.type_id = rec.subtype_id.task_type_id.id

    @api.multi
    def _create_history(self):
        self.env["openg2p.task.history"].create(
            {
                "task_id": self.id,
                "task_type_id": self.type_id.id,
                "task_subtype_id": self.subtype_id.id,
                "task_status_id": self.status_id.id,
                "task_entity_type_id": self.entity_type_id,
                "task_entity_id": self.entity_id,
                "task_assignee_id": self.assignee_id.id,
                "task_modifiedby_id": self.lastmodifiedby_id.id,
            }
        )

    @api.model
    def create(self, vals):
        res = super(Openg2pTask, self).create(vals)
        assert isinstance(res, Openg2pTask)
        res._create_history()
        return res

    @api.multi
    @api.model
    def write(self, vals):
        res = super(Openg2pTask, self).write(vals)
        if res:
            self._create_history()
        return res

    def name_get(self):
        for rec in self:
            yield rec.id, f"{rec.type_id.name}/{rec.subtype_id.name} ({rec.id})"

    # created_date of this entity = create_date
    # lastmodifiedby_date of this entity = write_date

    def create_task_from_notification(self, event_code, entity_id):
        model_ext_id = "openg2p_task"
        from .task_mapping import event_map

        curr_event = event_map.get(event_code)
        curr_type_id = self.env.ref(f"{model_ext_id}.{curr_event.type_ref}").id
        curr_subtype_id = self.env.ref(f"{model_ext_id}.{curr_event.subtype_ref}").id
        curr_status_id = self.env.ref(
            f"{model_ext_id}.{curr_event.default_status_ref}"
        ).id
        self.create(
            {
                "type_id": curr_type_id,
                "subtype_id": curr_subtype_id,
                "entity_type_id": curr_event.entity_type,
                "entity_id": entity_id,
                "status_id": curr_status_id,
                "target_url": f"http://localhost:8069/web?debug=true#id={entity_id}&model={curr_event.entity_type}",
            }
        )

    @api.model
    def _read_group_status_ids(self, status, domain, order):
        return self.env["openg2p.task.status"].search([])
