# ServiceDesk MCP Next Azure Deploy Plan

## Container Runtime
- Build from servicedesk-mcp-next/runtime
- Docker entrypoint: python -m app.mcp.server
- Expose port 8000
- Streamable HTTP endpoint: /mcp

## Required Environment Variables
- SERVICEDESK_BASE_URI
- SERVICEDESK_API_KEY
- MCP_HOST=0.0.0.0
- PORT=8000
- MCP_ENV=prod
- MCP_LOG_LEVEL=INFO

## Validation Order
1. initialize
2. tools/list
3. health
4. list_requests
5. create_request_for_requester_id in test tenant only

## Rollback Model
- revision-based rollback in Azure Container Apps
