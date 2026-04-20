# ServiceDesk MCP Live Forensics Summary

This folder captures the live Azure ServiceDesk MCP deployment as found in production.

## Live architecture
- Bridge App Service: caberlink-sd-mcp-bridge-260419044455
- Backend App Service: caberlink-sd-mcp-2604181914-7au5
- Bridge forwards to backend via BACKEND_BASE_URL
- Backend runs container image: servicedesk-plus-mcp:v3

## Current assessment
This architecture is more complex than the SharePoint thin baseline.
Treat this as forensic capture of legacy live state, not as the desired future baseline.

## Likely preserve
- SERVICEDESK_BASE_URI
- MCP route/source-root clues
- any proven endpoint contract details

## Likely discard in rebuild
- unnecessary bridge/backend split unless justified
- any mutation guard behavior that cannot be cleanly explained

## Rebuild doctrine
Rebuild ServiceDesk MCP to be as close as possible to the thin SharePoint baseline.
Any deviation must be explicit and justified.
