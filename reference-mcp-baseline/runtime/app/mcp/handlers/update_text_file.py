from app.mcp.handlers._service import svc
def handle_update_text_file(path: str, content: str):
    return svc.update_text_file(path, content)
