# Canonical Connector Doctrine

## Purpose

This document defines the non-negotiable doctrine for all CaberLink MCP connectors.

It exists so a future thread can build the next connector without re-deriving intent.

## Core Rule

One canonical MCP connector architecture.
One preserved live reference baseline.
One thin adapter layer per target system.

## Adapter-Only Variance Rule

The only expected connector-specific variance should be:
- target system auth/config
- target system API request/response shaping
- tool names and schemas required for that target system
- service-core logic that speaks to that target system

Everything else should match baseline unless a deviation is explicitly approved.

## What Must Match Baseline By Default

- Azure hosting substrate
- public MCP endpoint pattern
- ingress model
- target port behavior
- startup command shape
- MCP runtime shape
- transport/session behavior
- validation sequence
- evidence model
- GitHub-as-source-of-truth discipline

## Testing Connector Doctrine

For testing connectors:
- full read access
- full write access
- no intentional family exclusions unless technically impossible
- broad tool surface on purpose
- discovery first
- scope trimming later only if production needs it

## Constraint Doctrine

Do not cripple the tool surface in testing merely to constrain the model.

The connector should be broadly capable in test.

Operational constraint should come from:
- explicit human judgment
- intentional prompting / planning
- staged rollout and validation
- environment choice
- later production narrowing if desired

## Write Doctrine

Testing connectors may expose broad write capability.

However:
- writes should still be auditable
- read-back verification should be preferred where practical
- destructive or surprising behavior should be documented, not hidden

## Documentation Doctrine

Every connector repo or folder must be sufficient for a fresh thread to understand:
- what baseline it inherits
- what is intentionally the same as baseline
- what is intentionally different
- how Azure deploys it
- how ChatGPT attaches to it
- how validation is performed
- what evidence proves it works

## Research Doctrine For New Systems

When building a connector for a new target system:
- check the official product/API documentation
- check high-quality examples or top integrations for expected payload shapes and capabilities
- do not guess request contracts if official docs are available
- pin discovered request/response contracts into the adapter layer and docs

## Fresh-Thread Goal

A new thread should be able to say:
"Use the baseline and build me the next connector"

and GitHub should provide enough doctrine and artifacts to do that without re-explaining the architecture from scratch.
