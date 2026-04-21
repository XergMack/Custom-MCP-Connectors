# Azure Baseline

## Purpose

This document captures the exact Azure deployment model of the working reference connector.

It is the main parity anchor for future connectors.

## Reference Connector Azure Model

### Hosting Type

Azure Container App

### Public Base URL

https://ca-caberlink-write-api-mcp.wonderfulfield-3f700329.eastus.azurecontainerapps.io

### MCP URL

https://ca-caberlink-write-api-mcp.wonderfulfield-3f700329.eastus.azurecontainerapps.io/mcp

### Ingress

- external: True
- target port: 8000

### Registry

acrcaberlinkwriteapi01.azurecr.io/caberlink-write-api-mcp

### Managed Environment

- environment name: cae-caberlink-mcp-prod
- environment resource group: rg-caberlink-write-api-prod
- environment resource ID: /subscriptions/8eb1dbee-a6f3-44b4-9df4-9766109f1ffa/resourceGroups/rg-caberlink-mcp-prod/providers/Microsoft.App/managedEnvironments/cae-caberlink-mcp-prod

### Identity

SystemAssigned

### Scaling

- min replicas: 1
- max replicas: 10

## Runtime Configuration

Capture and pin the exact runtime assumptions:

- public hostname: ca-caberlink-write-api-mcp.wonderfulfield-3f700329.eastus.azurecontainerapps.io
- target port: 8000
- startup command or runtime entrypoint: python -m app.mcp.server
- environment variables:
  - CABERLINK_SITE_ID -> literal value present
  - CABERLINK_DRIVE_ID -> literal value present
  - CABERLINK_GRAPH_ACCESS_TOKEN
- secret references: documented via env secretRef mappings above and raw JSON evidence in evidence/live-capture
- registry/image: acrcaberlinkwriteapi01.azurecr.io/caberlink-write-api-mcp:mi-fix-01
- latest revision: ca-caberlink-write-api-mcp--0000005
- revision strategy: Azure Container Apps revisions (Multiple)

## Transport Security

Document exactly how host validation and origin validation are handled.

Known working guidance from the reference connector:

- FastMCP transport security handled host-header acceptance
- either explicit Azure hostname allowlisting or DNS rebinding protection disabled
- ingress security was not treated as the only control

### Known Working Hostname

ca-caberlink-write-api-mcp.wonderfulfield-3f700329.eastus.azurecontainerapps.io

## Deployment Model

Document how the reference connector is deployed:

- build tool or script: still needs exact operator command capture
- image build path: still needs exact operator command capture
- registry push path: acrcaberlinkwriteapi01.azurecr.io/caberlink-write-api-mcp
- deployment command: still needs exact operator command capture
- environment update command: still needs exact operator command capture
- restart/revision strategy: Azure Container Apps revision-based rollout (Multiple)

## Diagnostic Branches

Experimental or divergent deployments must be listed separately and must not be treated as parity baselines until they independently prove full end-to-end parity.

### ServiceDesk Diagnostic Branch

A later ServiceDesk bridge experiment used Azure App Service rather than Container Apps and should not be treated as the parity baseline.
