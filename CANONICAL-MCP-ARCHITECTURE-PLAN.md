# Canonical MCP Architecture Plan

## Rule

One canonical MCP connector architecture.
One preserved live reference.
One thin adapter layer per system.

## Repository Roles

- `reference-mcp-baseline/`
  Preserved live SharePoint reference.

- `connector-template-runtime/`
  Canonical reusable runtime, deployment, and validation shell.

- System-specific connectors such as:
  - `servicedesk-mcp-next/`
  - future RMM / PSA / other connectors

## Operating Doctrine

1. Mirror a live connector into GitHub first when one already exists.
2. Preserve the proven runtime and deploy pattern.
3. Pull shared pieces into the canonical template.
4. Change only the target adapter logic per system.

## Next Migration Targets

1. ServiceDesk
2. RMM
3. PSA
4. any future internal system connector
