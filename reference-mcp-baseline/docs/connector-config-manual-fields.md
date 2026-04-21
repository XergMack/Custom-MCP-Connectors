# Connector Config Manual Fields

These values still require manual confirmation from the live ChatGPT connector UI because they are not captured automatically from Azure.

## File To Update
reference-mcp-baseline/docs/connector-config.md

## Manual Fields To Confirm
- Exact working Description
- Exact Authentication Mode
- Exact confirmation behavior for write-capable operations
- Exact approval-gating behavior
- Any initialize/session behavior notes observed in ChatGPT

## Known Values Already Pinned
- Name: SharePoint Write MCP
- MCP Server URL: https://ca-caberlink-write-api-mcp.wonderfulfield-3f700329.eastus.azurecontainerapps.io/mcp
- MCP Path Shape: /mcp

## Suggested Process
1. Open the live SharePoint custom connector in ChatGPT.
2. Copy the exact description text.
3. Confirm the auth mode exactly as shown in the UI.
4. Test one write flow and record the confirmation/approval UX.
5. Update reference-mcp-baseline/docs/connector-config.md with the exact values.
