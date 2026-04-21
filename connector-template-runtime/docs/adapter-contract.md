# Adapter Contract

Every connector should supply a target adapter or service module that owns business logic.

## Required Responsibilities

- authenticate to the target system
- resolve target entities
- execute read and write operations
- normalize response shape for MCP tools
- keep protocol and runtime concerns out of business logic

## MCP Runtime Must Not Own

- vendor-specific logic
- deep business logic
- target-system policy rules
- data-shaping peculiarities beyond simple response wrapping

## Shared Expectations

- deterministic errors
- explicit verification when possible
- structured outputs for batch operations
- safe defaults
