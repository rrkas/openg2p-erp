from odoo import models, fields, api


class Openg2pTaskSubtype(models.Model):
    _name = "openg2p.task.subtype"
    _description = "Task subtask mapping for OpenG2P"

    task_type_id = fields.Many2one(
        comodel_name="openg2p.task.type",
        string="Task Type",
    )
    name = fields.Char(string="Task Subtype")
    role_id = fields.Many2one(
        comodel_name="openg2p.task.role",
        string="Task Role",
    )

    @api.onchange("task_type_id")
    def onchange_task_type(self):
        for rec in self:
            return {"domain": {"role_id": [("task_type_id", "=", rec.task_type_id.id)]}}

    def name_get(self):
        for rec in self:
            yield rec.id, rec.name

    def api_json(self):
        return {
            "task_type": self.task_type_id,
            "task_subtype": self.name,
            "task_role": self.role_id
        }
