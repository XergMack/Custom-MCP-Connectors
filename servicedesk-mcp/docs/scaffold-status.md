# Remaining Family Scaffold Status

## Proven Working Families
- requests
- notes
- worklogs
- tasks
- technicians
- users-requesters
- departments-groups-sites
- solutions
- contracts
- admin reference data
- catalog via request_templates

## Blocked / Constrained Families
- assets
  - direct /assets calls return SDP internal error in this environment
- cmdb
  - tested common CI-type paths and did not find an exposed working path
- purchase
  - blocked by current license

## Scaffolded but Not Implemented
- problems
- changes
- projects

## Doctrine
- Do not downgrade a family from Working without a live failure proving regression
- Do not promote a family to Working until live-tested through the MCP router
- Mark license or environment blocks explicitly
- Prefer deterministic tools over vague model-side filtering
- For request creation in this environment, support group must be treated as a post-create concern

## Next Practical Use
Use the current proven connector surface for deterministic ticket workflows:
- resolve requester
- resolve technician
- resolve department / support group / site
- resolve request template
- create or update request
- add notes / tasks / worklogs
