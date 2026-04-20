FAMILY_NAME = "admin"

async def _not_implemented(tool_name: str, arguments: dict | None = None):
    return {
        "ok": False,
        "error": "Not implemented yet",
        "family": FAMILY_NAME,
        "tool_name": tool_name,
        "arguments": arguments or {}
    }

async def list_priorities(**kwargs):
    return await _not_implemented("list_priorities", kwargs)
async def list_statuses(**kwargs):
    return await _not_implemented("list_statuses", kwargs)
async def list_templates(**kwargs):
    return await _not_implemented("list_templates", kwargs)

def register_tools():
    return [
    "list_priorities",
    "list_statuses",
    "list_templates",
    ]
