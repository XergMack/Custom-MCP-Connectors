FAMILY_NAME = "technicians"

async def _not_implemented(tool_name: str, arguments: dict | None = None):
    return {
        "ok": False,
        "error": "Not implemented yet",
        "family": FAMILY_NAME,
        "tool_name": tool_name,
        "arguments": arguments or {}
    }

async def list_technicians(**kwargs):
    return await _not_implemented("list_technicians", kwargs)
async def get_technician(**kwargs):
    return await _not_implemented("get_technician", kwargs)

def register_tools():
    return [
        "list_technicians",
        "get_technician",
    ]
