FAMILY_NAME = "changes"

async def _not_implemented(tool_name: str, arguments: dict | None = None):
    return {
        "ok": False,
        "error": "Not implemented yet",
        "family": FAMILY_NAME,
        "tool_name": tool_name,
        "arguments": arguments or {}
    }

async def list_changes(**kwargs):
    return await _not_implemented("list_changes", kwargs)
async def get_change(**kwargs):
    return await _not_implemented("get_change", kwargs)

def register_tools():
    return [
        "list_changes",
        "get_change",
    ]
