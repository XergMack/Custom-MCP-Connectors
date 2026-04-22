# Build Doctrine

## Core Rule

One canonical MCP connector architecture.
One preserved live reference.
One thin adapter layer per system.

## Adapter-Only Variance

Do not redesign the runtime shell for each connector.

Change only:
- target system auth/config
- target system request/response shaping
- target-specific tool surface
- service-core logic for that target system

## Mirror First

If a live connector already exists, mirror it into GitHub first.

## Abstract Second

Once mirrored, pull shared runtime, deploy, and validation patterns into the template runtime.

## Specialize Third

New connectors should implement only:
- target system config
- target system adapter/service logic
- tool definitions
- validation evidence

## Testing Connector Doctrine

In testing:
- full read
- full write
- broad family coverage
- no arbitrary family exclusions unless technically impossible

Production narrowing comes later only if explicitly chosen.

## Anti-Pattern

Do not start each connector by inventing a new runtime shell.
