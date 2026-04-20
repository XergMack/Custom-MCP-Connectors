from fastapi import FastAPI
from servicedesk_mcp.core.config import settings
from servicedesk_mcp.families import requests as requests_family

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

@app.get("/tools")
def tools():
    return {
        "families": {
            "requests": requests_family.register_tools()
        }
    }

@app.post("/mcp")
def mcp_placeholder():
    return {
        "message": "Requests family implemented first",
        "tools": requests_family.register_tools(),
        "next_step": "Implement notes, worklogs, and tasks"
    }
