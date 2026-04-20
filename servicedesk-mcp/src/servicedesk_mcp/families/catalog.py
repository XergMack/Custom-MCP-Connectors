FAMILY_NAME = "catalog"

async def _not_implemented(tool_name: str, arguments: dict | None = None):
    return {
        "ok": False,
        "error": "Not implemented yet",
        "family": FAMILY_NAME,
        "tool_name": tool_name,
        "arguments": arguments or {}
    }

async def list_service_templates(**kwargs):
    return await _not_implemented("list_service_templates", kwargs)
async def get_service_template(**kwargs):
    return await _not_implemented("get_service_template", kwargs)

def register_tools():
    return [
        "list_service_templates",
        "get_service_template",
    ]
