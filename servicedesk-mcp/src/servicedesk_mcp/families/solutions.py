from servicedesk_mcp.core.client import ServiceDeskClient

FAMILY_NAME = "solutions"

async def list_solutions(params: dict | None = None):
    client = ServiceDeskClient()
    response = await client.get("/solutions", params=params or {})
    return response.json()

async def get_solution(solution_id: str):
    client = ServiceDeskClient()
    response = await client.get(f"/solutions/{solution_id}")
    return response.json()

async def search_solutions(
    title_contains: str | None = None,
    start_index: int = 1,
    row_count: int = 100,
):
    criteria = []

    if title_contains:
        criteria.append({
            "field": "title",
            "condition": "contains",
            "value": title_contains
        })

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

    return await list_solutions(params)

def register_tools():
    return [
        "list_solutions",
        "get_solution",
        "search_solutions",
    ]
