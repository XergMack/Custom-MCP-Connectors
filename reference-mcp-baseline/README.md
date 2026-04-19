# MCP Connector Reference Baseline

This folder is the canonical baseline for building custom ChatGPT MCP connectors with true parity.

It exists so future connectors can be created by changing only project-specific pieces, rather than redesigning infrastructure, runtime behavior, validation, and deployment from scratch.

## Purpose

This baseline captures four layers together:

1. runtime code
2. Azure deployment pattern
3. ChatGPT connector configuration
4. validation evidence

## Golden Rule

GitHub is the source of truth.

Azure is the running instance.
This baseline is the reproducible blueprint.

## What Must Be Preserved

The baseline must preserve the parts that define runtime parity:

- hosting substrate
- ingress/public endpoint pattern
- target port
- startup command / entrypoint
- environment variable model
- identity/auth model
- MCP transport model
- transport security model
- validation sequence
- ChatGPT connector configuration

## What Future Connectors May Change

Future connectors may change only the target-system-specific parts, such as:

- connector name
- description
- backend target URL
- tool names and schemas
- service-core implementation
- secrets and auth specifics for the target system

## Repository Layout

- `docs/architecture.md` — top-down system design
- `docs/azure-baseline.md` — exact Azure runtime and deployment model
- `docs/connector-config.md` — exact ChatGPT connector settings
- `docs/validation.md` — deployment validation sequence
- `docs/parity-checklist.md` — required parity checks before calling a new connector aligned
- `runtime/` — MCP runtime code and runtime dependencies
- `infra/` — IaC and deployment scripts
- `evidence/` — captured working responses and operator evidence

## Status Model

This baseline should always distinguish between:

- **Reference baseline** — the known-good production pattern
- **Experimental branches** — alternative runtime or hosting attempts
- **Diagnostic history** — evidence gathered while debugging regressions

Only the reference baseline is allowed to define parity.
