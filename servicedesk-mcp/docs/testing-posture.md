# ServiceDesk MCP Testing Posture

## Purpose
This document defines the testing-environment posture for the rebuilt ServiceDesk MCP connector.

## Testing doctrine
- Full read access
- Full write access
- All available API families included
- No intentional family exclusions in test unless technically impossible
- Testing environment is for discovery, breakage finding, and scope calibration

## Goal
Use the testing connector to determine:
- what works cleanly
- what fails
- what is useful
- what is noisy
- what should remain in production
- what should be trimmed from production

## Scope
In testing:
- expose all practical read capabilities
- expose all practical write capabilities
- include all major ServiceDesk Plus API families
- keep the connector broad on purpose

In production later:
- reduce scope intentionally
- keep only the families and operations that prove useful and reliable
- remove noisy or risky surfaces

## Rule
Testing breadth first.
Production discipline second.
