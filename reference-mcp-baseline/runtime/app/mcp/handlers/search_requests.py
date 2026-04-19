from app.service_core.servicedesk.operations.search_requests import execute


def handle_search_requests(
    row_count: int = 25,
    start_index: int = 1,
    api_key: str | None = None,
):
    return execute(
        row_count=row_count,
        start_index=start_index,
        api_key=api_key,
    )
