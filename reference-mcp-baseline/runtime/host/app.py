import json
import os
import subprocess
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request

APP_ROOT = Path(__file__).resolve().parent.parent
HOST_DIR = APP_ROOT / "host"

with open(HOST_DIR / "host-config.json", "r", encoding="utf-8") as f:
    HOST_CONFIG = json.load(f)

with open(HOST_DIR / "route-map.json", "r", encoding="utf-8") as f:
    ROUTE_MAP = json.load(f)

ROUTES = {r["path"]: r["script"] for r in ROUTE_MAP["routes"]}
PWSH = HOST_CONFIG.get("pwsh_executable", "pwsh")

app = FastAPI(title="CaberLink Write API Host", version="phase1")


def _coerce_arg_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def _run_script(script_rel_path: str, body: dict[str, Any]) -> Any:
    script_path = APP_ROOT / script_rel_path
    if not script_path.exists():
        raise HTTPException(status_code=500, detail=f"Script not found: {script_rel_path}")

    cmd = [PWSH, "-NoProfile", "-File", str(script_path)]

    # inject default SiteUrl if caller omitted it
    if "SiteUrl" not in body and HOST_CONFIG.get("site_url"):
        body = dict(body)
        body["SiteUrl"] = HOST_CONFIG["site_url"]

    for key, value in body.items():
        if value is None:
            continue
        cmd.extend([f"-{key}", _coerce_arg_value(value)])

    proc = subprocess.run(
        cmd,
        cwd=str(APP_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()

    if proc.returncode != 0:
        raise HTTPException(
            status_code=500,
            detail={
                "returncode": proc.returncode,
                "stdout": stdout,
                "stderr": stderr,
                "command": cmd,
            },
        )

    if not stdout:
        return {"ok": True, "stdout": "", "stderr": stderr}

    # Try to parse final JSON object/array from stdout.
    lines = [line for line in stdout.splitlines() if line.strip()]
    for candidate in ("\n".join(lines), lines[-1] if lines else ""):
        try:
            return json.loads(candidate)
        except Exception:
            pass

    return {"ok": True, "stdout": stdout, "stderr": stderr}


@app.get("/healthz")
def healthz() -> dict[str, Any]:
    return {
        "ok": True,
        "service": "caberlink-write-api-host",
        "base_path": ROUTE_MAP.get("health_endpoint", "/healthz"),
    }


@app.post("/{full_path:path}")
async def dispatch(full_path: str, request: Request) -> Any:
    route_path = "/" + full_path
    if route_path not in ROUTES:
        raise HTTPException(status_code=404, detail=f"Unknown route: {route_path}")

    try:
        body = await request.json()
    except Exception:
        body = {}

    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="Request body must be a JSON object.")

    return _run_script(ROUTES[route_path], body)
