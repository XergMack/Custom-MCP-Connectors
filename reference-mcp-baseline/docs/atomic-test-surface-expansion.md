# Atomic Test Surface Expansion

This commit expands the current live SharePoint MCP Python connector in place.

Added tools:
- list_drives
- list_children
- resolve_path_to_item
- search_items
- read_text_file
- download_file
- get_item_versions
- upload_file_small
- rename_item
- copy_item

Preserved existing tools:
- get_item_metadata
- create_text_file
- update_text_file
- create_folder
- move_or_rename_item
- delete_item

Notes:
- current connector remains pinned to CABERLINK_SITE_ID + CABERLINK_DRIVE_ID
- current path policy remains Forge-scoped
- this is a test-environment broadening step on the same architecture
