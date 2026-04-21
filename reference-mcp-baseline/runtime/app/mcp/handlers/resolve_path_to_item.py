from app.mcp.handlers._service import svc
def handle_resolve_path_to_item(path: str, site_id: str = "", drive_id: str = ""):
    return svc.resolve_path_to_item(path, site_id, drive_id)
