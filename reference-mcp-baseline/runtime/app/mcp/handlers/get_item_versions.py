from app.mcp.handlers._service import svc
def handle_get_item_versions(path: str):
    return svc.get_item_versions(path)
