from app.core.client import ServiceDeskClient

FAMILY_NAME = "requests"

async def list_requests(params: dict | None = None):
    client = ServiceDeskClient()
    return await client.get("/requests", params=params or {})

async def get_request(request_id: str):
    client = ServiceDeskClient()
    return await client.get(f"/requests/{request_id}")

async def create_request(payload: dict):
    client = ServiceDeskClient()
    return await client.post("/requests", json_body=payload)

async def update_request(request_id: str, payload: dict):
    client = ServiceDeskClient()
    return await client.put(f"/requests/{request_id}", json_body=payload)

def register_tools():
    return [
        "list_requests",
        "get_request",
        "create_request",
        "update_request",
    ]
