from servicedesk_mcp.core.client import ServiceDeskClient

FAMILY_NAME = "admin"

async def list_priorities(params: dict | None = None):
    client = ServiceDeskClient()
    response = await client.get("/priorities", params=params or {})
    return response.json()

async def list_statuses(params: dict | None = None):
    client = ServiceDeskClient()
    response = await client.get("/statuses", params=params or {})
    return response.json()

async def list_templates(params: dict | None = None):
    client = ServiceDeskClient()
    response = await client.get("/request_templates", params=params or {})
    return response.json()

def register_tools():
    return [
        "list_priorities",
        "list_statuses",
        "list_templates",
    ]
