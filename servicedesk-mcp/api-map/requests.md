# requests

Status: In Progress

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
- list requests uses input_data.list_info for paging/filtering
- proven working:
  - row_count
  - start_index
  - get_total_count
  - search_criteria

## Write shape
- POST/PUT use form field: input_data
- input_data contains JSON body

## Required fields observed
- create request requires requester
- update request works with request payload wrapper

## Known working examples
- list requests
- get request
- create request
- update request
- assigned-to-me search with search_criteria

## Notes
- top-level start_index was rejected
- input_data.list_info worked
