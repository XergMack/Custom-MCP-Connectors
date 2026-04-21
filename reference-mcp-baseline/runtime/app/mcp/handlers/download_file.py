from app.mcp.handlers._service import svc
def handle_download_file(path: str):
    return svc.download_file(path)
