import requests

HOST = "http://127.0.0.1:8000"

def handle_resolve_path_to_item(path: str, site_id: str = "", drive_id: str = ""):
    payload = {
        "ItemPath": path,
        "SiteId": site_id or None,
        "DriveId": drive_id or None,
    }
    resp = requests.post(f"{HOST}/api/resolve-path-to-item", json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()
