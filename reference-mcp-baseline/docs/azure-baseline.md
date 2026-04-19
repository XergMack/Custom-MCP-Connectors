# Azure Baseline

## Purpose

This document captures the exact Azure deployment model of the working reference connector.

It is the main parity anchor for future connectors.

## Reference Connector Azure Model

### Hosting Type

Azure Container App

### Public Base URL

[REPLACE WITH WORKING BASE URL]

### MCP URL

[REPLACE WITH WORKING MCP URL]

### Ingress

- external: true
- target port: 8000

### Registry

[REPLACE WITH ACR LOGIN SERVER / IMAGE NAME]

### Managed Environment

- environment name: [REPLACE]
- environment resource group: [REPLACE]
- environment resource ID: [REPLACE]

### Identity

[REPLACE WITH MANAGED IDENTITY DETAILS]

### Scaling

- min replicas: [REPLACE]
- max replicas: [REPLACE IF USED]

## Runtime Configuration

Capture and pin the exact runtime assumptions:

- public hostname
- target port
- startup command or runtime entrypoint
- environment variables
- secret references
- registry/image digest
- revision strategy

## Transport Security

Document exactly how host validation and origin validation are handled.

This must include:

- whether DNS rebinding protection is enabled or disabled
- allowed hosts, if used
- allowed origins, if used
- whether ingress security is assumed to be enforced elsewhere

## Deployment Model

Document how the reference connector is deployed:

- build tool or script
- image build path
- registry push path
- deployment command
- environment update command
- restart/revision strategy

## Diagnostic Branches

Experimental or divergent deployments must be listed separately and must not be treated as parity baselines until they independently prove full end-to-end parity.
