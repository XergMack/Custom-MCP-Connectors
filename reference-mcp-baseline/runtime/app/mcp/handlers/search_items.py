from app.mcp.handlers._service import svc
def handle_search_items(query: str):
    return svc.search_items(query)
