from app.mcp.handlers._service import svc
def handle_bulk_move_or_rename_items(items: list[dict], site_id: str = "", drive_id: str = "", continue_on_error: bool = True, verify: bool = True, no_op_behavior: str = "skip"):
    return svc.bulk_move_or_rename_items(items, site_id, drive_id, continue_on_error, verify, no_op_behavior)
