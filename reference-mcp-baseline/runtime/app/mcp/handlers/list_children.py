import requests

HOST = "http://127.0.0.1:8000"

def handle_list_children(site_id: str = "", drive_id: str = "", item_id: str = "", path: str = ""):
    payload = {
        "SiteId": site_id or None,
        "DriveId": drive_id or None,
        "ItemId": item_id or None,
        "ItemPath": path or None,
    }
    resp = requests.post(f"{HOST}/api/list-children", json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()
