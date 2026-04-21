from app.mcp.handlers._service import svc
def handle_copy_item(source: str, destination: str):
    return svc.copy_item(source, destination)
