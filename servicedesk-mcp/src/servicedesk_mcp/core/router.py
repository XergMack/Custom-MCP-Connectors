from typing import Any

from servicedesk_mcp.families import requests as requests_family
from servicedesk_mcp.families import notes as notes_family
from servicedesk_mcp.families import worklogs as worklogs_family
from servicedesk_mcp.families import tasks as tasks_family

TOOL_REGISTRY = {
    "list_requests": requests_family.list_requests,
    "get_request": requests_family.get_request,
    "create_request": requests_family.create_request,
    "update_request": requests_family.update_request,
    "search_requests": requests_family.search_requests,
    "get_my_open_requests": requests_family.get_my_open_requests,
    "search_requests_by_subject": requests_family.search_requests_by_subject,
    "search_requests_by_requester": requests_family.search_requests_by_requester,

    "list_request_notes": notes_family.list_request_notes,
    "add_request_note": notes_family.add_request_note,

    "list_request_worklogs": worklogs_family.list_request_worklogs,
    "add_request_worklog": worklogs_family.add_request_worklog,

    "list_request_tasks": tasks_family.list_request_tasks,
    "add_request_task": tasks_family.add_request_task,
    "update_request_task": tasks_family.update_request_task,
}

def list_tools() -> dict[str, list[str]]:
    return {
        "requests": requests_family.register_tools(),
        "notes": notes_family.register_tools(),
        "worklogs": worklogs_family.register_tools(),
        "tasks": tasks_family.register_tools(),
    }

async def call_tool(tool_name: str, arguments: dict[str, Any] | None = None) -> Any:
    args = arguments or {}

    if tool_name not in TOOL_REGISTRY:
        return {
            "ok": False,
            "error": f"Unknown tool: {tool_name}",
            "available_tools": sorted(TOOL_REGISTRY.keys()),
        }

    handler = TOOL_REGISTRY[tool_name]
    return await handler(**args)
