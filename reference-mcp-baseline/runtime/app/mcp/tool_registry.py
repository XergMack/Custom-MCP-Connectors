from mcp.server.fastmcp import FastMCP

from app.mcp.handlers.get_item_metadata import handle_get_item_metadata
from app.mcp.handlers.create_text_file import handle_create_text_file
from app.mcp.handlers.update_text_file import handle_update_text_file
from app.mcp.handlers.create_folder import handle_create_folder
from app.mcp.handlers.move_or_rename_item import handle_move_or_rename_item
from app.mcp.handlers.delete_item import handle_delete_item

def register_tools(mcp: FastMCP):
    @mcp.tool(name="get_item_metadata")
    def get_item_metadata(path: str):
        return handle_get_item_metadata(path)

    @mcp.tool(name="create_text_file")
    def create_text_file(path: str, content: str, conflict: str = "fail"):
        return handle_create_text_file(path, content, conflict)

    @mcp.tool(name="update_text_file")
    def update_text_file(path: str, content: str):
        return handle_update_text_file(path, content)

    @mcp.tool(name="create_folder")
    def create_folder(path: str):
        return handle_create_folder(path)

    @mcp.tool(name="move_or_rename_item")
    def move_or_rename_item(source: str, destination: str):
        return handle_move_or_rename_item(source, destination)

    @mcp.tool(name="delete_item")
    def delete_item(path: str):
        return handle_delete_item(path)
