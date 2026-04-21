from app.mcp.handlers._service import svc
def handle_list_drives(site_id: str = ""):
    return svc.list_drives(site_id)
