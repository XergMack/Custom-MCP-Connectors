# assets

Status: Blocked

## Endpoints
- GET /assets
- GET /assets/{id}

## Read
- Intended yes
- Currently blocked in this environment

## Write
- Not implemented

## Query shape
- input_data.list_info tested

## Write shape
- Not yet mapped

## Required fields observed
- None yet

## Known working examples
- None in this environment

## Notes
- Direct call to /assets with valid auth returned:
  - status_code 4004
  - message "Internal Error"
- Same failure occurred through the MCP connector
- Conclusion: asset family is currently blocked by the ServiceDesk environment/module state, not the connector
- Defer further asset work for now and proceed to CMDB
