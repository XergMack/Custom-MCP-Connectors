FAMILY_NAME = "solutions"

async def _not_implemented(tool_name: str, arguments: dict | None = None):
    return {
        "ok": False,
        "error": "Not implemented yet",
        "family": FAMILY_NAME,
        "tool_name": tool_name,
        "arguments": arguments or {}
    }

async def list_solutions(**kwargs):
    return await _not_implemented("list_solutions", kwargs)
async def get_solution(**kwargs):
    return await _not_implemented("get_solution", kwargs)
async def search_solutions(**kwargs):
    return await _not_implemented("search_solutions", kwargs)

def register_tools():
    return [
    "list_solutions",
    "get_solution",
    "search_solutions",
    ]
