from odoo import models, fields


class Openg2pWorkflowStage(models.Model):
    _name = "openg2p.workflow.stage"
    _description = "Workflow stage for OpenG2P Workflows"

    curr_task_subtype = fields.Many2one(
        "openg2p.task.subtype", string="Current Task Subtype"
    )

    # next subtype if current stage is completed
    success_task_subtype = fields.Many2one(
        "openg2p.task.subtype", string="Success Task Subtype"
    )

    # next subtype if current stage is failed
    failure_task_subtype = fields.Many2one(
        "openg2p.task.subtype", string="Failure Task Subtype"
    )

    workflow_type_id = fields.Many2one("openg2p.workflow.type")

    def name_get(self):
        for rec in self:
            yield rec.id, f"{rec.workflow_type_id.name} / {rec.curr_task_subtype.id}"
