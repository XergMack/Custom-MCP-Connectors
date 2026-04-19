# Connector Configuration

## Purpose

This document captures the exact ChatGPT-side connector configuration for the working MCP connector.

This is necessary because the ChatGPT connector UI is part of the end-to-end system, but it is not captured automatically by Azure infrastructure.

## Connector Registration Fields

Record the exact values used in ChatGPT:

### Name

SharePoint Write MCP

### Description

[REPLACE WITH EXACT WORKING DESCRIPTION]

### Authentication Mode

[REPLACE WITH EXACT WORKING AUTH MODE]

### MCP Server URL

https://ca-caberlink-write-api-mcp.wonderfulfield-3f700329.eastus.azurecontainerapps.io/mcp

### MCP Path Shape

The working connector uses:

- `/mcp`

This should be treated as canonical unless later evidence proves otherwise.

## Expected Write Behavior

Document how write-capable tools behave in ChatGPT:

- write-capable custom connector
- confirmation behavior: [REPLACE WITH ACTUAL UX NOTES]
- approval-gating: [REPLACE]
- allowlisted operations should be documented in the tool surface below

## Session Behavior

Document what a successful external MCP initialize looks like.

Capture:

- expected `initialize` result shape
- `mcp-session-id` may be returned by the working endpoint
- follow-up requests should preserve session headers when required by the runtime

## Tool Surface

List the public tools exposed by the working connector.

- get_item_metadata — read — metadata lookup
- create_text_file — write — create content
- update_text_file — write — replace file content
- create_folder — write — create folder
- move_or_rename_item — write — move or rename item
- delete_item — write — delete item
