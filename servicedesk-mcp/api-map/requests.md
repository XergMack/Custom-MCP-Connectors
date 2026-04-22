# requests

Status: Working

## Endpoints
- GET /requests
- GET /requests/{id}
- POST /requests
- PUT /requests/{id}
- PUT /requests/{id}/assign

## Read
- Yes

## Write
- Yes

## Query shape
- Uses input_data.list_info for paging/filtering
- search_criteria currently mapped for:
  - technician.name
  - status.name
  - subject
  - requester.name

## Write shape
- Deterministic context create is implemented
- create_request_from_context resolves:
  - requester
  - template
  - site
  - priority
  - status
  - technician
  - support group
- Primary path is ManageEngine doc-first create/edit using documented request attributes
- Documented write fields now used in initial create payload:
  - requester
  - template
  - site
  - priority
  - status
  - technician
  - support group
  - category
- Documented assignment endpoint is also implemented:
  - PUT /requests/{id}/assign
- Compatibility fallback is only used after read-after-write verification detects that technician/group did not persist as expected

## Required fields observed
- subject
- description
- requester

## Known working examples
- list_requests
- get_request
- create_request
- update_request
- assign_request
- search_requests
- create_request_from_context

## Verification behavior
- create_request_from_context now fetches the created request
- final state is verified for:
  - requester
  - template
  - site
  - priority
  - status
  - technician
  - support group
  - category
- if technician or group mismatch after create, compatibility fallback uses the documented assign endpoint and verifies again

## Notes
- Default template fallback uses "Default Request"
- Site-aware support group resolution is implemented
- ManageEngine request docs document technician and group on Add Request and Edit Request, and document Assign Request at /requests/{id}/assign
