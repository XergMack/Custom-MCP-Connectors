import json
import os
import subprocess
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="CaberLink Write API Host")

HOST_ROOT = Path(__file__).resolve().parent
APP_ROOT = HOST_ROOT.parent
ROUTES_ROOT = APP_ROOT / "powershell" / "Routes"
AUTH_CONFIG_PATH = APP_ROOT / "config" / "auth-config.certificate.local.json"

class GetItemMetadataRequest(BaseModel):
    ItemPath: str

class CreateTextFileRequest(BaseModel):
    ParentPath: str
    Name: str
    Content: str
    ConflictBehavior: Optional[str] = "fail"
    ContentType: Optional[str] = "text/plain; charset=utf-8"

class UpdateTextFileRequest(BaseModel):
    ItemPath: str
    Content: str
    ContentType: Optional[str] = "text/plain; charset=utf-8"

class CreateFolderRequest(BaseModel):
    ParentPath: str
    Name: str
    ConflictBehavior: Optional[str] = "fail"

class MoveOrRenameItemRequest(BaseModel):
    ItemPath: str
    NewName: Optional[str] = None
    NewParentPath: Optional[str] = None

class DeleteItemRequest(BaseModel):
    ItemPath: str

def run_route(script_name: str, args: list[str]):
    script_path = ROUTES_ROOT / script_name
    if not script_path.exists():
        raise HTTPException(status_code=500, detail=f"Route script not found: {script_path}")

    cmd = [
        "pwsh",
        "-NoProfile",
        "-File",
        str(script_path),
        *args,
    ]

    proc = subprocess.run(
        cmd,
        cwd=str(APP_ROOT),
        capture_output=True,
        text=True,
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
    return {
        "status": "ok",
        "service": "caberlink-write-api-host-python",
        "transport": "http",
        "routesRoot": str(ROUTES_ROOT),
        "authConfigExists": AUTH_CONFIG_PATH.exists(),
    }

@app.post("/api/get-item-metadata")
def get_item_metadata(req: GetItemMetadataRequest):
    return run_route("get-item-metadata.graph.ps1", [
        "-ItemPath", req.ItemPath,
        "-AuthConfigPath", str(AUTH_CONFIG_PATH),
    ])

@app.post("/api/create-text-file")
def create_text_file(req: CreateTextFileRequest):
    return run_route("create-text-file.graph.ps1", [
        "-ParentPath", req.ParentPath,
        "-Name", req.Name,
        "-Content", req.Content,
        "-ConflictBehavior", req.ConflictBehavior or "fail",
        "-ContentType", req.ContentType or "text/plain; charset=utf-8",
        "-AuthConfigPath", str(AUTH_CONFIG_PATH),
    ])

@app.post("/api/update-text-file")
def update_text_file(req: UpdateTextFileRequest):
    return run_route("update-text-file.graph.ps1", [
        "-ItemPath", req.ItemPath,
        "-Content", req.Content,
        "-ContentType", req.ContentType or "text/plain; charset=utf-8",
        "-AuthConfigPath", str(AUTH_CONFIG_PATH),
    ])

@app.post("/api/create-folder")
def create_folder(req: CreateFolderRequest):
    return run_route("create-folder.graph.ps1", [
        "-ParentPath", req.ParentPath,
        "-Name", req.Name,
        "-ConflictBehavior", req.ConflictBehavior or "fail",
        "-AuthConfigPath", str(AUTH_CONFIG_PATH),
    ])

@app.post("/api/move-or-rename-item")
def move_or_rename_item(req: MoveOrRenameItemRequest):
    args = [
        "-ItemPath", req.ItemPath,
        "-AuthConfigPath", str(AUTH_CONFIG_PATH),
    ]
    if req.NewName:
        args += ["-NewName", req.NewName]
    if req.NewParentPath:
        args += ["-NewParentPath", req.NewParentPath]
    return run_route("move-or-rename-item.graph.ps1", args)

@app.post("/api/delete-item")
def delete_item(req: DeleteItemRequest):
    return run_route("delete-item.graph.ps1", [
        "-ItemPath", req.ItemPath,
        "-AuthConfigPath", str(AUTH_CONFIG_PATH),
    ])
