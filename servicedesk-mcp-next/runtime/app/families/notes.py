from app.core.client import ServiceDeskClient

FAMILY_NAME = "notes"

async def list_request_notes(request_id: str):
    client = ServiceDeskClient()
    return await client.get(f"/requests/{request_id}/notes")

async def add_request_note(request_id: str, payload: dict):
    client = ServiceDeskClient()
    return await client.post(f"/requests/{request_id}/notes", json_body=payload)

async def add_request_note_simple(request_id: str, description: str, show_to_requester: bool = False):
    payload = {
        "description": description,
        "show_to_requester": bool(show_to_requester)
    }
    return await add_request_note(request_id=request_id, payload=payload)
