from app.mcp.handlers._service import svc
def handle_get_item_versions(path: str, site_id: str = "", drive_id: str = ""):
    return svc.get_item_versions(path, site_id, drive_id)
