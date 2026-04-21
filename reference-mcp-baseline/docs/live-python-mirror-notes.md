# Live Python Mirror Notes

This commit aligns the repo with the currently deployed live Python SharePoint MCP connector structure observed in the running container.

Confirmed live areas:
- /app/app/core
- /app/app/graph
- /app/app/mcp
- /app/app/policies
- /app/app/transport

Confirmed live MCP handlers:
- create_folder
- create_text_file
- delete_item
- get_item_metadata
- move_or_rename_item
- update_text_file

Important:
- This is a mirror-alignment step first.
- Tool-surface expansion should happen only after this mirror commit.
