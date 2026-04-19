from app.service_core.servicedesk.client import ServiceDeskClient
from app.service_core.servicedesk.config import ServiceDeskSettings


def execute(
    row_count: int = 25,
    start_index: int = 1,
    api_key: str | None = None,
):
    settings = ServiceDeskSettings.from_env()
    client = ServiceDeskClient(settings=settings, api_key=api_key)
    return client.search_requests(
        row_count=row_count,
        start_index=start_index,
    )
