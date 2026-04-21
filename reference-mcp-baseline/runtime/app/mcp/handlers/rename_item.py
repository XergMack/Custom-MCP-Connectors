from app.mcp.handlers._service import svc
def handle_rename_item(path: str, new_name: str):
    return svc.rename_item(path, new_name)
