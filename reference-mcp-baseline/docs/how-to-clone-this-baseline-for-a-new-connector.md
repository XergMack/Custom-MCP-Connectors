# How to Clone This Baseline for a New Connector

## Purpose

This document explains how to use the reference MCP baseline to create a new connector with true parity.

The goal is to reuse the proven deployment and runtime pattern while changing only the target-system-specific pieces.

## Golden Rule

Do not redesign the connector unless there is a documented reason.

Start from this baseline and preserve parity first.
Change only what is required for the new target system.

## Read First

Before cloning, read:

- eference-mcp-baseline/docs/architecture.md
- eference-mcp-baseline/docs/azure-baseline.md
- eference-mcp-baseline/docs/canonical-connector-doctrine.md
- eference-mcp-baseline/docs/fresh-thread-handoff-for-next-connector.md
- eference-mcp-baseline/docs/parity-checklist.md
- eference-mcp-baseline/docs/validation.md

## What To Copy Unchanged First

Clone the baseline repository or copy the baseline folder structure as your starting point.

Preserve these areas initially without modification:

- eference-mcp-baseline/docs/architecture.md
- eference-mcp-baseline/docs/azure-baseline.md
- eference-mcp-baseline/docs/canonical-connector-doctrine.md
- eference-mcp-baseline/docs/validation.md
- eference-mcp-baseline/docs/parity-checklist.md
- eference-mcp-baseline/runtime/Dockerfile
- eference-mcp-baseline/runtime/startup-command.txt
- eference-mcp-baseline/infra/ deployment artifacts, unless the Azure environment itself must differ

## What To Replace For A New Connector

Only replace the parts that are specific to the target system.

### 1. Connector Identity

Update:
- connector name
- connector description
- repository/project naming
- target-system references in docs

### 2. Runtime Tool Surface

Update the tool registration and any connector-specific logic.

Primary files:
- eference-mcp-baseline/runtime/app/mcp/tool_registry.py
- any target-system-specific modules added under untime/app/

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

### 5. Tool Evidence

Replace the evidence files with evidence from the new connector once validation is complete.

## What Must Not Change Without Deliberate Review

Do not change these casually:
- Azure hosting substrate
- ingress/public endpoint model
- target port behavior
- runtime entrypoint/startup shape
- transport model
- transport security posture
- validation sequence

Testing posture may remain broad in test connectors, but any production narrowing must be explicit and documented.

## Testing Connector Rule

In testing:
- expose broad read
- expose broad write
- avoid arbitrary family exclusions unless technically impossible
- let human judgment, validation, and deployment discipline provide control

In production later:
- reduce scope intentionally only after testing proves what is useful and reliable

## Recommended Build Sequence For A New Connector

Use this order every time:

1. Clone the baseline
2. Rename only project identity values
3. Replace target-system-specific runtime logic
4. Check official product/API docs for request contracts
5. Update Azure config values
6. Deploy to the same Azure pattern when possible
7. Prove initialize
8. Prove 	ools/list
9. Prove one real safe 	ools/call
10. Attach in ChatGPT
11. Replace evidence files with the new connector's proof

## Minimum Handoff Contents For Any Future Connector

Before treating a new connector as reusable, make sure its repo includes:

- runtime code
- dependency manifest
- Dockerfile
- startup command
- Azure deployment artifacts
- canonical doctrine docs
- validation doc
- parity checklist
- evidence files
- connector-specific tool-surface doc
