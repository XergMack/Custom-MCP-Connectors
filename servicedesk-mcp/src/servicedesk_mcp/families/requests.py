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

def register_tools():
    return [
        "list_requests",
        "get_request",
        "create_request",
        "update_request",
    ]
