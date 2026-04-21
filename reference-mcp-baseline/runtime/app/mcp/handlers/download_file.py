from app.mcp.handlers._service import svc
def handle_download_file(path: str, site_id: str = "", drive_id: str = ""):
    return svc.download_file(path, site_id, drive_id)
