from app.mcp.handlers._service import svc
def handle_move_or_rename_item(source: str, destination: str, site_id: str = "", drive_id: str = ""):
    return svc.move_or_rename_item(source, destination, site_id, drive_id)
