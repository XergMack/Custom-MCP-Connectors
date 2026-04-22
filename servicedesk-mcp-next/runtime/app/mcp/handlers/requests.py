from app.mcp.handlers._service import svc

async def handle_list_requests(params: dict | None = None):
    return await svc.list_requests(params=params)

async def handle_get_request(request_id: str):
    return await svc.get_request(request_id=request_id)

async def handle_create_request(payload: dict):
    return await svc.create_request(payload=payload)

async def handle_update_request(request_id: str, payload: dict):
    return await svc.update_request(request_id=request_id, payload=payload)
