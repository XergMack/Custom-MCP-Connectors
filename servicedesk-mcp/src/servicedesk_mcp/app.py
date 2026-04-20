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

@app.post("/debug/requests/create")
def debug_create_request():
    payload = {
        "request": {
            "subject": "Thin MCP Test Ticket",
            "description": "Created by rebuilt thin ServiceDesk MCP local test.",
            "requester": {"name": "Matt MacKinnon"}
        }
    }
    return asyncio.run(requests_family.create_request(payload))

@app.post("/debug/requests/update/{request_id}")
def debug_update_request(request_id: str):
    payload = {"request": {"subject": "Thin MCP Test Ticket - Updated"}}
    return asyncio.run(requests_family.update_request(request_id, payload))

@app.post("/debug/requests/{request_id}/notes/create")
def debug_create_note(request_id: str):
    payload = {"note": {"description": "Thin MCP test note."}}
    return asyncio.run(notes_family.add_request_note(request_id, payload))

@app.post("/debug/requests/{request_id}/worklogs/create")
def debug_create_worklog(request_id: str):
    payload = {
        "worklog": {
            "description": "Thin MCP test worklog.",
            "time_spent": {
                "hours": "0",
                "minutes": "10"
            }
        }
    }
    return asyncio.run(worklogs_family.add_request_worklog(request_id, payload))

@app.post("/debug/requests/{request_id}/tasks/create")
def debug_create_task(request_id: str):
    payload = {"task": {"title": "Thin MCP test task"}}
    return asyncio.run(tasks_family.add_request_task(request_id, payload))

@app.post("/mcp")
def mcp_placeholder():
    return {"message": "debug routes loaded"}
