from app.mcp.handlers._service import svc
def handle_create_folder(path: str):
    return svc.create_folder(path)
