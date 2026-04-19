from app.service_core.servicedesk.client import ServiceDeskClient
from app.service_core.servicedesk.config import ServiceDeskSettings


def execute(request_id: str, api_key: str | None = None):
    settings = ServiceDeskSettings.from_env()
    client = ServiceDeskClient(settings=settings, api_key=api_key)
    request_object = client.get_request(request_id=request_id)

    return {
        "id": request_object.get("id"),
        "subject": request_object.get("subject"),
        "status": request_object.get("status"),
        "requester": request_object.get("requester"),
        "technician": request_object.get("technician"),
        "group": request_object.get("group"),
        "site": request_object.get("site"),
        "priority": request_object.get("priority"),
        "template": request_object.get("template"),
        "created_time": request_object.get("created_time"),
        "due_by_time": request_object.get("due_by_time"),
        "description": request_object.get("description"),
        "resolution": request_object.get("resolution"),
        "has_attachments": request_object.get("has_attachments"),
        "raw": request_object,
    }
