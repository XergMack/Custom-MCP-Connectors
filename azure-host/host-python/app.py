import json
import os
import subprocess
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="MCP Connector Host")

ROUTES_ROOT = Path(
    os.getenv("MCP_ROUTES_ROOT", "/service/powershell/Routes")
).resolve()

SRC_ROOT = Path(
    os.getenv("MCP_SRC_ROOT", "/service/src/QuickBooksOnline.Mcp")
).resolve()


class EmptyRequest(BaseModel):
    pass


class GetItemRequest(BaseModel):
    item_id: str


class SearchItemsRequest(BaseModel):
    page: Optional[int] = 1
    page_size: Optional[int] = 25
    search_fields: Optional[dict[str, Any]] = None


class CreateItemRequest(BaseModel):
    name: str
    description: Optional[str] = None


class UpdateItemRequest(BaseModel):
    item_id: str
    fields: dict[str, Any]


def run_route(script_name: str, payload: dict[str, Any]):
    script_path = ROUTES_ROOT / script_name
    if not script_path.exists():
        raise HTTPException(status_code=500, detail=f"Route script not found: {script_path}")

    env = os.environ.copy()
    env["MCP_SRC_ROOT"] = str(SRC_ROOT)

    cmd = [
        "pwsh",
        "-NoProfile",
        "-File",
        str(script_path),
        "-JsonPayload",
        json.dumps(payload),
    ]

    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=env,
    )

    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()

    if proc.returncode != 0:
        raise HTTPException(status_code=500, detail=stderr or stdout or "Route execution failed")

    if not stdout:
        return {"ok": True, "route": script_name}

    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return {"raw_output": stdout}


@app.get("/healthz")
def healthz():
    connector_auth_mode = os.getenv("CONNECTOR_AUTH_MODE", "QuickBooksOAuth")

    return {
        "status": "ok",
        "service": "mcp-connector-host",
        "transport": "http",
        "routesRoot": str(ROUTES_ROOT),
        "srcRoot": str(SRC_ROOT),
        "connectorAuthMode": connector_auth_mode,
        "baseUriConfigured": bool(os.getenv("CONNECTOR_BASE_URI")),
        "apiKeyConfigured": bool(os.getenv("CONNECTOR_API_KEY")),
        "qboClientIdConfigured": bool(os.getenv("QBO_CLIENT_ID")),
        "qboClientSecretConfigured": bool(os.getenv("QBO_CLIENT_SECRET")),
        "qboRefreshTokenConfigured": bool(os.getenv("QBO_REFRESH_TOKEN")),
        "qboRealmIdConfigured": bool(os.getenv("QBO_REALM_ID")),
        "qboEnvironment": os.getenv("QBO_ENVIRONMENT", "Production"),
    }


@app.post("/api/get-company-info")
def get_company_info(req: EmptyRequest):
    return run_route("get-company-info.ps1", req.model_dump())


@app.post("/api/get-item")
def get_item(req: GetItemRequest):
    return run_route("get-item.ps1", req.model_dump())


@app.post("/api/search-items")
def search_items(req: SearchItemsRequest):
    return run_route("search-items.ps1", req.model_dump())


@app.post("/api/create-item")
def create_item(req: CreateItemRequest):
    return run_route("create-item.ps1", req.model_dump())


@app.post("/api/update-item")
def update_item(req: UpdateItemRequest):
    return run_route("update-item.ps1", req.model_dump())
