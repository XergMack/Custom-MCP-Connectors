# Architecture

## Objective

Provide a known-good architectural pattern for custom ChatGPT MCP connectors that can be reused for future systems with minimal change.

## Top-Down Flow

ChatGPT  
→ Custom MCP Connector  
→ MCP Runtime hosted in Azure  
→ Backend authority / service core  
→ Target system API

## Boundary Rule

The MCP runtime is a transport and tool-registration layer.

It must remain thin.

Business logic belongs in the service core or backend authority layer, not in the MCP transport layer.

## Design Doctrine

The connector should follow these rules:

- read broadly
- write narrowly
- keep the public tool surface small
- fail closed
- verify writes with read-back where applicable
- preserve auditability

## Canonical Layers

### 1. ChatGPT Connector Layer

This layer contains:

- connector registration in ChatGPT
- connector name
- connector description
- auth mode
- MCP server URL

This layer should be documented explicitly because it is not the same as Azure infrastructure.

### 2. MCP Runtime Layer

This layer contains:

- FastMCP runtime
- MCP transport
- tool registration
- transport security settings
- request/session handling

This layer should not become the business-logic tier.

### 3. Backend Authority Layer

This layer contains:

- service-core implementation
- backend routing/handlers
- target-system request shaping
- auth to the target system
- guardrails for writes

This is the layer that owns the operational truth for the connector.

### 4. Target System Layer

This is the actual external system of record, such as:

- SharePoint / Microsoft Graph
- ServiceDesk
- PSA
- another SaaS/API platform

## Reference Pattern

The reference pattern is the known-good MCP connector deployment that already works in ChatGPT.

Future connectors must start by matching this reference pattern at the runtime and infrastructure level before changing target-system-specific behavior.

## Non-Reference Branches

If an experiment uses a different Azure substrate, startup model, or transport-security model, it must be marked as a diagnostic or experimental branch until it proves full parity.

Examples of non-reference variation include:

- moving from Container Apps to App Service
- changing the runtime entrypoint
- changing startup command shape
- changing MCP path behavior
- changing transport security behavior

## Required Output of Every New Connector Build

Every new connector build must produce:

1. a live MCP endpoint
2. a successful `initialize`
3. a successful `tools/list`
4. at least one real `tools/call`
5. successful ChatGPT connector attachment
