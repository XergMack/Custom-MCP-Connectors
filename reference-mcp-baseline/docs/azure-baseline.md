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

- external: true
- target port: 8000

### Registry

acrcaberlinkwriteapi01.azurecr.io/caberlink-write-api-mcp

### Managed Environment

- environment name: cae-caberlink-mcp-prod
- environment resource group: rg-caberlink-mcp-prod
- environment resource ID: /subscriptions/8eb1dbee-a6f3-44b4-9df4-9766109f1ffa/resourceGroups/rg-caberlink-mcp-prod/providers/Microsoft.App/managedEnvironments/cae-caberlink-mcp-prod

### Identity

Managed identity enabled in production deployment. Exact identity assignment and usage should be documented here once exported from Azure.

### Scaling

- min replicas: [REPLACE WITH ACTUAL VALUE]
- max replicas: [REPLACE IF USED]

## Runtime Configuration

Capture and pin the exact runtime assumptions:

- public hostname: ca-caberlink-write-api-mcp.wonderfulfield-3f700329.eastus.azurecontainerapps.io
- target port: 8000
- startup command or runtime entrypoint: python -m app.mcp.server
- environment variables: [REPLACE WITH ACTUAL WORKING SET]
- secret references: [REPLACE WITH ACTUAL WORKING SET]
- registry/image digest: [REPLACE WITH DIGEST IF AVAILABLE]
- revision strategy: Container Apps revisions

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

- build tool or script: [REPLACE]
- image build path: [REPLACE]
- registry push path: acrcaberlinkwriteapi01.azurecr.io/caberlink-write-api-mcp
- deployment command: [REPLACE]
- environment update command: [REPLACE]
- restart/revision strategy: Azure Container Apps revision-based rollout

## Diagnostic Branches

Experimental or divergent deployments must be listed separately and must not be treated as parity baselines until they independently prove full end-to-end parity.

### ServiceDesk Diagnostic Branch

A later ServiceDesk bridge experiment used Azure App Service rather than Container Apps and should not be treated as the parity baseline.
