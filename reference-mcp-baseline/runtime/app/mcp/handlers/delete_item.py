from app.mcp.handlers._service import svc
def handle_delete_item(path: str, site_id: str = "", drive_id: str = ""):
    return svc.delete_item(path, site_id, drive_id)
