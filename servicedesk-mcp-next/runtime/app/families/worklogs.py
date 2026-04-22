from app.core.client import ServiceDeskClient

FAMILY_NAME = "worklogs"

async def list_request_worklogs(request_id: str):
    client = ServiceDeskClient()
    return await client.get(f"/requests/{request_id}/worklogs")

async def add_request_worklog(request_id: str, payload: dict):
    client = ServiceDeskClient()
    return await client.post(f"/requests/{request_id}/worklogs", json_body=payload)

def register_tools():
    return [
        "list_request_worklogs",
        "add_request_worklog",
    ]
