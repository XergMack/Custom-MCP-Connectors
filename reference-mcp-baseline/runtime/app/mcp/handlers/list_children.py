from app.mcp.handlers._service import svc
def handle_list_children(path: str = "", site_id: str = "", drive_id: str = ""):
    return svc.list_children(path, site_id, drive_id)
