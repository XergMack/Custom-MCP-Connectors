# Repo Structure Status Map

## Canonical

### `reference-mcp-baseline`
Role: canonical baseline
Status: required
Authority level: highest

### `connector-template-runtime`
Role: reusable connector shell
Status: required for future connector reuse
Authority level: high, but subordinate to baseline doctrine

## Current Live Mirrors

### `servicedesk-mcp-next`
Role: current ServiceDesk live mirror
Status: active
Authority level: production mirror for ServiceDesk

### SharePoint live mirror
Role: current SharePoint live mirror
Status: active
Location: `reference-mcp-baseline`
Authority level: production mirror for SharePoint until explicitly split into its own folder

## Legacy / Forensic

### `servicedesk-mcp`
Role: legacy forensic reference for old ServiceDesk live shape
Status: non-canonical
Authority level: historical only

### `sharepoint-mcp`
Role: legacy planning / forensic material
Status: non-canonical
Authority level: historical only

## Fresh-Thread Rule

When a future thread asks to build or extend a connector, it should not treat all root folders equally.

It should use:
1. canonical baseline
2. template shell
3. current live mirror for the target system
4. legacy material only if specifically needed
