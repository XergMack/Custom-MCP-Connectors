# Fresh-Thread Handoff For The Next Connector

## Purpose

Use this document when starting a new connector build in a fresh thread.

Examples:
- QuickBooks connector
- RMM connector
- PSA connector
- ServiceNow connector
- any future SaaS/API connector

## Instruction To The Future Thread

Use the SharePoint MCP live baseline as the canonical architecture baseline.

Do not redesign the Azure or MCP runtime architecture unless a deviation is explicitly justified.

## Required Assumptions

Assume the following by default:
- one Azure Container App
- one public MCP endpoint
- target port 8000 unless documented otherwise
- startup command shape matches baseline
- runtime remains thin
- service-core/adapter owns target-system-specific logic
- GitHub is source of truth
- validation must prove initialize, tools/list, and one real tools/call
- evidence must be stored in repo

## Connector Build Order

1. Read:
   - reference-mcp-baseline/README.md
   - reference-mcp-baseline/docs/architecture.md
   - reference-mcp-baseline/docs/azure-baseline.md
   - reference-mcp-baseline/docs/canonical-connector-doctrine.md
   - reference-mcp-baseline/docs/how-to-clone-this-baseline-for-a-new-connector.md
   - reference-mcp-baseline/docs/parity-checklist.md
   - reference-mcp-baseline/docs/validation.md

2. Copy baseline shape first

3. Change only:
   - connector identity
   - target system auth/config
   - target system adapter/service-core
   - target-specific tool surface
   - connector-specific deploy values

4. Check official product/API docs before finalizing request contracts

5. Validate locally

6. Deploy to the same Azure pattern when possible

7. Replace evidence with new connector proof

## Required Repo Outputs

Before saying a connector is ready, GitHub should contain:
- runtime code
- requirements/dependency manifest
- Dockerfile
- startup command
- Azure deploy notes/artifacts
- connector doctrine
- connector config notes
- validation doc
- parity checklist
- evidence files
- connector-specific tool-surface doc

## Testing Posture

In test:
- expose broad read
- expose broad write
- include all practical API families
- use human judgment, not arbitrary connector crippling, as the control surface

In production later:
- reduce scope intentionally if needed
