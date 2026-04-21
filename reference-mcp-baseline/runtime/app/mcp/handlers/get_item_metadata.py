from app.mcp.handlers._service import svc
def handle_get_item_metadata(path: str, site_id: str = "", drive_id: str = ""):
    return svc.get_item_metadata(path, site_id, drive_id)
