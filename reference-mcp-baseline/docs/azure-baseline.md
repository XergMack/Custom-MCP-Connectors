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
- allowInsecure: false
- target port: 8000
- transport: Auto
- active revisions mode: Multiple

### Registry

- registry server: acrcaberlinkwriteapi01.azurecr.io
- reference image: acrcaberlinkwriteapi01.azurecr.io/caberlink-write-api-mcp:mi-fix-01

### Managed Environment

- environment name: cae-caberlink-mcp-prod
- container app resource group: rg-caberlink-write-api-prod
- managed environment resource group: rg-caberlink-mcp-prod
- managed environment resource ID: /subscriptions/8eb1dbee-a6f3-44b4-9df4-9766109f1ffa/resourceGroups/rg-caberlink-mcp-prod/providers/Microsoft.App/managedEnvironments/cae-caberlink-mcp-prod

### Identity

- type: SystemAssigned

### Scaling

- min replicas: 1
- max replicas: 10
- polling interval: 30
- cooldown period: 300

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

- build tool: az acr build
- registry push path: acrcaberlinkwriteapi01.azurecr.io/<connector-image>:<tag>
- deployment substrate: az containerapp create for first deploy, az containerapp update for later revisions
- restart and rollback model: Azure Container Apps revision-based rollout (Multiple)

### Operator Lessons Captured From ServiceDesk Deployment

These are now baseline rules because the ServiceDesk deployment exposed them in practice:

1. Use the full managed environment resource ID when the managed environment lives in a different resource group from the container app.
   - Do not rely on short environment name lookup across resource groups.

2. Keep Azure Container App names under 32 characters and within ACA naming rules.
   - lower case alphanumeric and '-'
   - must start with a letter
   - must end with an alphanumeric character
   - cannot contain '--'
   - must be less than 32 characters

3. First deploy and later deploy are different operations.
   - first deploy: az containerapp create
   - later deploys: az containerapp update
   - do not blindly rerun create after the app exists

4. Smoke-test scripts must be stored as literal script content.
   - do not generate PowerShell scripts with interpolated runtime variables baked into the file body
   - preserve literal variable names in committed artifacts

5. Record the actual successful live endpoint after deploy.
   - FQDN
   - MCP URL
   - healthy revision name
   - successful initialize/tools-list/health evidence

### Required Operator-Specific Deployment Items

These must be documented for each connector before calling it airtight:

- exact az acr build command actually used
- exact first-time az containerapp create command actually used
- exact later az containerapp update command actually used
- exact env-var or secret update command actually used
- exact smoke validation command actually used

## Diagnostic Branches

Experimental or divergent deployments must be listed separately and must not be treated as parity baselines until they independently prove full end-to-end parity.

### ServiceDesk Diagnostic Branch

A later ServiceDesk bridge experiment used Azure App Service rather than Container Apps and should not be treated as the parity baseline.

## Drift Rule

Do not change these casually:

- Azure hosting substrate
- ingress/public endpoint model
- target port behavior
- startup command / runtime entrypoint
- multiple-revision rollout pattern
- managed environment selection method when RGs differ
- baseline validation sequence
