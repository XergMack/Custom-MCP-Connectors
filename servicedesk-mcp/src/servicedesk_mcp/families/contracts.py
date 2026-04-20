FAMILY_NAME = "contracts"

async def _not_implemented(tool_name: str, arguments: dict | None = None):
    return {
        "ok": False,
        "error": "Not implemented yet",
        "family": FAMILY_NAME,
        "tool_name": tool_name,
        "arguments": arguments or {}
    }

async def list_contracts(**kwargs):
    return await _not_implemented("list_contracts", kwargs)
async def get_contract(**kwargs):
    return await _not_implemented("get_contract", kwargs)

def register_tools():
    return [
        "list_contracts",
        "get_contract",
    ]
