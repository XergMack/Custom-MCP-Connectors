from app.mcp.handlers._service import svc
def handle_search_items(query: str, site_id: str = "", drive_id: str = ""):
    return svc.search_items(query, site_id, drive_id)
