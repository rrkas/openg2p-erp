from odoo import models, fields, api


class Openg2pWorkflow(models.Model):
    _name = "openg2p.workflow"
    _description = "Workflows for OpenG2P Tasks"

    # name = fields.Char(string="Workflow Name")

    workflow_type = fields.Many2one("openg2p.workflow.type", string="Workflow type")

    curr_workflow_stage = fields.Many2one(
        "openg2p.workflow.stage", string="Current workflow stage"
    )

    workflow_completed = fields.Boolean(
        string="Workflow completed",
    )

    workflow_context = fields.Text(
        string="Context",
    )

    def _update_context(self, event_code, obj, status):
        pass

    @api.model
    def create(self, vals_list):
        res = super().create(vals_list)
        # subtype_obj = self.env["openg2p.task.subtype"].search(
        #     [("id", "=", self.curr_workflow_stage.curr_task_subtype.id)]
        # )[0]
        self.env["openg2p.task"].create(
            {
                "type_id": 2,
                "subtype_id": 5,
                "entity_type_id": "odk.config",
                "entity_id": 0,
                "status_id": 2,
                "workflow_id": res.id,
                "target_url": "http://localhost:8069/web#action=288&model=odk.config&view_type=list&menu_id=207",
            }
        )
        return res

    def name_get(self):
        for rec in self:
            yield rec.id, f"{rec.workflow_type.name} ({rec.id})"

    # odk -> conv_ben -> ben_enroll -> batch
    def handle_tasks(self, event_code, obj):
        task = self.env["openg2p.task"].search([("status_id", "=", 2)])
        # create config
        if event_code == 1:
            task.write(
                {
                    "entity_id": obj.id,
                    "status_id": 3,
                    "target_url": f"http://localhost:8069/web#"
                    f"id={task.entity_id}&"
                    f"action=288&"
                    f"model=odk.config&"
                    f"view_type=list&menu_id=207",
                }
            )
            self.env["openg2p.task"].create(
                {
                    "type_id": 2,
                    "subtype_id": 7,
                    "entity_type_id": "odk.config",
                    "entity_id": 0,
                    "status_id": 2,
                    "workflow_id": task.workflow_id,
                    "target_url": "http://localhost:8069/web#action=288&model=odk.config&view_type=list&menu_id=207",
                }
            )
        # pull odk
        elif event_code == 2:
            task.write(
                {
                    "entity_id": obj.id,
                    "status_id": 3,
                    "target_url": "http://localhost:8069/web#action=288&model=odk.config&view_type=list&menu_id=207",
                }
            )
            self.env["openg2p.task"].create(
                {
                    "type_id": 3,
                    "subtype_id": 11,
                    "entity_type_id": "openg2p.registration",
                    "entity_id": 0,
                    "status_id": 2,
                    "workflow_id": task.workflow_id,
                    "target_url": "http://localhost:8069/web#action=184&model=openg2p.registration&view_type=kanban&menu_id=127",
                }
            )
        # regd -> beneficiary
        elif event_code == 3:
            task.write(
                {
                    "entity_id": obj.id,
                    "status_id": 3,
                    "target_url": "http://localhost:8069/web#action=184&model=openg2p.registration&view_type=kanban&menu_id=127",
                }
            )
            self.env["openg2p.task"].create(
                {
                    "type_id": 4,
                    "subtype_id": 14,
                    "entity_type_id": "openg2p.beneficiary",
                    "entity_id": 0,
                    "status_id": 2,
                    "workflow_id": task.workflow_id,
                    "target_url": "http://localhost:8069/web#action=155&model=openg2p.beneficiary&view_type=kanban&menu_id=111",
                }
            )
        # enroll beneficiaries
        elif event_code == 4:
            task.write(
                {
                    "entity_id": obj.id,
                    "status_id": 3,
                    "target_url": "http://localhost:8069/web#action=155&model=openg2p.beneficiary&view_type=kanban&menu_id=111",
                }
            )
            self.env["openg2p.task"].create(
                {
                    "type_id": 4,
                    "subtype_id": 15,
                    "entity_type_id": "openg2p.beneficiary",
                    "entity_id": 0,
                    "status_id": 2,
                    "workflow_id": task.workflow_id,
                    "target_url": "http://localhost:8069/web#action=155&model=openg2p.beneficiary&view_type=kanban&menu_id=111",
                }
            )
        # workflow = self.env["openg2p.workflow"].search(
        #     [("id", "=", task.workflow_id)]
        # )
        # workflow.write(
        #     {
        #         "curr_workflow_stage": workflow.curr_workflow_stage.id + 1,
        #     }
        # )

    def api_json(self):
        return {
            "workflow-type": self.workflow_type.id,
            "current-workflow-stage": self.curr_workflow_stage.id,
            "workflow-completed": self.workflow_completed,
        }
