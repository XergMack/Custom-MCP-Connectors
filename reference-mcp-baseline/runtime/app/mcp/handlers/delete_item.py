from app.mcp.handlers._service import svc
def handle_delete_item(path: str):
    return svc.delete_item(path)
