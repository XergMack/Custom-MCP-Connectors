from app.mcp.handlers._service import svc
def handle_create_text_file(path: str, content: str, conflict: str = "fail", site_id: str = "", drive_id: str = ""):
    return svc.create_text_file(path, content, conflict, site_id, drive_id)
