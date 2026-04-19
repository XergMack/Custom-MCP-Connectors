CaberLink MCP runtime entrypoint

Start command:
python -m app.mcp.server

Environment variables required for local delegated runtime:
CABERLINK_SITE_ID
CABERLINK_DRIVE_ID
CABERLINK_GRAPH_ACCESS_TOKEN

Environment variables used by server bootstrap:
MCP_HOST
MCP_PORT
PORT

Production note:
Local delegated token use is for local validation only.
Final Azure production auth target remains managed identity.
