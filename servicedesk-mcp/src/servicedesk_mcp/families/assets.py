from servicedesk_mcp.core.client import ServiceDeskClient

FAMILY_NAME = "assets"

async def list_assets(params: dict | None = None):
    client = ServiceDeskClient()
    response = await client.get("/assets", params=params or {})
    return response.json()

async def get_asset(asset_id: str):
    client = ServiceDeskClient()
    response = await client.get(f"/assets/{asset_id}")
    return response.json()

async def search_assets(
    name_contains: str | None = None,
    asset_tag_contains: str | None = None,
    serial_number_contains: str | None = None,
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

    if asset_tag_contains:
        criteria.append({
            "field": "asset_tag",
            "condition": "contains",
            "value": asset_tag_contains,
            "logical_operator": "and" if criteria else None
        })

    if serial_number_contains:
        criteria.append({
            "field": "serial_number",
            "condition": "contains",
            "value": serial_number_contains,
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

    return await list_assets(params)

def register_tools():
    return [
        "list_assets",
        "get_asset",
        "search_assets",
    ]
