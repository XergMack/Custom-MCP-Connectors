# Canonical MCP Connector Architecture

## Goal

Provide one reusable connector architecture for all CaberLink MCP connectors.

## Layers

### 1. Connector Identity Layer
Per-connector metadata only:
- connector name
- description
- docs naming
- resource naming
- env var names that are target-specific

### 2. MCP Runtime Layer
Shared across all connectors:
- server entrypoint
- transport and session pattern
- tool registration pattern
- handler routing pattern
- Docker and runtime startup model

### 3. Service Core / Adapter Layer
This is the only layer that should substantially differ per connector.

Examples:
- SharePoint graph adapter
- ServiceDesk adapter
- RMM adapter
- PSA adapter

### 4. Deployment Layer
Shared deployment doctrine:
- Azure Container App
- ACR image build and push
- revision-based rollout
- health validation
- rollback by revision

## Rule

Do not redesign the runtime layer per system.

Swap only the adapter layer and identity and config values.
