# requests

Status: Working

## Endpoints
- GET /requests
- GET /requests/{id}
- POST /requests
- PUT /requests/{id}

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
- In this environment, support group is resolved but omitted from initial create payload
- Group should be handled as a deferred post-create action

## Required fields observed
- subject
- description
- requester

## Known working examples
- list_requests
- get_request
- create_request
- update_request
- search_requests
- create_request_from_context

## Notes
- Default template fallback uses "Default Request"
- Site-aware support group resolution is implemented
