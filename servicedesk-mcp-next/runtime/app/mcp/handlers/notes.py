from app.mcp.handlers._service import svc

async def handle_list_request_notes(request_id: str):
    return await svc.list_request_notes(request_id=request_id)

async def handle_add_request_note(request_id: str, payload: dict):
    return await svc.add_request_note(request_id=request_id, payload=payload)

async def handle_add_request_note_simple(request_id: str, description: str, show_to_requester: bool = False):
    return await svc.add_request_note_simple(
        request_id=request_id,
        description=description,
        show_to_requester=show_to_requester,
    )
