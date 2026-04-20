# ServiceDesk MCP Rebuild Target

## Purpose
This document defines the target architecture for the rebuilt ServiceDesk MCP connector.

The goal is to rebuild ServiceDesk MCP to be as thin, understandable, and maintainable as possible, using the live SharePoint MCP as the reference baseline.

## Rebuild Doctrine
- Prefer the thin SharePoint MCP pattern.
- Do not preserve complexity unless it has a clear technical reason.
- GitHub must mirror live production exactly.
- The rebuilt ServiceDesk connector must be easy to explain in one paragraph.
- Any deviation from the SharePoint baseline must be explicit and justified.

## Reference Baseline
Reference connector:
- SharePoint MCP live baseline
- Single Azure Container App
- Single public MCP endpoint
- Managed identity
- Clear ingress and revision model
- GitHub mirrored from live Azure

## Current ServiceDesk Live State
Current live ServiceDesk deployment is a forensic reference only.

Observed live architecture:
- Bridge App Service
- Backend App Service
- Bridge forwards to backend via BACKEND_BASE_URL
- Backend runs container image: servicedesk-plus-mcp:v3

Current assessment:
- More complex than the SharePoint baseline
- Not suitable as the preferred future pattern unless complexity is proven necessary
- Write behavior is currently gated/guarded in a way that is not yet cleanly explained

## Rebuild Target
Target shape:
- One MCP service
- One public MCP endpoint
- No bridge by default
- No separate backend by default
- One clearly documented hosting model
- One clearly documented auth path
- One clearly documented route/tool surface
- GitHub mirrors production exactly

## Preserve from Current ServiceDesk State
Preserve only what is clearly required:
- SERVICEDESK_BASE_URI
- Proven ServiceDesk API/auth method
- Any proven MCP route or tool contract worth keeping
- Any required environment variables that have a clear purpose

## Discard by Default
Discard unless clearly justified:
- Bridge app
- Split bridge/backend architecture
- Mutation guard behavior
- Any unexplained intermediate routing layer
- Any architecture that cannot be justified simply

## Success Criteria
The rebuild is successful when:
- ServiceDesk MCP is explainable simply
- Read and write behavior both work cleanly
- The live Azure deployment is mirrored into GitHub
- The connector follows the same baseline discipline as SharePoint
- Future changes can be made from GitHub without drift

## Next Design Questions
1. What hosting model should the rebuilt ServiceDesk MCP use?
2. What is the minimum auth/config surface required?
3. What tools are required for MVP?
4. What write operations are required for MVP?
5. What exact behavior should replace the current guarded mutation path?

## MVP Bias
Bias toward the smallest working connector that:
- can read ServiceDesk cleanly
- can create/update requests cleanly
- is fully documented
- can be mirrored exactly into GitHub
