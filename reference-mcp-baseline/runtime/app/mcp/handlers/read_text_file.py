from app.mcp.handlers._service import svc
def handle_read_text_file(path: str):
    return svc.read_text_file(path)
