from servicedesk_mcp.core.client import ServiceDeskClient

FAMILY_NAME = "tasks"

async def list_request_tasks(request_id: str):
    client = ServiceDeskClient()
    response = await client.get(f"/requests/{request_id}/tasks")
    return response.json()

async def add_request_task(request_id: str, payload: dict):
    client = ServiceDeskClient()
    response = await client.post(f"/requests/{request_id}/tasks", json_body=payload)
    return response.json()

async def update_request_task(request_id: str, task_id: str, payload: dict):
    client = ServiceDeskClient()
    response = await client.put(f"/requests/{request_id}/tasks/{task_id}", json_body=payload)
    return response.json()

def register_tools():
    return [
        "list_request_tasks",
        "add_request_task",
        "update_request_task",
    ]
