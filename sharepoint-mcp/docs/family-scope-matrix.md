# SharePoint MCP Family Scope Matrix

## Purpose
Define the SharePoint read/write family scope.

## Matrix

| Family | Read | Write | MVP Now | Later | Notes |
|---|---:|---:|---:|---:|---|
| Sites | Yes | Limited | Yes |  | Core discovery |
| Drives | Yes | Limited | Yes |  | Core document access |
| Items / Files | Yes | Yes | Yes |  | Core file operations |
| Folders | Yes | Yes | Yes |  | Core structure operations |
| Permissions | Yes | Limited |  | Yes | Add later if needed |
| Search | Yes | No | Yes |  | Important for retrieval |
| Metadata | Yes | Yes | Yes |  | Important for document workflows |

## Doctrine
- Keep SharePoint thin and deterministic
- Mirror live Azure baseline exactly
