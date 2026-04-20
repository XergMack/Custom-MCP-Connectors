# assets

Status: In Progress

## Endpoints
- GET /assets
- GET /assets/{id}

## Read
- Yes

## Write
- Supported by docs, not yet implemented here

## Query shape
- Uses input_data.list_info for paging/filtering
- search_criteria currently mapped for:
  - name
  - asset_tag
  - serial_number

## Write shape
- Not yet mapped in connector

## Required fields observed
- None yet in live testing

## Known working examples
- list_assets
- get_asset
- search_assets

## Notes
- On-prem V3 assets are supported at /api/v3/assets
