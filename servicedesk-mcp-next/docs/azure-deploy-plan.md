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

## Actual Successful Azure Deployment Values
- container app name: ca-caberlink-sd-mcp-next
- container app resource group: rg-caberlink-write-api-prod
- managed environment resource ID: /subscriptions/8eb1dbee-a6f3-44b4-9df4-9766109f1ffa/resourceGroups/rg-caberlink-mcp-prod/providers/Microsoft.App/managedEnvironments/cae-caberlink-mcp-prod
- image: acrcaberlinkwriteapi01.azurecr.io/caberlink-servicedesk-mcp-next:test-3aa274a-20260422045933
- live FQDN: ca-caberlink-sd-mcp-next.wonderfulfield-3f700329.eastus.azurecontainerapps.io
- live MCP URL: https://ca-caberlink-sd-mcp-next.wonderfulfield-3f700329.eastus.azurecontainerapps.io/mcp
- healthy revision: ca-caberlink-sd-mcp-next--0000001

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

## Validated After Deploy
- initialize against live ACA endpoint
- tools/list against live ACA endpoint
- health against live ACA endpoint
- custom connector attached in ChatGPT
- list_requests returned live ServiceDesk data through the deployed connector

## Known Remaining Gap
- note create endpoint still requires final payload/auth alignment
- note read works
- request lifecycle is deployable now

## Operator Rules From Actual Deploy
1. Use the full managed environment resource ID, not just the short environment name, because the managed environment lives in a different resource group from the container app.
2. Keep the container app name under Azure's ACA naming limits.
3. First deploy uses az containerapp create.
4. Later revisions should use az containerapp update.
5. Do not treat a malformed checked-in smoke script as deploy-ready just because a manual in-session recovery worked.

## Rollback Model
- revision-based rollback in Azure Container Apps
