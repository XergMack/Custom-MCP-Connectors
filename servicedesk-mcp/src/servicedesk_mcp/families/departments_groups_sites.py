from servicedesk_mcp.core.client import ServiceDeskClient

FAMILY_NAME = "departments_groups_sites"

async def list_departments(params: dict | None = None):
    client = ServiceDeskClient()
    response = await client.get("/departments", params=params or {})
    return response.json()

async def list_groups(params: dict | None = None):
    client = ServiceDeskClient()
    response = await client.get("/groups", params=params or {})
    return response.json()

async def list_sites(params: dict | None = None):
    client = ServiceDeskClient()
    response = await client.get("/sites", params=params or {})
    return response.json()

async def get_site(site_id: str):
    client = ServiceDeskClient()
    response = await client.get(f"/sites/{site_id}")
    return response.json()

def register_tools():
    return [
        "list_departments",
        "list_groups",
        "list_sites",
        "get_site",
    ]
