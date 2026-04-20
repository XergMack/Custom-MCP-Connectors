# ServiceDesk MCP Rebuild Target

## Purpose
Define the target architecture for the rebuilt ServiceDesk MCP connector.

## Rebuild Doctrine
- Prefer the thin SharePoint MCP pattern
- One Azure Container App
- One public MCP endpoint
- No bridge by default
- No split backend/frontend by default
- Minimal env vars
- Clear auth path
- Clear documented tool surface
- GitHub must mirror live production exactly

## Reference Baseline
Reference connector:
- SharePoint MCP live baseline
- Single Azure Container App
- Single public MCP endpoint
- Managed identity
- Clear ingress and revision model
- GitHub mirrored from live Azure

## Current ServiceDesk Live State
Observed live architecture:
- Bridge App Service
- Backend App Service
- Bridge forwards to backend via BACKEND_BASE_URL
- Backend runs container image: servicedesk-plus-mcp:v3

## Assessment
- More complex than the SharePoint baseline
- Treat current ServiceDesk live state as forensic reference, not desired future architecture
- Rebuild thin unless extra complexity is explicitly justified

## Preserve from Current ServiceDesk State
- SERVICEDESK_BASE_URI
- Proven ServiceDesk API/auth method
- Any proven route/tool contract worth keeping
- Any required environment variables with clear purpose

## Discard by Default
- Bridge app
- Split bridge/backend architecture
- Mutation guard behavior
- Any unexplained routing layer

## Success Criteria
- Simple architecture
- Clean read/write behavior
- Live Azure mirrored into GitHub
- Same baseline discipline as SharePoint

## MVP Bias
Bias toward the smallest working connector that:
- can read ServiceDesk cleanly
- can write ServiceDesk cleanly
- is fully documented
- can be mirrored exactly into GitHub
