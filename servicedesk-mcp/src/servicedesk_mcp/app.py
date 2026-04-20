from fastapi import FastAPI
from servicedesk_mcp.core.config import settings
from servicedesk_mcp.families import requests as requests_family
from servicedesk_mcp.families import notes as notes_family
from servicedesk_mcp.families import worklogs as worklogs_family
from servicedesk_mcp.families import tasks as tasks_family
import asyncio

app = FastAPI(title="ServiceDesk MCP", version="0.1.0")

@app.get("/")
def root():
    return {"service": "servicedesk-mcp", "environment": settings.mcp_env, "status": "ok"}

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/tools")
def tools():
    return {
        "families": {
            "requests": requests_family.register_tools(),
            "notes": notes_family.register_tools(),
            "worklogs": worklogs_family.register_tools(),
            "tasks": tasks_family.register_tools(),
        }
    }

@app.get("/debug/requests")
def debug_requests():
    return asyncio.run(requests_family.list_requests())

@app.get("/debug/requests/assigned-to-me")
def debug_requests_assigned_to_me():
    return asyncio.run(
        requests_family.search_requests(
            technician_name="Matthew MacKinnon",
            status_name="Open",
            start_index=1,
            row_count=100
        )
    )
