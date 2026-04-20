FAMILY_NAME = "purchase"

async def _not_implemented(tool_name: str, arguments: dict | None = None):
    return {
        "ok": False,
        "error": "Not implemented yet",
        "family": FAMILY_NAME,
        "tool_name": tool_name,
        "arguments": arguments or {}
    }

async def list_purchase_orders(**kwargs):
    return await _not_implemented("list_purchase_orders", kwargs)
async def get_purchase_order(**kwargs):
    return await _not_implemented("get_purchase_order", kwargs)

def register_tools():
    return [
        "list_purchase_orders",
        "get_purchase_order",
    ]
