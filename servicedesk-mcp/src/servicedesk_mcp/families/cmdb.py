FAMILY_NAME = "cmdb"

async def _not_implemented(tool_name: str, arguments: dict | None = None):
    return {
        "ok": False,
        "error": "Not implemented yet",
        "family": FAMILY_NAME,
        "tool_name": tool_name,
        "arguments": arguments or {}
    }

async def list_cis(**kwargs):
    return await _not_implemented("list_cis", kwargs)
async def get_ci(**kwargs):
    return await _not_implemented("get_ci", kwargs)
async def search_cis(**kwargs):
    return await _not_implemented("search_cis", kwargs)

def register_tools():
    return [
        "list_cis",
        "get_ci",
        "search_cis",
    ]
