from app.mcp.handlers._service import svc
def handle_bulk_create_folders(paths: list[str], site_id: str = "", drive_id: str = "", exists_behavior: str = "skip", continue_on_error: bool = True, verify: bool = True):
    return svc.bulk_create_folders(paths, site_id, drive_id, exists_behavior, continue_on_error, verify)
