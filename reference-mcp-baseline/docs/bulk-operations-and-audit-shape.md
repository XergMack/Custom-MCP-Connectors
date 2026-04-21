# Bulk Operations and Audit Shape

This patch adds the first usability/product-shape layer needed to make the custom SharePoint MCP more competitive.

Added tools:
- bulk_create_folders
- bulk_move_or_rename_items
- bulk_delete_items

Behavior added:
- continue_on_error
- skip/fail behaviors for common idempotent cases
- verification flags
- structured summary output for batch runs
