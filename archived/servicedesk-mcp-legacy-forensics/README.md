# Archived ServiceDesk MCP Legacy Forensics

This folder contains legacy forensic artifacts from non-canonical ServiceDesk connector attempts.

These artifacts are retained only for historical/debugging context. They must not be used for live connector registration, deployment, or API-key injection.

## Canonical live ServiceDesk connector

Use the root-level file `SERVICEDESK-CANONICAL-LIVE.md`.

Current canonical live endpoint:

```text
https://ca-caberlink-sd-mcp-next.wonderfulfield-3f700329.eastus.azurecontainerapps.io/mcp
```

Current Azure target:

```text
rg-caberlink-write-api-prod / ca-caberlink-sd-mcp-next
```

Current ChatGPT connector registration:

```text
SDP ServiceDesk Tickets
```

## Do not use

Do not use artifacts in this archive if they reference:

- bridge deployments
- backend/frontend split deployments
- App Service deployments
- `azurewebsites.net` ServiceDesk endpoints
- `/openapi.json` ServiceDesk connector registrations
- direct ManageEngine connector registrations pointed at `https://tickets.caberlink.com/api/v3`

## Why this archive exists

The legacy bridge/backend/OpenAPI artifacts caused confusion during API-key rotation and connector recovery. They are archived here so future work starts from the canonical native MCP Container App path.
