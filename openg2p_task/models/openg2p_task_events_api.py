from odoo.http import Controller, route, request


class Openg2pTaskEventsApi(Controller):
    @route("/workflows", type="json", auth="user", methods=["GET"])
    def get_workflows(self):
        workflows_list = request.env["openg2p.workflow"].search([])

        try:
            workflows = []
            for wf in workflows_list:
                workflows.append(wf.api_json())

            return {"status": 200, "message": "Success", "workflows": workflows}

        except BaseException as e:
            return {"status": 400, "error": str(e)}

    @route("/workflow/<int:id>", type="json", auth="user", methods=["GET"])
    def get_workflow_by_id(self, id):
        workflows_list = request.env["openg2p.workflow"].search([("id", "=", id)])

        try:
            workflows = []
            for wf in workflows_list:
                workflows.append(wf.api_json())

            return {"status": 200, "message": "Success", "workflows": workflows}

        except BaseException as e:
            return {"status": 400, "error": str(e)}
