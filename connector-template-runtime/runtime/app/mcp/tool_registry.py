from mcp.server.fastmcp import FastMCP
from app.mcp.handlers.health import handle_health

def register_tools(mcp: FastMCP):
    @mcp.tool(name="health")
    def health():
        return handle_health()
