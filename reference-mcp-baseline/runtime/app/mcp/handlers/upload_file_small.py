from app.mcp.handlers._service import svc
def handle_upload_file_small(path: str, content_b64: str, conflict: str = "replace"):
    return svc.upload_file_small(path, content_b64, conflict)
