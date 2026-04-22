from app.mcp.handlers._service import svc

async def handle_health():
    return svc.health()
