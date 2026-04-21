from app.mcp.handlers._service import svc
def handle_list_children(path: str = ""):
    return svc.list_children(path)
