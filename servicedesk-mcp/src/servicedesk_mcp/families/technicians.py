from servicedesk_mcp.core.client import ServiceDeskClient

FAMILY_NAME = "technicians"

async def list_technicians():
    client = ServiceDeskClient()
    response = await client.get("/technicians")
    return response.json()

async def get_technician(technician_id: str):
    client = ServiceDeskClient()
    response = await client.get(f"/technicians/{technician_id}")
    return response.json()

def register_tools():
    return [
        "list_technicians",
        "get_technician",
    ]
