# worklogs

Status: In Progress

## Endpoints
- GET /requests/{id}/worklogs
- POST /requests/{id}/worklogs

## Read
- Yes

## Write
- Yes

## Write shape
- POST uses form field: input_data
- payload wrapper: worklog

## Required fields observed
- owner
- time_spent as structured object
- description

## Known working examples
- create worklog with owner.name and time_spent.hours/minutes

## Notes
- simple string time_spent failed
- owner missing failed
- corrected payload works
