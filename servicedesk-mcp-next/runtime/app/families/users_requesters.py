from app.core.client import ServiceDeskClient

FAMILY_NAME = "users_requesters"

async def list_requesters(params: dict | None = None):
    client = ServiceDeskClient()
    return await client.get("/users", params=params or {})

async def search_requesters(name_contains: str, row_count: int = 10):
    client = ServiceDeskClient()
    params = {
        "input_data": {
            "list_info": {
                "row_count": row_count,
                "start_index": 1,
                "search_criteria": [
                    {
                        "field": "name",
                        "condition": "contains",
                        "value": name_contains
                    }
                ]
            }
        }
    }
    return await client.get("/users", params=params)
