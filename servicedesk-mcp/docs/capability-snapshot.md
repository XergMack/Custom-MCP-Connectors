# Connector Capability Snapshot

## Working Now
- Request CRUD
- Deterministic request search
- Deterministic context-based request creation
- Requester lookup
- Technician lookup
- Department lookup
- Support group lookup
- Site lookup
- Solution lookup/search
- Contract listing
- Priority/status reference lookup
- Request template listing
- Note/task/worklog operations on requests

## Important Behavioral Note
- Support group resolution works
- Support group should not be sent in the initial request create payload in this environment
- If a group is requested, the connector should treat it as a post-create action

## Blocked / Limited
- Assets blocked by SDP internal error
- CMDB path unresolved in this environment
- Purchase orders blocked by license

## Implication
This connector is strong enough for deterministic request lifecycle management and hosted deployment planning even without assets/CMDB/purchase.
