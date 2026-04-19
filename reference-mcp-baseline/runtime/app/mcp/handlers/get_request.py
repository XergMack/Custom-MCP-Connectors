from app.service_core.servicedesk.operations.get_request import execute


def handle_get_request(request_id: str, api_key: str | None = None):
    return execute(request_id=request_id, api_key=api_key)
