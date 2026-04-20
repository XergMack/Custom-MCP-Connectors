from servicedesk_mcp.core.client import ServiceDeskClient

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

async def search_requests(
    technician_name: str | None = None,
    status_name: str | None = None,
    subject_contains: str | None = None,
    start_index: int = 1,
    row_count: int = 100,
):
    criteria = []

    if technician_name:
        criteria.append({
            "field": "technician.name",
            "condition": "is",
            "value": technician_name
        })

    if status_name:
        criteria.append({
            "field": "status.name",
            "condition": "is",
            "value": status_name,
            "logical_operator": "and" if criteria else None
        })

    if subject_contains:
        criteria.append({
            "field": "subject",
            "condition": "contains",
            "value": subject_contains,
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

    return await list_requests(params)

def register_tools():
    return [
        "list_requests",
        "get_request",
        "create_request",
        "update_request",
        "search_requests",
    ]
