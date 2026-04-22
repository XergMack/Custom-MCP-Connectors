# SharePoint MCP — Full-Surface Test Connector Implementation Map

## Purpose

This document maps the target full-surface SharePoint MCP test connector to concrete implementation primitives.

For each MCP tool, this file defines:

- likely Microsoft Graph endpoint family
- required addressing inputs
- preferred execution model
- safety / validation rules
- expected return shape guidance
- logging requirements
- phase assignment

This is the implementation companion to:

`sharepoint-mcp/docs/full-surface-test-connector-plan.md`

## Core Implementation Rules

### 1. Resolve first, execute second

Preferred flow for most operations:

1. accept human-friendly input
2. resolve to stable IDs
3. execute using IDs
4. return both original input and resolved IDs

### 2. IDs are the durable execution primitive

Use:

- `site_id`
- `drive_id`
- `item_id`

Friendly path should be treated as a convenience layer, not the primary durable key.

### 3. Mutations must declare policy

Every mutation tool must declare or accept:

- conflict mode
- overwrite mode
- confirmation/destructive flag if relevant
- validation / preflight behavior
- logging expectations

### 4. Broad test surface, controlled production trim

This file defines the full-surface test harness, not the final production trim surface.

## Shared Return Shape Guidance

Where practical, responses should include:

- `input`
- `resolved.site_id`
- `resolved.drive_id`
- `resolved.item_id`
- `resolved.path`
- `result`
- `request_id` / correlation ID if available
- `warnings`
- `is_error`

## Shared Logging Guidance

Every high-value read and every mutation should log:

- timestamp
- tool name
- actor / auth mode
- original input
- resolved IDs
- normalized path
- result summary
- request/correlation IDs
- error class if failed

## Phase A — Discovery + Read Ceiling

## 1. `list_sites`

### Goal
Enumerate accessible SharePoint sites within the configured scope.

### Graph family
- Sites listing/search family
- likely `/sites` search/query patterns depending on scope model

### Inputs
- optional search term
- optional pagination controls

### Execution model
- no mutation
- returns site identifiers and human-friendly names

### Safety rules
- read-only
- pagination required
- avoid unbounded dumps

### Return shape
- site id
- display name
- web URL
- optional site name / hostname

### Logging
- query
- count returned

### Phase
- Phase A

## 2. `get_site`

### Goal
Fetch one site by ID or by resolvable friendly reference.

### Graph family
- site get family

### Inputs
- `site_id` or resolvable site reference

### Execution model
- resolve if needed
- fetch canonical site object

### Safety rules
- read-only

### Return shape
- site metadata
- canonical IDs

### Phase
- Phase A

## 3. `list_drives`

### Goal
List document libraries / drives for a target site.

### Graph family
- site drives family

### Inputs
- `site_id`

### Execution model
- fetch drives for site

### Safety rules
- read-only
- pagination if needed

### Return shape
- drive id
- drive name
- drive type
- web URL if available

### Phase
- Phase A

## 4. `get_drive`

### Goal
Fetch one drive/library by ID.

### Graph family
- drive get family

### Inputs
- `drive_id`

### Execution model
- direct fetch by ID

### Safety rules
- read-only

### Return shape
- drive metadata

### Phase
- Phase A

## 5. `list_children`

### Goal
List children under a root or folder item.

### Graph family
- drive item children family

### Inputs
One of:
- `drive_id` + `item_id`
- `drive_id` + relative path
- `site_id` + path if resolver supports it

### Execution model
- resolve folder/root target
- enumerate children

### Safety rules
- read-only
- pagination required
- return item type indicators (file/folder/package)

### Return shape
- item ids
- names
- type indicators
- size
- last modified
- parent references

### Phase
- Phase A

## 6. `search_items`

### Goal
Search items within configured site/drive scope.

### Graph family
- drive/site search family

### Inputs
- search query
- optional site/drive scope
- pagination controls

### Execution model
- perform bounded search
- return ranked matches

### Safety rules
- read-only
- explicit scope control preferred
- avoid unbounded org-wide search by default in test unless intentionally enabled

### Return shape
- matched item metadata
- scope used

### Phase
- Phase A

## 7. `resolve_path_to_item`

### Goal
Resolve a friendly path to a stable site/drive/item reference.

### Graph family
- site/drive resolution + drive item by path family

### Inputs
- path
- optional `site_id`
- optional `drive_id`

### Execution model
- normalize path
- identify target drive
- resolve to stable item IDs

### Safety rules
- read-only
- path normalization must be deterministic
- return clear not-found vs ambiguous-path errors

### Return shape
- original path
- normalized path
- resolved site/drive/item IDs
- item metadata

### Phase
- Phase A

## 8. `get_item_metadata`

### Goal
Fetch metadata for one item.

### Graph family
- drive item get family

### Inputs
One of:
- `item_id`
- resolvable path with site/drive context

### Execution model
- resolve if needed
- fetch metadata by ID

### Safety rules
- read-only

### Return shape
- item metadata
- resolved IDs

### Phase
- Phase A

## 9. `read_text_file`

### Goal
Read textual file content for supported text-like file types.

### Graph family
- drive item content family

### Inputs
- `item_id` or resolvable path
- optional encoding hint if needed

### Execution model
- resolve target
- fetch content stream
- decode as text

### Safety rules
- read-only
- size guardrails
- content-type validation
- reject unsupported binary content unless explicitly routed to download flow

### Return shape
- resolved IDs
- content type
- decoded text
- truncation indicator if used

### Phase
- Phase A

## 10. `download_file`

### Goal
Download file content / content URL / bytes descriptor for any file type.

### Graph family
- drive item content family

### Inputs
- `item_id` or resolvable path

### Execution model
- resolve target
- fetch download URL or stream metadata

### Safety rules
- read-only
- size guardrails
- return metadata if full byte-return is impractical

### Return shape
- resolved IDs
- size
- mime type
- download primitive or content wrapper

### Phase
- Phase A

## 11. `get_item_versions`

### Goal
List versions for a file.

### Graph family
- drive item versions family

### Inputs
- `item_id` or resolvable path

### Execution model
- resolve target
- list versions

### Safety rules
- read-only

### Return shape
- version IDs
- modified times
- modified by
- optional size / labels

### Phase
- Phase A or C depending on implementation pace

## 12. `get_permissions`

### Goal
Read permissions/sharing metadata for a file/folder.

### Graph family
- permissions family

### Inputs
- `item_id` or resolvable path

### Execution model
- resolve target
- fetch permissions

### Safety rules
- read-only
- permission visibility depends on auth scope

### Return shape
- permissions/shares summary

### Phase
- Phase A or C depending on auth complexity

## Phase B — Non-Destructive Write Ceiling

## 13. `create_folder`

### Goal
Create a folder under a parent location.

### Graph family
- drive item children create family

### Inputs
- parent identified by ID or path
- folder name
- conflict policy

### Execution model
- resolve parent
- create child folder

### Safety rules
- require explicit conflict policy (`fail`, `replace`, `rename` where supported)
- log parent and created child IDs

### Return shape
- created folder metadata
- resolved parent IDs

### Phase
- Phase B

## 14. `create_text_file`

### Goal
Create a new text file with provided content.

### Graph family
- drive item by path/content upload family

### Inputs
- parent or full target path
- content
- conflict / overwrite mode

### Execution model
- resolve target parent
- create file with text content

### Safety rules
- explicit conflict policy
- content size checks
- optional dry-run path validation before write

### Return shape
- created item metadata
- write policy used

### Phase
- Phase B

## 15. `update_text_file`

### Goal
Replace or update text file content.

### Graph family
- file content update family

### Inputs
- item identified by ID or path
- new content
- optional concurrency token / eTag

### Execution model
- resolve target
- optionally validate item type/content type
- upload replacement content

### Safety rules
- support optimistic concurrency if possible
- explicit overwrite intent
- reject folders/non-text-like targets unless explicitly allowed

### Return shape
- updated item metadata
- prior eTag/new eTag if available

### Phase
- Phase B

## 16. `upload_file_small`

### Goal
Upload small file content directly.

### Graph family
- direct content upload family

### Inputs
- parent target
- filename
- bytes/content
- conflict mode

### Execution model
- direct upload for size-bounded files

### Safety rules
- hard size threshold
- conflict policy required

### Return shape
- created/updated item metadata

### Phase
- Phase B

## 17. `upload_file_large_session`

### Goal
Upload large files via resumable upload session.

### Graph family
- upload session family

### Inputs
- parent target
- filename
- content source / chunk plan
- conflict mode

### Execution model
- create upload session
- upload chunks
- finalize item

### Safety rules
- resumable logging
- chunk progress visibility
- cleanup/retry behavior documented

### Return shape
- upload session metadata during execution
- final item metadata on completion

### Phase
- Phase B

## 18. `rename_item`

### Goal
Rename an item without moving it.

### Graph family
- drive item patch/update family

### Inputs
- target by ID or path
- new name
- optional concurrency token

### Execution model
- resolve target
- patch name

### Safety rules
- concurrency support preferred
- conflict behavior explicit if target name exists

### Return shape
- updated item metadata

### Phase
- Phase B

## 19. `copy_item`

### Goal
Copy an item to a destination.

### Graph family
- drive item copy family

### Inputs
- source by ID/path
- destination parent by ID/path
- optional new name

### Execution model
- resolve source and destination
- invoke copy operation
- handle async/monitoring if needed

### Safety rules
- do not overwrite silently
- return operation tracking info if asynchronous

### Return shape
- operation status or copied item metadata

### Phase
- Phase B

## Phase C — Destructive / Admin Ceiling

## 20. `move_item`

### Goal
Move an item to a new parent and/or rename it.

### Graph family
- drive item patch/update parentReference family

### Inputs
- source by ID/path
- destination parent by ID/path
- optional new name
- optional concurrency token

### Execution model
- resolve source/destination
- patch parent reference / name

### Safety rules
- explicit confirmation in destructive/admin mode if risk is high
- concurrency support preferred
- no silent overwrite

### Return shape
- moved item metadata
- source/destination IDs

### Phase
- Phase C

## 21. `delete_item`

### Goal
Delete a file/folder.

### Graph family
- drive item delete family

### Inputs
- target by ID/path
- destructive confirmation flag
- optional concurrency token

### Execution model
- resolve target
- validate target
- delete

### Safety rules
- explicit destructive confirmation required
- optional soft-delete awareness if available
- strong logging required

### Return shape
- deleted target summary
- resolved IDs
- deletion status

### Phase
- Phase C

## 22. `restore_version`

### Goal
Restore a prior version of a file.

### Graph family
- versions restore family if supported by chosen auth/resource flow

### Inputs
- target item
- version ID

### Execution model
- resolve target
- validate version
- restore

### Safety rules
- explicit confirmation required
- audit old/new state

### Return shape
- restored item metadata
- restored version info

### Phase
- Phase C

## 23. `set_metadata`

### Goal
Patch item/list metadata fields.

### Graph family
- list item fields / metadata update family

### Inputs
- target item
- metadata patch payload
- optional concurrency token

### Execution model
- resolve target
- validate allowed fields
- patch metadata

### Safety rules
- field allowlist strongly recommended
- reject unsupported/system-managed fields
- log before/after field set where practical

### Return shape
- updated metadata
- fields changed

### Phase
- Phase C

## Optional Control / Safety Tools

## 24. `preflight_mutation`

### Goal
Validate a mutation request before executing it.

### Inputs
- proposed operation name
- target identifiers
- policy flags

### Execution model
- resolve target
- validate permissions / addressability / likely conflicts
- return predicted execution plan

### Safety rules
- no mutation

### Return shape
- executable: true/false
- warnings
- resolved IDs
- predicted conflict points

### Phase
- Optional but highly recommended in test harness mode

## Permission Strategy

## Test Harness Mode
Broad enough for full-surface testing, but still intentionally scoped to the test environment.

Recommended principle:
- use the minimum set that still supports the full target test surface
- avoid granting org-wide power where narrower site-scoped or resource-scoped grants are possible

## Production Mode
Trim permissions along with the tool surface.

## Open permission task
Create a separate permission matrix mapping each tool to the narrowest acceptable Graph permission set once the exact auth mode is finalized.

## Error Model

Normalize backend/provider failures into:

- `auth_error`
- `not_found`
- `conflict`
- `validation_error`
- `throttled`
- `backend_error`
- `unexpected_error`

Each tool should preserve raw provider context in logs while returning normalized MCP-facing errors.

## Immediate Build Order

1. Implement deterministic path/site/drive/item resolution
2. Build discovery tools
3. Build read tools
4. Build non-destructive writes
5. Build destructive/admin tools
6. Add permission and metadata depth only after core discovery/read/write flows are stable

## Current Recommendation

Treat the current live SharePoint connector as:

- hosting baseline
- transport/session baseline
- minimal working reference

Treat the next connector iteration as:

- full-surface test harness
- ID-first design
- broad read/write with guardrails
- later trimmed for production
