# Validation

## Purpose

This document defines the minimum proof required before a connector can be called working.

No connector should be treated as production-ready until all validation checks pass.

## Validation Sequence

### 1. Runtime Reachability

Confirm the public MCP URL is reachable from outside Azure.

Record:

- URL tested
- timestamp
- status code
- whether `/mcp` or `/mcp/` is canonical

### 2. MCP Initialize

Send a valid `initialize` request.

Success criteria:

- HTTP 200
- valid JSON-RPC response
- expected protocol version returned
- expected server info present
- session header behavior recorded

Store the full successful response in `evidence/initialize-response.json`.

### 3. MCP Tools List

Send `tools/list` after proper initialization/session handling.

Success criteria:

- HTTP 200
- expected tool list present
- no missing required tools
- schema shape looks correct

Store the full successful response in `evidence/tools-list-response.json`.

### 4. Real Tool Call

Call at least one real tool against the live backend authority.

Prefer a safe read tool first.

Success criteria:

- HTTP 200
- response is operationally valid
- result matches backend authority expectations

Store the response in `evidence/sample-tool-call.json`.

### 5. ChatGPT Connector Attachment

Register or attach the connector in ChatGPT.

Success criteria:

- connector accepts the MCP URL
- ChatGPT can enumerate tools
- at least one tool can be invoked from ChatGPT successfully

## Failure Classification

If validation fails, classify the failure as one of:

- infrastructure
- startup/runtime
- transport security
- MCP protocol/session
- backend authority
- target-system auth
- ChatGPT connector registration
