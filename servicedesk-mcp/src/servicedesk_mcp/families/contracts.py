from servicedesk_mcp.core.client import ServiceDeskClient

FAMILY_NAME = "contracts"

async def list_contracts(params: dict | None = None):
    client = ServiceDeskClient()
    response = await client.get("/contracts", params=params or {})
    return response.json()

async def get_contract(contract_id: str):
    client = ServiceDeskClient()
    response = await client.get(f"/contracts/{contract_id}")
    return response.json()

def register_tools():
    return [
        "list_contracts",
        "get_contract",
    ]
