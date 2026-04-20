from servicedesk_mcp.core.client import ServiceDeskClient

FAMILY_NAME = "worklogs"

async def list_request_worklogs(request_id: str):
    client = ServiceDeskClient()
    response = await client.get(f"/requests/{request_id}/worklogs")
    return response.json()

async def add_request_worklog(request_id: str, payload: dict):
    client = ServiceDeskClient()
    response = await client.post(f"/requests/{request_id}/worklogs", json_body=payload)
    return response.json()

def register_tools():
    return [
        "list_request_worklogs",
        "add_request_worklog",
    ]
