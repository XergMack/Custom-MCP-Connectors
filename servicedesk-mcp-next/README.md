# ServiceDesk MCP Next

This is the **canonical live ServiceDesk connector**.

It is the target-specific connector intended to inherit the canonical MCP connector architecture.

## Goal

- preserve runtime and deployment parity with the baseline
- implement only ServiceDesk-specific adapter logic
- avoid connector-by-connector architecture drift
- keep the live connector on the thin Azure Container App MCP pattern

## Current live deployment

- ChatGPT connector registration: `SDP ServiceDesk Tickets`
- Azure resource group: `rg-caberlink-write-api-prod`
- Azure Container App: `ca-caberlink-sd-mcp-next`
- MCP endpoint: `https://ca-caberlink-sd-mcp-next.wonderfulfield-3f700329.eastus.azurecontainerapps.io/mcp`
- ServiceDesk base URI: `https://tickets.caberlink.com/api/v3`
- API key env var: `SERVICEDESK_API_KEY`

## Current validation

The live MCP endpoint has been validated with:

- `initialize`: pass
- `notifications/initialized`: pass
- `tools/list`: pass
- `tools/call get_request request_id=111906`: pass
- ChatGPT registered connector `get_request 111906`: pass

## Current tool surface

The registered `SDP ServiceDesk Tickets` connector currently exposes:

- `health`
- `list_requests`
- `get_request`
- `create_request`
- `update_request`
- `create_request_from_context`
- `create_request_for_requester_id`
- `update_request_status`
- `update_request_subject_and_description`
- `list_request_notes`
- `add_request_note`
- `add_request_note_simple`
- `list_request_worklogs`
- `add_request_worklog`
- `list_request_tasks`
- `add_request_task`
- `update_request_task`

## Expansion rule

Future ServiceDesk read/write expansion must happen here, against `servicedesk-mcp-next`, and must be validated against the live Container App before connector registration changes.

Do not use the legacy `servicedesk-mcp` App Service/OpenAPI/bridge material for production registration or key injection.
