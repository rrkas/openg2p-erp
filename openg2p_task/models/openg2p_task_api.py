from odoo import fields
from odoo.http import Controller, route, request


# getTaskById
# getSubTaskForTaskId
# getTaskByProcess
# getTasksforUser
# getTasksforRole
# createTask with stateTransition commands - reassign, changeRole, suspend, close, unassign, approve, reject, changeProgram,bulkReassign, bulkunassign

class Openg2pTaskApi(Controller):

    @route("/tasks", type="json", auth="user", methods=["GET"])
    def all_tasks(self):
        try:
            task = request.env["openg2p.task"].search([])

            tasks_all = []
            for t in task:
                tasks_all.append(t.api_json())

            if len(task) > 0:
                return {
                    "status": 200,
                    "message": "Success",
                    "id": id,
                    "task_details": tasks_all
                }
            else:
                return {
                    "status": 404,
                    "id": id,
                    "error": "No tasks exists",
                }
        except BaseException as e:
            return {
                "status": 400,
                "error": str(e)
            }

    @route("/task/<int:id>", type="json", auth="user", methods=["GET"])
    def get_task_by_id(self, id):
        try:
            task = request.env["openg2p.task"].search([("id", "=", id)])

            if len(task) > 0:
                task = task[0]
                return {
                    "status": 200,
                    "message": "Success",
                    "id": id,
                    "task_details": task.api_json()
                }
            else:
                return {
                    "status": 404,
                    "id": id,
                    "error": f"Error ! No task by the id {id} exists",
                }
        except BaseException as e:
            return {
                "status": 400,
                "id": id,
                "error": str(e)
            }

    @route("/sub-task/<int:id>", type="json", auth="user", methods=["GET"])
    def get_sub_task_for_task_id(self, id):
        try:
            task = request.env["openg2p.task"].search([("id", "=", id)])

            if len(task.subtype_id) > 0:
                sub_tasks_details = []
                for st in task.subtype_id:
                    sub_task = request.env["openg2p.task.subtype"].search([("id", "=", st)])
                    sub_tasks_details.append(sub_task.api_json())

                return {
                    "status": 200,
                    "message": "Success",
                    "task_id": id,
                    "sub_task": sub_tasks_details
                }
            else:
                return {
                    "status": 404,
                    "id": id,
                    "error": f"Error ! No sub-task for task by the id {id} exists",
                }
        except BaseException as e:
            return {
                "status": 400,
                "id": id,
                "error": str(e)
            }

    @route("/process/<int:id>", type="json", auth="user", methods=["GET"])
    def get_task_by_process(self):
        task = request.env["openg2p.task"].search([("workflow_pid", "=", id)])

        try:
            if len(task) > 0:
                task = task[0]
                return {
                    "status": 200,
                    "message": "Success",
                    "workflow process": id,
                    "task details": task.api_json()
                }
            else:
                return {
                    "status": 404,
                    "workflow process": id,
                    "error": f"Error ! No task by the workflow process {id} exists",
                }
        except BaseException as e:
            return {
                "status": 400,
                "id": id,
                "error": str(e)
            }

    @route("/tasks/user/<int:id>", type="json", auth="user", methods=["GET"])
    def get_tasks_for_user(self, id):
        user_ids = request.env["res.users"].search([("id", "=", id)])

        tasks = []
        try:
            if user_ids:
                for ids in user_ids:
                    task_details = request.env["openg2p.task"].search([("assignee_id", "=", ids)])
                    tasks.append(
                        task_details.api_json()
                    )
                return {
                    "status": 200,
                    "message": "Success",
                    "user-id": id,
                    "task_details": tasks
                }
            else:
                return {
                    "status": 404,
                    "user-id": id,
                    "error": f"Error ! No tasks for the user {id} exists",
                }
        except BaseException as e:
            return {
                "status": 400,
                "user-id": id,
                "error": str(e)
            }

    @route("/tasks/role/<int:id>", type="json", auth="user", methods=["GET"])
    def get_tasks_for_role(self, id):
        tasks = request.env["openg2p.task"].search([])
        role = request.env["openg2p.task.role"].search([("id", "=", id)])
        tasks_details = []

        try:
            if role:
                for task in tasks:
                    if task.type_id.id == role.task_type_id.id:
                        tasks_details.append(task.api_json())

                return {
                    "status": 200,
                    "message": "Success",
                    "role-id": id,
                    "task_details": tasks_details
                }
            else:
                return {
                    "status": 404,
                    "role-id": id,
                    "error": f"Error ! No tasks for the role-id {id} exists",
                }
        except BaseException as e:
            return {
                "status": 400,
                "role-id": id,
                "error": str(e)
            }
