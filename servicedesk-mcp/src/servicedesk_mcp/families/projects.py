FAMILY_NAME = "projects"

async def _not_implemented(tool_name: str, arguments: dict | None = None):
    return {
        "ok": False,
        "error": "Not implemented yet",
        "family": FAMILY_NAME,
        "tool_name": tool_name,
        "arguments": arguments or {}
    }

async def list_projects(**kwargs):
    return await _not_implemented("list_projects", kwargs)
async def get_project(**kwargs):
    return await _not_implemented("get_project", kwargs)

def register_tools():
    return [
        "list_projects",
        "get_project",
    ]
