from servicedesk_mcp.core.client import ServiceDeskClient

FAMILY_NAME = "users_requesters"

async def list_requesters(params: dict | None = None):
    client = ServiceDeskClient()
    response = await client.get("/requesters", params=params or {})
    return response.json()

async def get_requester(requester_id: str):
    client = ServiceDeskClient()
    response = await client.get(f"/requesters/{requester_id}")
    return response.json()

async def search_requesters(
    name_contains: str | None = None,
    email_contains: str | None = None,
    start_index: int = 1,
    row_count: int = 100,
):
    criteria = []

    if name_contains:
        criteria.append({
            "field": "name",
            "condition": "contains",
            "value": name_contains
        })

    if email_contains:
        criteria.append({
            "field": "email_id",
            "condition": "contains",
            "value": email_contains,
            "logical_operator": "and" if criteria else None
        })

    for c in criteria:
        if c.get("logical_operator") is None:
            c.pop("logical_operator", None)

    params = {
        "input_data": {
            "list_info": {
                "row_count": row_count,
                "start_index": start_index,
                "get_total_count": True
            }
        }
    }

    if criteria:
        params["input_data"]["list_info"]["search_criteria"] = criteria

    return await list_requesters(params)

def register_tools():
    return [
        "list_requesters",
        "get_requester",
        "search_requesters",
    ]
