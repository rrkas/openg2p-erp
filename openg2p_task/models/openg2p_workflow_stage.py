from odoo import models, fields, api


class Openg2pWorkflowStage(models.Model):
    _name = "openg2p.workflow.stage"
    _description = "Workflow stage for OpenG2P Tasks"

    task_subtype_id = fields.Many2one(
        "openg2p.task.subtype",
        string="Task Subtype",
    )

    intermediate = fields.Boolean(string="Stage is intermediate")

    def name_get(self):
        for rec in self:
            yield rec.id, f"{rec.task_subtype_id.name}{' (intermediate)' if rec.intermediate else ''}"

    def api_json(self):
        return {
            "task_subtype_id": self.task_subtype_id.id,
            "intermediate": self.intermediate,
        }
