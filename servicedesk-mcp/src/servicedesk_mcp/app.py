from fastapi import FastAPI
from servicedesk_mcp.core.config import settings

app = FastAPI(title="ServiceDesk MCP", version="0.1.0")

@app.get("/")
def root():
    return {
        "service": "servicedesk-mcp",
        "environment": settings.mcp_env,
        "status": "ok"
    }

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/mcp")
def mcp_placeholder():
    return {
        "message": "MCP endpoint scaffold created",
        "next_step": "Implement tool routing"
    }
