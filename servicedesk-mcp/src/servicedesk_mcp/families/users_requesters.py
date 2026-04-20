FAMILY_NAME = "users_requesters"

async def _not_implemented(tool_name: str, arguments: dict | None = None):
    return {
        "ok": False,
        "error": "Not implemented yet",
        "family": FAMILY_NAME,
        "tool_name": tool_name,
        "arguments": arguments or {}
    }

async def list_requesters(**kwargs):
    return await _not_implemented("list_requesters", kwargs)
async def get_requester(**kwargs):
    return await _not_implemented("get_requester", kwargs)
async def search_requesters(**kwargs):
    return await _not_implemented("search_requesters", kwargs)

def register_tools():
    return [
    "list_requesters",
    "get_requester",
    "search_requesters",
    ]
