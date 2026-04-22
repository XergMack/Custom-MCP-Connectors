from mcp.server.fastmcp import FastMCP

from app.mcp.handlers.health import handle_health
from app.mcp.handlers.requests import (
    handle_list_requests,
    handle_get_request,
    handle_create_request,
    handle_update_request,
    handle_create_request_from_context,
)
from app.mcp.handlers.notes import (
    handle_list_request_notes,
    handle_add_request_note,
)
from app.mcp.handlers.worklogs import (
    handle_list_request_worklogs,
    handle_add_request_worklog,
)
from app.mcp.handlers.tasks import (
    handle_list_request_tasks,
    handle_add_request_task,
    handle_update_request_task,
)

def register_tools(mcp: FastMCP):
    @mcp.tool(name="health")
    async def health():
        return await handle_health()

    @mcp.tool(name="list_requests")
    async def list_requests(params: dict = {}):
        return await handle_list_requests(params=params)

    @mcp.tool(name="get_request")
    async def get_request(request_id: str):
        return await handle_get_request(request_id=request_id)

    @mcp.tool(name="create_request")
    async def create_request(payload: dict):
        return await handle_create_request(payload=payload)

    @mcp.tool(name="update_request")
    async def update_request(request_id: str, payload: dict):
        return await handle_update_request(request_id=request_id, payload=payload)

    @mcp.tool(name="create_request_from_context")
    async def create_request_from_context(subject: str, description: str, requester_name: str):
        return await handle_create_request_from_context(
            subject=subject,
            description=description,
            requester_name=requester_name,
        )

    @mcp.tool(name="list_request_notes")
    async def list_request_notes(request_id: str):
        return await handle_list_request_notes(request_id=request_id)

    @mcp.tool(name="add_request_note")
    async def add_request_note(request_id: str, payload: dict):
        return await handle_add_request_note(request_id=request_id, payload=payload)

    @mcp.tool(name="list_request_worklogs")
    async def list_request_worklogs(request_id: str):
        return await handle_list_request_worklogs(request_id=request_id)

    @mcp.tool(name="add_request_worklog")
    async def add_request_worklog(request_id: str, payload: dict):
        return await handle_add_request_worklog(request_id=request_id, payload=payload)

    @mcp.tool(name="list_request_tasks")
    async def list_request_tasks(request_id: str):
        return await handle_list_request_tasks(request_id=request_id)

    @mcp.tool(name="add_request_task")
    async def add_request_task(request_id: str, payload: dict):
        return await handle_add_request_task(request_id=request_id, payload=payload)

    @mcp.tool(name="update_request_task")
    async def update_request_task(request_id: str, task_id: str, payload: dict):
        return await handle_update_request_task(request_id=request_id, task_id=task_id, payload=payload)
