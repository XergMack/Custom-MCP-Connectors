# Connector Configuration

## Purpose

This document captures the exact ChatGPT-side connector configuration for the working MCP connector.

This is necessary because the ChatGPT connector UI is part of the end-to-end system, but it is not captured automatically by Azure infrastructure.

## Connector Registration Fields

Record the exact values used in ChatGPT:

### Name

[REPLACE WITH WORKING CONNECTOR NAME]

### Description

[REPLACE WITH WORKING DESCRIPTION]

### Authentication Mode

[REPLACE WITH WORKING AUTH MODE]

### MCP Server URL

[REPLACE WITH EXACT WORKING MCP URL]

### MCP Path Shape

Document whether the working connector uses:

- `/mcp`
- `/mcp/`

and whether redirects are acceptable or should be avoided.

## Expected Write Behavior

Document how write-capable tools behave in ChatGPT:

- whether confirmation is required
- whether the connector is read-only or read/write
- whether writes are approval-gated
- whether any fields are allowlisted

## Session Behavior

Document what a successful external MCP initialize looks like.

Capture:

- expected `initialize` result shape
- whether `mcp-session-id` is returned
- whether follow-up requests must preserve session headers

## Tool Surface

List the public tools exposed by the working connector.

Use this format:

- tool name
- purpose
- read or write
- risk class
- target-system dependency
