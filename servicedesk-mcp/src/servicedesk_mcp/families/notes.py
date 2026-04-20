from servicedesk_mcp.core.client import ServiceDeskClient

FAMILY_NAME = "notes"

async def list_request_notes(request_id: str):
    client = ServiceDeskClient()
    response = await client.get(f"/requests/{request_id}/notes")
    return response.json()

async def add_request_note(request_id: str, payload: dict):
    client = ServiceDeskClient()
    response = await client.post(f"/requests/{request_id}/notes", json_body=payload)
    return response.json()

def register_tools():
    return [
        "list_request_notes",
        "add_request_note",
    ]
