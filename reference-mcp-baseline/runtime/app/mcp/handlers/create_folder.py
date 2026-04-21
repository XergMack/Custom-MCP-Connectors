from app.mcp.handlers._service import svc
def handle_create_folder(path: str, site_id: str = "", drive_id: str = ""):
    return svc.create_folder(path, site_id, drive_id)
