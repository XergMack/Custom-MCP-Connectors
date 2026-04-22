from app.mcp.handlers._service import svc

async def handle_list_requests(params: dict | None = None):
    return await svc.list_requests(params=params)

async def handle_get_request(request_id: str):
    return await svc.get_request(request_id=request_id)

async def handle_create_request(payload: dict):
    return await svc.create_request(payload=payload)

async def handle_update_request(request_id: str, payload: dict):
    return await svc.update_request(request_id=request_id, payload=payload)

async def handle_create_request_from_context(subject: str, description: str, requester_name: str):
    return await svc.create_request_from_context(
        subject=subject,
        description=description,
        requester_name=requester_name,
    )

async def handle_create_request_for_requester_id(subject: str, description: str, requester_id: str):
    return await svc.create_request_for_requester_id(
        subject=subject,
        description=description,
        requester_id=requester_id,
    )

async def handle_update_request_status(request_id: str, status_id: str):
    return await svc.update_request_status(
        request_id=request_id,
        status_id=status_id,
    )

async def handle_update_request_subject_and_description(request_id: str, subject: str, description: str):
    return await svc.update_request_subject_and_description(
        request_id=request_id,
        subject=subject,
        description=description,
    )
