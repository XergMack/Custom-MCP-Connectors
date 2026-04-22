# Custom MCP Connectors

This repository contains four different kinds of material and they are not all equal.

## Canonical Layers

### 1. `reference-mcp-baseline`
The canonical architecture baseline.

Use this for:
- Azure hosting parity
- MCP runtime parity
- connector doctrine
- validation doctrine
- deployment doctrine
- drift control

### 2. `connector-template-runtime`
The reusable shell for future connectors.

Use this for:
- shared runtime shape
- adapter-only variance model
- future connector bootstrapping

## Current Live Production Mirrors

### 3. `servicedesk-mcp-next`
The current ServiceDesk production mirror.

Use this for:
- current ServiceDesk runtime
- current ServiceDesk Azure deploy plan
- current ServiceDesk evidence
- current ServiceDesk live endpoint state

### 4. SharePoint live mirror
The current SharePoint live production mirror is preserved through `reference-mcp-baseline`.

That baseline contains the mirrored live SharePoint Azure deployment facts and should be treated as the SharePoint production reference until or unless SharePoint is split into its own dedicated live-mirror folder.

## Legacy / Forensic Material

### 5. `servicedesk-mcp`
Legacy forensic and rebuild-reference material.

Do not treat this as the current production mirror.

### 6. `sharepoint-mcp`
Legacy planning / forensic material.

Do not treat this as the canonical current SharePoint production mirror when baseline docs already supersede it.

## Practical Rule For Future Threads

A future thread should orient itself in this order:

1. `reference-mcp-baseline`
2. `connector-template-runtime`
3. the current live mirror for the target system
4. legacy / forensic material only if historical context is needed

## Current Governance Intent

This repository is normalized conceptually as:
- canonical baseline
- reusable template
- live production mirrors
- legacy / forensic material

Physical folder relocation can happen later if desired, but these role assignments are now the source of truth.
