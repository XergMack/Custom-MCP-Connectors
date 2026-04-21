import os
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from app.mcp.tool_registry import register_tools

mcp = FastMCP(
    "connector-template-runtime",
    json_response=True,
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False
    ),
)

register_tools(mcp)

if __name__ == "__main__":
    host = os.environ.get("MCP_HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", os.environ.get("MCP_PORT", "8000")))
    mcp.settings.host = host
    mcp.settings.port = port
    mcp.run(transport="streamable-http")
