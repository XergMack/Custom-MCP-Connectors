from servicedesk_mcp.core.client import ServiceDeskClient

FAMILY_NAME = "purchase"

async def list_purchase_orders(params: dict | None = None):
    client = ServiceDeskClient()
    response = await client.get("/purchase_orders", params=params or {})
    return response.json()

async def get_purchase_order(purchase_order_id: str):
    client = ServiceDeskClient()
    response = await client.get(f"/purchase_orders/{purchase_order_id}")
    return response.json()

def register_tools():
    return [
        "list_purchase_orders",
        "get_purchase_order",
    ]
