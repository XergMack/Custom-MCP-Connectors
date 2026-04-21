from app.mcp.handlers._service import svc
def handle_update_text_file(path: str, content: str, site_id: str = "", drive_id: str = ""):
    return svc.update_text_file(path, content, site_id, drive_id)
