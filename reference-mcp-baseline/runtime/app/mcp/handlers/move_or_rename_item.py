from app.mcp.handlers._service import svc
def handle_move_or_rename_item(source: str, destination: str):
    return svc.move_or_rename_item(source, destination)
