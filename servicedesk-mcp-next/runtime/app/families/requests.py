from app.core.client import ServiceDeskClient
from app.families import users_requesters as requesters_family

FAMILY_NAME = "requests"

async def list_requests(params: dict | None = None):
    client = ServiceDeskClient()
    return await client.get("/requests", params=params or {})

async def get_request(request_id: str):
    client = ServiceDeskClient()
    return await client.get(f"/requests/{request_id}")

async def create_request(payload: dict):
    client = ServiceDeskClient()
    wrapped_payload = {"request": payload}
    return await client.post("/requests", json_body=wrapped_payload)

async def update_request(request_id: str, payload: dict):
    client = ServiceDeskClient()
    wrapped_payload = {"request": payload}
    return await client.put(f"/requests/{request_id}", json_body=wrapped_payload)

async def create_request_for_requester_id(subject: str, description: str, requester_id: str):
    payload = {
        "subject": subject,
        "description": description,
        "requester": {
            "id": str(requester_id)
        }
    }
    return await create_request(payload)

async def update_request_status(request_id: str, status_id: str):
    payload = {
        "status": {
            "id": str(status_id)
        }
    }
    return await update_request(request_id=request_id, payload=payload)

async def update_request_subject_and_description(request_id: str, subject: str, description: str):
    payload = {
        "subject": subject,
        "description": description
    }
    return await update_request(request_id=request_id, payload=payload)

def _extract_users(result: dict) -> list[dict]:
    if isinstance(result, dict):
        if isinstance(result.get("users"), list):
            return result["users"]
        if isinstance(result.get("requesters"), list):
            return result["requesters"]
    return []

def _match_by_name(items: list[dict], expected_name: str) -> list[dict]:
    expected = (expected_name or "").strip().lower()
    return [x for x in items if (x.get("name") or "").strip().lower() == expected]

async def _resolve_requester(requester_name: str) -> dict:
    result = await requesters_family.search_requesters(name_contains=requester_name, row_count=10)
    users = _extract_users(result)
    exact = _match_by_name(users, requester_name)

    if len(exact) == 1:
        return {"ok": True, "item": exact[0]}
    if len(exact) > 1:
        return {
            "ok": False,
            "error": f"Requester is ambiguous: {requester_name}",
            "matches": [{"id": x.get("id"), "name": x.get("name")} for x in exact]
        }
    if len(users) == 1:
        return {"ok": True, "item": users[0]}
    if not users:
        return {"ok": False, "error": f"Requester not found: {requester_name}"}

    return {
        "ok": False,
        "error": f"Requester is ambiguous: {requester_name}",
        "matches": [{"id": x.get("id"), "name": x.get("name")} for x in users]
    }

async def create_request_from_context(subject: str, description: str, requester_name: str):
    validation_errors = []

    if not subject or not subject.strip():
        validation_errors.append("subject is required")
    if not description or not description.strip():
        validation_errors.append("description is required")
    if not requester_name or not requester_name.strip():
        validation_errors.append("requester_name is required")

    if validation_errors:
        return {"ok": False, "validation_errors": validation_errors}

    requester_res = await _resolve_requester(requester_name)
    if not requester_res.get("ok"):
        return requester_res

    requester = requester_res["item"]

    final_payload = {
        "subject": subject,
        "description": description,
        "requester": {
            "id": requester.get("id"),
            "name": requester.get("name")
        }
    }

    created = await create_request(final_payload)
    return {
        "ok": True,
        "requester": {
            "id": requester.get("id"),
            "name": requester.get("name")
        },
        "created": created
    }
