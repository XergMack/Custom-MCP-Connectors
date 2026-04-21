# Validation Refresh - Next Steps

The validation sequence is already defined in:
reference-mcp-baseline/docs/validation.md

The following artifacts should now be refreshed from the LIVE SharePoint MCP endpoint:

- evidence/initialize-response.json
- evidence/tools-list-response.json
- evidence/sample-tool-call.json

Recommended order:
1. Validate runtime reachability for:
   https://ca-caberlink-write-api-mcp.wonderfulfield-3f700329.eastus.azurecontainerapps.io/mcp
2. Run initialize and store full response
3. Run tools/list and store full response
4. Run one safe real tool call and store full response
5. Confirm ChatGPT connector attachment still works

Live capture for this pass is stored under:
reference-mcp-baseline/evidence/live-capture
