# SharePoint MCP Live Baseline Summary

Source of truth: live Azure Container App

App Name: ca-caberlink-write-api-mcp
Resource Group: rg-caberlink-write-api-prod
Environment: cae-caberlink-mcp-prod
FQDN: ca-caberlink-write-api-mcp.wonderfulfield-3f700329.eastus.azurecontainerapps.io
MCP URL: https://ca-caberlink-write-api-mcp.wonderfulfield-3f700329.eastus.azurecontainerapps.io/mcp

Active Revision: ca-caberlink-write-api-mcp--0000005
Image: acrcaberlinkwriteapi01.azurecr.io/caberlink-write-api-mcp:mi-fix-01

Identity:
- System-assigned managed identity enabled

Environment Variables:
- CABERLINK_SITE_ID
- CABERLINK_DRIVE_ID
- CABERLINK_GRAPH_ACCESS_TOKEN (blank in live config)

Scale:
- minReplicas: 1
- maxReplicas: 10

Doctrine:
This live Azure definition is the canonical SharePoint MCP baseline.
GitHub must mirror this live state exactly before any further baseline abstraction or reuse work.
