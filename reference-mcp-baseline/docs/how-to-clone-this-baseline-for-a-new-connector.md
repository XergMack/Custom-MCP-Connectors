# How to Clone This Baseline for a New Connector

## Purpose

This document explains how to use the reference MCP baseline to create a new connector with true parity.

The goal is to reuse the proven deployment and runtime pattern while changing only the target-system-specific pieces.

## Golden Rule

Do not redesign the connector unless there is a documented reason.

Start from this baseline and preserve parity first.
Change only what is required for the new target system.

## What To Copy Unchanged First

Clone the baseline repository or copy the baseline folder structure as your starting point.

Preserve these areas initially without modification:

- `reference-mcp-baseline/docs/architecture.md`
- `reference-mcp-baseline/docs/validation.md`
- `reference-mcp-baseline/docs/parity-checklist.md`
- `reference-mcp-baseline/runtime/Dockerfile`
- `reference-mcp-baseline/runtime/startup-command.txt`
- `reference-mcp-baseline/infra/` deployment artifacts, unless the Azure environment itself must differ

## What To Replace For A New Connector

Only replace the parts that are specific to the target system.

### 1. Connector Identity

Update:

- connector name
- connector description
- repository/project naming
- target-system references in docs

Primary file:

- `reference-mcp-baseline/docs/connector-config.md`

### 2. Runtime Tool Surface

Update the tool registration and any connector-specific logic.

Primary files:

- `reference-mcp-baseline/runtime/app/mcp/tool_registry.py`
- any target-system-specific modules added under `runtime/app/`

Keep the MCP runtime thin.

### 3. Backend Authority Or Service Core

If the connector uses a backend/service-core model, update only the system-specific logic there.

Do not move business logic into the MCP transport layer.

### 4. Configuration Values

Update only the values that must change, such as:

- backend base URL
- vendor API endpoints
- auth settings
- managed identity usage
- registry/image names
- Azure resource names
- environment-specific secrets/config

Primary files:

- `reference-mcp-baseline/docs/azure-baseline.md`
- `reference-mcp-baseline/infra/*`
- runtime env var handling

### 5. Tool Evidence

Replace the evidence files with evidence from the new connector once validation is complete.

Primary files:

- `reference-mcp-baseline/evidence/initialize-response.json`
- `reference-mcp-baseline/evidence/tools-list-response.json`
- `reference-mcp-baseline/evidence/sample-tool-call.json`
- `reference-mcp-baseline/evidence/working-endpoint.txt`

## What Must Not Change Without Deliberate Review

Do not change these casually:

- Azure hosting substrate
- ingress/public endpoint model
- target port behavior
- runtime entrypoint/startup shape
- transport model
- transport security posture
- validation sequence
- write-safety posture

Any change to one of those must be documented explicitly in:

- `reference-mcp-baseline/docs/azure-baseline.md`
- `reference-mcp-baseline/docs/parity-checklist.md`

## Recommended Build Sequence For A New Connector

Use this order every time:

1. Clone the baseline
2. Rename only project identity values
3. Replace target-system-specific runtime logic
4. Update Azure config values
5. Deploy to the same Azure pattern when possible
6. Prove `initialize`
7. Prove `tools/list`
8. Prove one safe real `tools/call`
9. Attach in ChatGPT
10. Replace evidence files with the new connector's proof

## Validation Standard

A connector is not “at parity” because the code looks similar.

It is only at parity when:

- the deployment model matches where intended
- the runtime model matches where intended
- the connector config matches where intended
- the validation artifacts prove real end-to-end behavior

## Minimum Handoff Contents For Any Future Connector

Before treating a new connector as reusable, make sure its repo includes:

- runtime code
- dependency manifest
- Dockerfile or startup command
- Azure deployment artifacts
- connector configuration doc
- validation doc
- parity checklist
- evidence files

## Practical Rule

Keep the baseline boring.

The baseline should optimize for:

- repeatability
- auditability
- minimal surprise
- minimal reinvention

If a new connector needs innovation, prove parity first, then document the deviation.
