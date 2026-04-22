from app.mcp.handlers._service import svc

async def handle_list_request_tasks(request_id: str):
    return await svc.list_request_tasks(request_id=request_id)

async def handle_add_request_task(request_id: str, payload: dict):
    return await svc.add_request_task(request_id=request_id, payload=payload)

async def handle_update_request_task(request_id: str, task_id: str, payload: dict):
    return await svc.update_request_task(request_id=request_id, task_id=task_id, payload=payload)
