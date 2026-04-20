# Connector Rebuild Target

## Purpose
Define the target architecture for a rebuilt connector.

## Rebuild Doctrine
- Prefer the thinnest viable architecture
- One service by default
- One public MCP endpoint by default
- No extra layers unless justified
- Minimal env vars
- Clear auth path
- Clear documented tool surface
- GitHub must mirror live production exactly

## Preserve from Current State
- only what is clearly required
- proven auth/config
- proven endpoint/tool contracts

## Discard by Default
- unexplained layers
- unexplained guards
- any architecture that cannot be justified simply

## Success Criteria
- simple architecture
- clean read/write behavior
- live deployment mirrored into GitHub
- deterministic, documented tool behavior
