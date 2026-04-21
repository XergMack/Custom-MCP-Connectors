from app.mcp.handlers._service import svc
def handle_read_text_file(path: str, site_id: str = "", drive_id: str = ""):
    return svc.read_text_file(path, site_id, drive_id)
