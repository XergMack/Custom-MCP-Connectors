# users-requesters

Status: In Progress

## Endpoints
- GET /users
- GET /users/{id}

## Read
- Yes

## Write
- Unknown

## Query shape
- Uses input_data.list_info for paging/filtering
- search_criteria currently mapped for:
  - name
  - email_id

## Write shape
- Not yet mapped

## Required fields observed
- None yet

## Known working examples
- list_requesters
- get_requester
- search_requesters

## Notes
- On-prem V3 maps Requester/User to /api/v3/users
