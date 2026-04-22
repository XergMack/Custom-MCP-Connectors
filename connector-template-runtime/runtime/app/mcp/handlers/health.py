from app.mcp.handlers._service import svc

def handle_health():
    return svc.health()
