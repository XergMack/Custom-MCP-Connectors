from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Any

from servicedesk_mcp.core.config import settings
from servicedesk_mcp.core.router import call_tool, list_tools

app = FastAPI(title="ServiceDesk MCP", version="0.1.0")

class MCPToolRequest(BaseModel):
    tool_name: str = Field(..., description="Registered tool name")
    arguments: dict[str, Any] = Field(default_factory=dict)

@app.get("/")
def root():
    return {
        "service": "servicedesk-mcp",
        "environment": settings.mcp_env,
        "status": "ok",
    }

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/tools")
def tools():
    return {"families": list_tools()}

@app.post("/mcp")
async def mcp_call(request: MCPToolRequest):
    result = await call_tool(request.tool_name, request.arguments)
    return {
        "ok": True if not (isinstance(result, dict) and result.get("ok") is False) else False,
        "tool_name": request.tool_name,
        "arguments": request.arguments,
        "result": result,
    }
