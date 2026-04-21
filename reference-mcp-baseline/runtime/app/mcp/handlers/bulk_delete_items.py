from app.mcp.handlers._service import svc
def handle_bulk_delete_items(paths: list[str], site_id: str = "", drive_id: str = "", missing_behavior: str = "skip", continue_on_error: bool = True, verify: bool = True):
    return svc.bulk_delete_items(paths, site_id, drive_id, missing_behavior, continue_on_error, verify)
