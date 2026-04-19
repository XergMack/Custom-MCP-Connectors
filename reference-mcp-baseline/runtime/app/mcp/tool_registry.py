from mcp.server.fastmcp import FastMCP

from app.mcp.handlers.get_request import handle_get_request
from app.mcp.handlers.search_requests import handle_search_requests


def register_tools(mcp: FastMCP) -> None:
    @mcp.tool(name="get_request")
    def get_request(request_id: str, api_key: str | None = None):
        return handle_get_request(request_id=request_id, api_key=api_key)

    @mcp.tool(name="search_requests")
    def search_requests(
        row_count: int = 25,
        start_index: int = 1,
        api_key: str | None = None,
    ):
        return handle_search_requests(
            row_count=row_count,
            start_index=start_index,
            api_key=api_key,
        )
