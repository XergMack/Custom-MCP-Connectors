# Legacy ServiceDesk App Service Backend Artifact Removed From Active Path

The former active-path file was:

```text
servicedesk-mcp/live-forensics/servicedesk-backend-live.json
```

It described the legacy App Service/OpenAPI backend:

```text
caberlink-sd-mcp-2604181914-7au5.azurewebsites.net
```

That backend is **not** the canonical live ServiceDesk connector.

Canonical live ServiceDesk connector:

```text
https://ca-caberlink-sd-mcp-next.wonderfulfield-3f700329.eastus.azurecontainerapps.io/mcp
```

Canonical Azure target:

```text
rg-caberlink-write-api-prod / ca-caberlink-sd-mcp-next
```

Canonical ChatGPT connector registration:

```text
SDP ServiceDesk Tickets
```

The original JSON remains recoverable from Git history if forensic reconstruction is needed. Do not restore it into an active ServiceDesk path unless it is clearly labeled as non-live legacy evidence.
