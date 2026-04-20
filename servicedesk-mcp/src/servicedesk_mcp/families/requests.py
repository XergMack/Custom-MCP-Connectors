from servicedesk_mcp.core.client import ServiceDeskClient

FAMILY_NAME = "requests"

async def list_requests(params: dict | None = None):
    client = ServiceDeskClient()
    response = await client.get("/requests", params=params or {})
    return response.json()

async def get_request(request_id: str):
    client = ServiceDeskClient()
    response = await client.get(f"/requests/{request_id}")
    return response.json()

async def create_request(payload: dict):
    client = ServiceDeskClient()
    response = await client.post("/requests", json_body=payload)
    return response.json()

async def update_request(request_id: str, payload: dict):
    client = ServiceDeskClient()
    response = await client.put(f"/requests/{request_id}", json_body=payload)
    return response.json()

async def search_requests(
    technician_name: str | None = None,
    status_name: str | None = None,
    subject_contains: str | None = None,
    created_after: str | None = None,
    created_before: str | None = None,
    start_index: int = 1,
    row_count: int = 100,
):
    params = {
        "start_index": start_index,
        "row_count": row_count,
    }

    if technician_name:
        params["technician_name"] = technician_name
    if status_name:
        params["status_name"] = status_name
    if subject_contains:
        params["subject_contains"] = subject_contains
    if created_after:
        params["created_after"] = created_after
    if created_before:
        params["created_before"] = created_before

    return await list_requests(params)

def register_tools():
    return [
        "list_requests",
        "get_request",
        "create_request",
        "update_request",
        "search_requests",
    ]
