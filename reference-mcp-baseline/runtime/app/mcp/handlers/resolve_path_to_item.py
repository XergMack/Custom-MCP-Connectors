from app.mcp.handlers._service import svc
def handle_resolve_path_to_item(path: str):
    return svc.resolve_path_to_item(path)
