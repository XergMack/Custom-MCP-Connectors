FAMILY_NAME = "problems"

async def _not_implemented(tool_name: str, arguments: dict | None = None):
    return {
        "ok": False,
        "error": "Not implemented yet",
        "family": FAMILY_NAME,
        "tool_name": tool_name,
        "arguments": arguments or {}
    }

async def list_problems(**kwargs):
    return await _not_implemented("list_problems", kwargs)
async def get_problem(**kwargs):
    return await _not_implemented("get_problem", kwargs)

def register_tools():
    return [
    "list_problems",
    "get_problem",
    ]
