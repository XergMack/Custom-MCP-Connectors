# ServiceDesk MCP — Archived / Non-Canonical

> **ARCHIVED / NON-CANONICAL**
>
> This directory is legacy forensic and scaffold material. It is **not** the live ServiceDesk connector.
>
> Do not register, deploy, or inject API keys into this path.
>
> Use `servicedesk-mcp-next` and the Azure Container App `ca-caberlink-sd-mcp-next`.

## Canonical live connector

See the root-level file:

- `SERVICEDESK-CANONICAL-LIVE.md`

Current live MCP endpoint:

```text
https://ca-caberlink-sd-mcp-next.wonderfulfield-3f700329.eastus.azurecontainerapps.io/mcp
```

Current ChatGPT connector registration:

```text
SDP ServiceDesk Tickets
```

## Do not use from this tree

Do not use this directory for live registration or key injection. In particular, do not use legacy material referencing:

- bridge deployments
- backend/frontend split deployments
- App Service deployments
- `azurewebsites.net` ServiceDesk endpoints
- `/openapi.json` ServiceDesk connector registrations
- direct ManageEngine connector registrations pointed at `https://tickets.caberlink.com/api/v3`

## Why this remains in the repository

This tree may still contain useful historical implementation notes, API-family scaffolding, and forensic evidence. It is retained only as a reference source for future expansion work.

Any production expansion must be ported deliberately into `servicedesk-mcp-next` and validated against the canonical MCP Container App.
