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

## Validated Before Deploy
- initialize
- tools/list
- health
- list_requests
- get_request
- create_request
- create_request_for_requester_id
- update_request_subject_and_description
- update_request_status

## Known Remaining Gap
- note create endpoint still requires final payload/auth alignment
- note read works
- request lifecycle is deployable now

## Rollback Model
- revision-based rollback in Azure Container Apps
