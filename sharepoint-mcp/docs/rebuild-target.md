# SharePoint MCP Rebuild Target

## Purpose
Define the target architecture for the SharePoint MCP connector.

## Rebuild Doctrine
- Prefer the thinnest viable architecture
- One service
- One public MCP endpoint
- Managed identity preferred
- Minimal env vars
- Clear documented tool surface
- GitHub must mirror live production exactly

## Live Baseline
- Source of truth: live Azure Container App
- App Name: ca-caberlink-write-api-mcp
- Resource Group: rg-caberlink-write-api-prod
- Environment: cae-caberlink-mcp-prod
- MCP URL: https://ca-caberlink-write-api-mcp.wonderfulfield-3f700329.eastus.azurecontainerapps.io/mcp

## Success Criteria
- GitHub mirrors live SharePoint MCP exactly
- API shape is mapped
- Tool surface is documented
- Future changes are made from repo truth
