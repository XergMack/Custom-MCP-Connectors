FAMILY_NAME = "assets"

async def _not_implemented(tool_name: str, arguments: dict | None = None):
    return {
        "ok": False,
        "error": "Not implemented yet",
        "family": FAMILY_NAME,
        "tool_name": tool_name,
        "arguments": arguments or {}
    }

async def list_assets(**kwargs):
    return await _not_implemented("list_assets", kwargs)
async def get_asset(**kwargs):
    return await _not_implemented("get_asset", kwargs)
async def search_assets(**kwargs):
    return await _not_implemented("search_assets", kwargs)

def register_tools():
    return [
        "list_assets",
        "get_asset",
        "search_assets",
    ]
