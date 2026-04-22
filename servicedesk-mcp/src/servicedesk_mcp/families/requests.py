from servicedesk_mcp.core.client import ServiceDeskClient
from servicedesk_mcp.families import users_requesters as requesters_family
from servicedesk_mcp.families import technicians as technicians_family
from servicedesk_mcp.families import departments_groups_sites as dgs_family
from servicedesk_mcp.families import admin as admin_family

FAMILY_NAME = "requests"


async def list_requests(params: dict | None = None):
    client = ServiceDeskClient()
    response = await client.get("/requests", params=params or {})
    return response.json()


async def get_request(request_id: str):
    client = ServiceDeskClient()
    response = await client.get(f"/requests/{request_id}")
    return response.json()


async def create_request(payload: dict):
    client = ServiceDeskClient()
    response = await client.post("/requests", json_body=payload)
    return response.json()


async def update_request(request_id: str, payload: dict):
    client = ServiceDeskClient()
    response = await client.put(f"/requests/{request_id}", json_body=payload)
    return response.json()


async def assign_request(request_id: str, payload: dict):
    client = ServiceDeskClient()
    response = await client.put(f"/requests/{request_id}/assign", json_body=payload)
    return response.json()


async def search_requests(
    technician_name: str | None = None,
    status_name: str | None = None,
    subject_contains: str | None = None,
    requester_name: str | None = None,
    start_index: int = 1,
    row_count: int = 100,
):
    criteria = []

    if technician_name:
        criteria.append({
            "field": "technician.name",
            "condition": "is",
            "value": technician_name,
        })

    if status_name:
        criteria.append({
            "field": "status.name",
            "condition": "is",
            "value": status_name,
            "logical_operator": "and" if criteria else None,
        })

    if subject_contains:
        criteria.append({
            "field": "subject",
            "condition": "contains",
            "value": subject_contains,
            "logical_operator": "and" if criteria else None,
        })

    if requester_name:
        criteria.append({
            "field": "requester.name",
            "condition": "contains",
            "value": requester_name,
            "logical_operator": "and" if criteria else None,
        })

    for c in criteria:
        if c.get("logical_operator") is None:
            c.pop("logical_operator", None)

    params = {
        "input_data": {
            "list_info": {
                "row_count": row_count,
                "start_index": start_index,
                "get_total_count": True,
            }
        }
    }

    if criteria:
        params["input_data"]["list_info"]["search_criteria"] = criteria

    return await list_requests(params)


async def get_my_open_requests(
    technician_name: str = "Matthew MacKinnon",
    start_index: int = 1,
    row_count: int = 100,
):
    return await search_requests(
        technician_name=technician_name,
        status_name="Open",
        start_index=start_index,
        row_count=row_count,
    )


async def search_requests_by_subject(
    subject_contains: str,
    technician_name: str | None = None,
    status_name: str | None = None,
    start_index: int = 1,
    row_count: int = 100,
):
    return await search_requests(
        technician_name=technician_name,
        status_name=status_name,
        subject_contains=subject_contains,
        start_index=start_index,
        row_count=row_count,
    )


async def search_requests_by_requester(
    requester_name: str,
    technician_name: str | None = None,
    status_name: str | None = None,
    start_index: int = 1,
    row_count: int = 100,
):
    return await search_requests(
        technician_name=technician_name,
        status_name=status_name,
        requester_name=requester_name,
        start_index=start_index,
        row_count=row_count,
    )


def _normalize(s: str | None) -> str:
    return (s or "").strip().lower()


def _is_default_template_name(s: str | None) -> bool:
    return _normalize(s) in ("", "default", "default request")


def _extract_list(result: dict, key: str) -> list:
    value = result.get(key, [])
    return value if isinstance(value, list) else []


def _match_by_name(items: list, target_name: str, field_name: str = "name") -> list:
    target = _normalize(target_name)
    exact = [x for x in items if _normalize(x.get(field_name)) == target]
    if exact:
        return exact
    contains = [x for x in items if target in _normalize(x.get(field_name))]
    return contains


def _as_id_name(item: dict | None) -> dict | None:
    if not item:
        return None
    value = item.get("id")
    return {
        "id": str(value) if value is not None else None,
        "name": item.get("name"),
    }


def _is_success_response(result: dict | None) -> bool:
    if not isinstance(result, dict):
        return False

    response_status = result.get("response_status")
    if isinstance(response_status, dict):
        return response_status.get("status_code") == 2000 or _normalize(response_status.get("status")) == "success"

    if isinstance(response_status, list):
        return any(
            isinstance(entry, dict)
            and (entry.get("status_code") == 2000 or _normalize(entry.get("status")) == "success")
            for entry in response_status
        )

    return False


def _extract_created_request_id(result: dict | None) -> str | None:
    if not isinstance(result, dict):
        return None

    request = result.get("request")
    if isinstance(request, dict) and request.get("id") is not None:
        return str(request.get("id"))

    requests = result.get("requests")
    if isinstance(requests, list) and requests:
        first = requests[0]
        if isinstance(first, dict) and first.get("id") is not None:
            return str(first.get("id"))

    return None


def _extract_request_object(result: dict | None) -> dict | None:
    if not isinstance(result, dict):
        return None
    request = result.get("request")
    return request if isinstance(request, dict) else None


def _verify_field_by_id_or_name(actual: dict | None, expected: dict | None, field_name: str) -> dict | None:
    if expected is None:
        return None

    actual = actual or {}
    actual_id = actual.get("id")
    expected_id = expected.get("id")
    actual_name = actual.get("name")
    expected_name = expected.get("name")

    if expected_id is not None and str(actual_id) == str(expected_id):
        return None

    if _normalize(actual_name) == _normalize(expected_name):
        return None

    return {
        "field": field_name,
        "expected": expected,
        "actual": {"id": actual_id, "name": actual_name},
    }


def _verify_category(actual: dict | None, expected: dict | None) -> dict | None:
    if expected is None:
        return None

    actual = actual or {}
    if _normalize(actual.get("name")) == _normalize(expected.get("name")):
        return None

    return {
        "field": "category",
        "expected": expected,
        "actual": {"id": actual.get("id"), "name": actual.get("name")},
    }


def _build_verification(actual_request: dict | None, expected: dict) -> dict:
    actual_request = actual_request or {}
    mismatches = []

    mismatch = _verify_field_by_id_or_name(actual_request.get("requester"), expected.get("requester"), "requester")
    if mismatch:
        mismatches.append(mismatch)

    mismatch = _verify_field_by_id_or_name(actual_request.get("template"), expected.get("template"), "template")
    if mismatch:
        mismatches.append(mismatch)

    mismatch = _verify_field_by_id_or_name(actual_request.get("site"), expected.get("site"), "site")
    if mismatch:
        mismatches.append(mismatch)

    mismatch = _verify_field_by_id_or_name(actual_request.get("priority"), expected.get("priority"), "priority")
    if mismatch:
        mismatches.append(mismatch)

    mismatch = _verify_field_by_id_or_name(actual_request.get("status"), expected.get("status"), "status")
    if mismatch:
        mismatches.append(mismatch)

    mismatch = _verify_field_by_id_or_name(actual_request.get("technician"), expected.get("technician"), "technician")
    if mismatch:
        mismatches.append(mismatch)

    mismatch = _verify_field_by_id_or_name(actual_request.get("group"), expected.get("group"), "group")
    if mismatch:
        mismatches.append(mismatch)

    mismatch = _verify_category(actual_request.get("category"), expected.get("category"))
    if mismatch:
        mismatches.append(mismatch)

    return {
        "ok": len(mismatches) == 0,
        "mismatches": mismatches,
        "actual": {
            "requester": _as_id_name(actual_request.get("requester")),
            "template": _as_id_name(actual_request.get("template")),
            "site": _as_id_name(actual_request.get("site")),
            "priority": _as_id_name(actual_request.get("priority")),
            "status": _as_id_name(actual_request.get("status")),
            "technician": _as_id_name(actual_request.get("technician")),
            "group": _as_id_name(actual_request.get("group")),
            "category": _as_id_name(actual_request.get("category")),
        },
    }


async def _resolve_requester(requester_name: str) -> dict:
    result = await requesters_family.search_requesters(
        name_contains=requester_name,
        start_index=1,
        row_count=50,
    )
    users = _extract_list(result, "users")
    matches = _match_by_name(users, requester_name, "name")

    if len(matches) == 1:
        return {"ok": True, "item": matches[0]}

    if len(matches) == 0:
        return {"ok": False, "error": f"Requester not found: {requester_name}"}

    return {
        "ok": False,
        "error": f"Requester is ambiguous: {requester_name}",
        "matches": [
            {"id": x.get("id"), "name": x.get("name"), "email_id": x.get("email_id")}
            for x in matches[:10]
        ],
    }


async def _resolve_technician(technician_name: str) -> dict:
    result = await technicians_family.list_technicians(
        params={
            "input_data": {
                "list_info": {
                    "row_count": 200,
                    "start_index": 1,
                    "get_total_count": True,
                }
            }
        }
    )
    techs = _extract_list(result, "technicians")
    matches = _match_by_name(techs, technician_name, "name")

    if len(matches) == 1:
        return {"ok": True, "item": matches[0]}

    if len(matches) == 0:
        return {"ok": False, "error": f"Technician not found: {technician_name}"}

    return {
        "ok": False,
        "error": f"Technician is ambiguous: {technician_name}",
        "matches": [{"id": x.get("id"), "name": x.get("name")} for x in matches[:10]],
    }


async def _resolve_site(site_name: str) -> dict:
    result = await dgs_family.list_sites()
    sites = _extract_list(result, "sites")
    matches = _match_by_name(sites, site_name, "name")

    if len(matches) == 1:
        return {"ok": True, "item": matches[0]}

    if len(matches) == 0:
        return {"ok": False, "error": f"Site not found: {site_name}"}

    return {
        "ok": False,
        "error": f"Site is ambiguous: {site_name}",
        "matches": [{"id": x.get("id"), "name": x.get("name")} for x in matches[:10]],
    }


async def _resolve_group(group_name: str, site_name: str | None = None) -> dict:
    result = await dgs_family.list_groups()
    groups = _extract_list(result, "support_groups")
    matches = _match_by_name(groups, group_name, "name")

    if site_name and matches:
        site_filtered = [
            x for x in matches
            if _normalize((x.get("site") or {}).get("name")) == _normalize(site_name)
        ]
        if len(site_filtered) == 1:
            return {"ok": True, "item": site_filtered[0]}
        if len(site_filtered) > 1:
            matches = site_filtered

    if len(matches) == 1:
        return {"ok": True, "item": matches[0]}

    if len(matches) == 0:
        return {"ok": False, "error": f"Support group not found: {group_name}"}

    return {
        "ok": False,
        "error": f"Support group is ambiguous: {group_name}",
        "matches": [
            {
                "id": x.get("id"),
                "name": x.get("name"),
                "site": (x.get("site") or {}).get("name"),
            }
            for x in matches[:10]
        ],
    }


async def _resolve_priority(priority_name: str) -> dict:
    result = await admin_family.list_priorities()
    priorities = _extract_list(result, "priorities")
    matches = _match_by_name(priorities, priority_name, "name")

    if len(matches) == 1:
        return {"ok": True, "item": matches[0]}

    if len(matches) == 0:
        return {"ok": False, "error": f"Priority not found: {priority_name}"}

    return {
        "ok": False,
        "error": f"Priority is ambiguous: {priority_name}",
        "matches": [{"id": x.get("id"), "name": x.get("name")} for x in matches[:10]],
    }


async def _resolve_status(status_name: str) -> dict:
    result = await admin_family.list_statuses()
    statuses = _extract_list(result, "statuses")
    matches = _match_by_name(statuses, status_name, "name")

    if len(matches) == 1:
        return {"ok": True, "item": matches[0]}

    if len(matches) == 0:
        return {"ok": False, "error": f"Status not found: {status_name}"}

    return {
        "ok": False,
        "error": f"Status is ambiguous: {status_name}",
        "matches": [{"id": x.get("id"), "name": x.get("name")} for x in matches[:10]],
    }


async def _resolve_template(template_name: str | None) -> dict:
    result = await admin_family.list_templates()
    templates = _extract_list(result, "request_templates")
    target_name = "Default Request" if _is_default_template_name(template_name) else template_name
    matches = _match_by_name(templates, target_name, "name")

    if len(matches) == 1:
        return {"ok": True, "item": matches[0]}

    if len(matches) == 0:
        return {"ok": False, "error": f"Request template not found: {target_name}"}

    return {
        "ok": False,
        "error": f"Request template is ambiguous: {target_name}",
        "matches": [{"id": x.get("id"), "name": x.get("name")} for x in matches[:10]],
    }


async def _fetch_request_for_verification(request_id: str) -> dict:
    fetched = await get_request(request_id)
    actual_request = _extract_request_object(fetched)
    return {"raw": fetched, "request": actual_request}


async def _apply_assign_fallback(
    request_id: str,
    resolved_technician: dict | None,
    resolved_group: dict | None,
) -> dict | None:
    request_payload = {}

    if resolved_group:
        request_payload["group"] = {"id": resolved_group["id"]}

    if resolved_technician:
        request_payload["technician"] = {"id": resolved_technician["id"]}

    if not request_payload:
        return None

    payload = {"request": request_payload}
    result = await assign_request(request_id, payload)

    return {
        "action": "assign_request",
        "payload": payload,
        "result": result,
        "ok": _is_success_response(result),
        "reason": (
            "Compatibility fallback after create verification mismatch. "
            "Primary path is doc-first create/edit; fallback uses documented /assign endpoint."
        ),
    }


async def create_request_from_context(
    subject: str,
    description: str,
    requester_name: str,
    template_name: str | None = None,
    site_name: str | None = None,
    priority_name: str | None = None,
    status_name: str | None = None,
    technician_name: str | None = None,
    group_name: str | None = None,
    category_name: str | None = None,
):
    validation_errors = []
    if not subject or not subject.strip():
        validation_errors.append("subject is required")
    if not description or not description.strip():
        validation_errors.append("description is required")
    if not requester_name or not requester_name.strip():
        validation_errors.append("requester_name is required")

    if validation_errors:
        return {"ok": False, "error": "Validation failed", "details": validation_errors}

    requester_res = await _resolve_requester(requester_name)
    if not requester_res.get("ok"):
        return requester_res

    template_res = await _resolve_template(template_name)
    if not template_res.get("ok"):
        return template_res

    payload_request = {
        "subject": subject,
        "description": description,
        "requester": {"id": str(requester_res["item"].get("id"))},
        "template": {"id": str(template_res["item"].get("id"))},
    }

    resolved_site = None
    resolved_priority = None
    resolved_status = None
    resolved_technician = None
    resolved_group = None
    resolved_category = None

    if site_name:
        site_res = await _resolve_site(site_name)
        if not site_res.get("ok"):
            return site_res
        payload_request["site"] = {"id": str(site_res["item"].get("id"))}
        resolved_site = _as_id_name(site_res["item"])

    if priority_name:
        priority_res = await _resolve_priority(priority_name)
        if not priority_res.get("ok"):
            return priority_res
        payload_request["priority"] = {"id": str(priority_res["item"].get("id"))}
        resolved_priority = _as_id_name(priority_res["item"])

    if status_name:
        status_res = await _resolve_status(status_name)
        if not status_res.get("ok"):
            return status_res
        payload_request["status"] = {"id": str(status_res["item"].get("id"))}
        resolved_status = _as_id_name(status_res["item"])

    if technician_name:
        technician_res = await _resolve_technician(technician_name)
        if not technician_res.get("ok"):
            return technician_res
        payload_request["technician"] = {"id": str(technician_res["item"].get("id"))}
        resolved_technician = _as_id_name(technician_res["item"])

    if group_name:
        group_res = await _resolve_group(group_name, site_name=site_name)
        if not group_res.get("ok"):
            return group_res
        payload_request["group"] = {"id": str(group_res["item"].get("id"))}
        resolved_group = _as_id_name(group_res["item"])
        if resolved_group is not None:
            resolved_group["site"] = (group_res["item"].get("site") or {}).get("name")

    if category_name:
        payload_request["category"] = {"name": category_name}
        resolved_category = {"name": category_name}

    final_payload = {"request": payload_request}
    created = await create_request(final_payload)
    created_request_id = _extract_created_request_id(created)

    verification = None
    fetched_after_create = None
    compatibility_actions = []

    if created_request_id:
        fetched_after_create = await _fetch_request_for_verification(created_request_id)
        verification = _build_verification(
            fetched_after_create.get("request"),
            {
                "requester": _as_id_name(requester_res["item"]),
                "template": _as_id_name(template_res["item"]),
                "site": resolved_site,
                "priority": resolved_priority,
                "status": resolved_status,
                "technician": resolved_technician,
                "group": resolved_group,
                "category": resolved_category,
            },
        )

        needs_assign_fallback = False
        if verification and not verification.get("ok"):
            mismatch_fields = {m.get("field") for m in verification.get("mismatches", [])}
            if "technician" in mismatch_fields or "group" in mismatch_fields:
                needs_assign_fallback = True

        if needs_assign_fallback:
            assign_result = await _apply_assign_fallback(
                created_request_id,
                resolved_technician=resolved_technician,
                resolved_group=resolved_group,
            )
            if assign_result:
                compatibility_actions.append(assign_result)
                fetched_after_assign = await _fetch_request_for_verification(created_request_id)
                verification = _build_verification(
                    fetched_after_assign.get("request"),
                    {
                        "requester": _as_id_name(requester_res["item"]),
                        "template": _as_id_name(template_res["item"]),
                        "site": resolved_site,
                        "priority": resolved_priority,
                        "status": resolved_status,
                        "technician": resolved_technician,
                        "group": resolved_group,
                        "category": resolved_category,
                    },
                )
                fetched_after_create = fetched_after_assign

    return {
        "ok": _is_success_response(created) and (verification is None or verification.get("ok", False)),
        "resolved": {
            "requester": _as_id_name(requester_res["item"]),
            "template": _as_id_name(template_res["item"]),
            "site": resolved_site,
            "priority": resolved_priority,
            "status": resolved_status,
            "technician": resolved_technician,
            "group": resolved_group,
            "category": resolved_category,
        },
        "payload": final_payload,
        "created": created,
        "request_id": created_request_id,
        "verification": verification,
        "fetched_request": fetched_after_create.get("raw") if isinstance(fetched_after_create, dict) else None,
        "compatibility_actions": compatibility_actions,
    }


def register_tools():
    return [
        "list_requests",
        "get_request",
        "create_request",
        "update_request",
        "assign_request",
        "search_requests",
        "get_my_open_requests",
        "search_requests_by_subject",
        "search_requests_by_requester",
        "create_request_from_context",
    ]
