# ServiceDesk Canonical Live Connector

## Current live connector

The canonical live ServiceDesk connector is:

- Connector registration name: `SDP ServiceDesk Tickets`
- Azure resource group: `rg-caberlink-write-api-prod`
- Azure Container App: `ca-caberlink-sd-mcp-next`
- MCP endpoint: `https://ca-caberlink-sd-mcp-next.wonderfulfield-3f700329.eastus.azurecontainerapps.io/mcp`
- Protocol: native MCP
- Runtime family: canonical thin Azure Container App MCP pattern

## Do not use

The following are legacy, forensic, or non-canonical ServiceDesk references and must not be used for live connector registration or API-key injection:

- `servicedesk-mcp` bridge references
- `servicedesk-mcp` backend references
- `azurewebsites.net` OpenAPI/App Service references
- `/openapi.json` ServiceDesk connector registrations
- any direct ManageEngine connector registration pointing at `https://tickets.caberlink.com/api/v3`

## API key location

The active ServiceDesk API key belongs on:

- Azure Container App: `ca-caberlink-sd-mcp-next`
- Environment variable: `SERVICEDESK_API_KEY`
- Base URI variable: `SERVICEDESK_BASE_URI=https://tickets.caberlink.com/api/v3`

Do not inject the ServiceDesk key into legacy App Service/OpenAPI deployments.

## Current validation

The live MCP endpoint has been validated with:

- `initialize`: pass
- `notifications/initialized`: pass
- `tools/list`: pass
- `tools/call get_request request_id=111906`: pass
- ChatGPT registered connector `get_request 111906`: pass

## Current exposed ChatGPT connector tools

The registered `SDP ServiceDesk Tickets` connector currently exposes request-focused read/write tooling:

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

## Expansion target

Future ServiceDesk expansion work must be performed against `servicedesk-mcp-next` and the Container App `ca-caberlink-sd-mcp-next`, not the legacy App Service/OpenAPI fallback.
