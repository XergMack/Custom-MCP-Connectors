from app.mcp.handlers._service import svc

async def handle_list_request_worklogs(request_id: str):
    return await svc.list_request_worklogs(request_id=request_id)

async def handle_add_request_worklog(request_id: str, payload: dict):
    return await svc.add_request_worklog(request_id=request_id, payload=payload)
