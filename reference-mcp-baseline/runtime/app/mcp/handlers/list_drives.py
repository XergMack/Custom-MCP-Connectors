import requests

HOST = "http://127.0.0.1:8000"

def handle_list_drives(site_id: str = ""):
    payload = {"SiteId": site_id or None}
    resp = requests.post(f"{HOST}/api/list-drives", json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()
