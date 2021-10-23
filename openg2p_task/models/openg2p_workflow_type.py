from odoo import models, fields, api


class Openg2pWorkflowType(models.Model):
    _name = "openg2p.workflow.type"
    _description = "Workflow type for OpenG2P Tasks"

    name = fields.Char(string="Workflow name")

    # list of stages to be followed
    stages = fields.Many2many(
        comodel_name="openg2p.workflow.stage",
        relation="openg2p_workflow_type_stage",
        column1="workflow_type_id",
        column2="workflow_stage_id",
        string="Workflow stages",
    )

    stage_count = fields.Integer(
        string="Number of stages",
        readonly=True,
        store=False,
        compute="_compute_stage_count",
    )

    def name_get(self):
        for rec in self:
            yield rec.id, f"{rec.name} (WT{rec.id})"

    @api.depends("stages")
    def _compute_stage_count(self):
        for rec in self:
            rec.stage_count = len(rec.stages)

    def api_json(self):
        return {
            "name": self.name,
            "stages": self.stages.ids,
            "number_of_stages": self.stage_count,
        }
