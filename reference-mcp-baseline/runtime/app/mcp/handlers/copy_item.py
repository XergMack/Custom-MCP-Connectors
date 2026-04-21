from app.mcp.handlers._service import svc
def handle_copy_item(source: str, destination: str, site_id: str = "", drive_id: str = ""):
    return svc.copy_item(source, destination, site_id, drive_id)
