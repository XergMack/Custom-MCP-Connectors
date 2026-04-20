FAMILY_NAME = "departments_groups_sites"

async def _not_implemented(tool_name: str, arguments: dict | None = None):
    return {
        "ok": False,
        "error": "Not implemented yet",
        "family": FAMILY_NAME,
        "tool_name": tool_name,
        "arguments": arguments or {}
    }

async def list_departments(**kwargs):
    return await _not_implemented("list_departments", kwargs)
async def list_groups(**kwargs):
    return await _not_implemented("list_groups", kwargs)
async def list_sites(**kwargs):
    return await _not_implemented("list_sites", kwargs)
async def get_site(**kwargs):
    return await _not_implemented("get_site", kwargs)

def register_tools():
    return [
        "list_departments",
        "list_groups",
        "list_sites",
        "get_site",
    ]
