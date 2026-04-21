from mcp.server.fastmcp import FastMCP

from app.mcp.handlers.get_item_metadata import handle_get_item_metadata
from app.mcp.handlers.create_text_file import handle_create_text_file
from app.mcp.handlers.update_text_file import handle_update_text_file
from app.mcp.handlers.create_folder import handle_create_folder
from app.mcp.handlers.move_or_rename_item import handle_move_or_rename_item
from app.mcp.handlers.delete_item import handle_delete_item
from app.mcp.handlers.list_sites import handle_list_sites
from app.mcp.handlers.list_drives import handle_list_drives
from app.mcp.handlers.list_children import handle_list_children
from app.mcp.handlers.resolve_path_to_item import handle_resolve_path_to_item
from app.mcp.handlers.search_items import handle_search_items
from app.mcp.handlers.read_text_file import handle_read_text_file
from app.mcp.handlers.download_file import handle_download_file
from app.mcp.handlers.get_item_versions import handle_get_item_versions
from app.mcp.handlers.upload_file_small import handle_upload_file_small
from app.mcp.handlers.rename_item import handle_rename_item
from app.mcp.handlers.copy_item import handle_copy_item
from app.mcp.handlers.bulk_create_folders import handle_bulk_create_folders
from app.mcp.handlers.bulk_move_or_rename_items import handle_bulk_move_or_rename_items
from app.mcp.handlers.bulk_delete_items import handle_bulk_delete_items

def register_tools(mcp: FastMCP):
    @mcp.tool(name="list_sites")
    def list_sites():
        return handle_list_sites()

    @mcp.tool(name="get_item_metadata")
    def get_item_metadata(path: str, site_id: str = "", drive_id: str = ""):
        return handle_get_item_metadata(path, site_id, drive_id)

    @mcp.tool(name="list_drives")
    def list_drives(site_id: str = ""):
        return handle_list_drives(site_id)

    @mcp.tool(name="list_children")
    def list_children(path: str = "", site_id: str = "", drive_id: str = ""):
        return handle_list_children(path, site_id, drive_id)

    @mcp.tool(name="resolve_path_to_item")
    def resolve_path_to_item(path: str, site_id: str = "", drive_id: str = ""):
        return handle_resolve_path_to_item(path, site_id, drive_id)

    @mcp.tool(name="search_items")
    def search_items(query: str, site_id: str = "", drive_id: str = ""):
        return handle_search_items(query, site_id, drive_id)

    @mcp.tool(name="read_text_file")
    def read_text_file(path: str, site_id: str = "", drive_id: str = ""):
        return handle_read_text_file(path, site_id, drive_id)

    @mcp.tool(name="download_file")
    def download_file(path: str, site_id: str = "", drive_id: str = ""):
        return handle_download_file(path, site_id, drive_id)

    @mcp.tool(name="get_item_versions")
    def get_item_versions(path: str, site_id: str = "", drive_id: str = ""):
        return handle_get_item_versions(path, site_id, drive_id)

    @mcp.tool(name="create_text_file")
    def create_text_file(path: str, content: str, conflict: str = "fail", site_id: str = "", drive_id: str = ""):
        return handle_create_text_file(path, content, conflict, site_id, drive_id)

    @mcp.tool(name="update_text_file")
    def update_text_file(path: str, content: str, site_id: str = "", drive_id: str = ""):
        return handle_update_text_file(path, content, site_id, drive_id)

    @mcp.tool(name="upload_file_small")
    def upload_file_small(path: str, content_b64: str, conflict: str = "replace", site_id: str = "", drive_id: str = ""):
        return handle_upload_file_small(path, content_b64, conflict, site_id, drive_id)

    @mcp.tool(name="create_folder")
    def create_folder(path: str, site_id: str = "", drive_id: str = ""):
        return handle_create_folder(path, site_id, drive_id)

    @mcp.tool(name="rename_item")
    def rename_item(path: str, new_name: str, site_id: str = "", drive_id: str = ""):
        return handle_rename_item(path, new_name, site_id, drive_id)

    @mcp.tool(name="copy_item")
    def copy_item(source: str, destination: str, site_id: str = "", drive_id: str = ""):
        return handle_copy_item(source, destination, site_id, drive_id)

    @mcp.tool(name="move_or_rename_item")
    def move_or_rename_item(source: str, destination: str, site_id: str = "", drive_id: str = ""):
        return handle_move_or_rename_item(source, destination, site_id, drive_id)

    @mcp.tool(name="delete_item")
    def delete_item(path: str, site_id: str = "", drive_id: str = ""):
        return handle_delete_item(path, site_id, drive_id)

    @mcp.tool(name="bulk_create_folders")
    def bulk_create_folders(paths: list[str], site_id: str = "", drive_id: str = "", exists_behavior: str = "skip", continue_on_error: bool = True, verify: bool = True):
        return handle_bulk_create_folders(paths, site_id, drive_id, exists_behavior, continue_on_error, verify)

    @mcp.tool(name="bulk_move_or_rename_items")
    def bulk_move_or_rename_items(items: list[dict], site_id: str = "", drive_id: str = "", continue_on_error: bool = True, verify: bool = True, no_op_behavior: str = "skip"):
        return handle_bulk_move_or_rename_items(items, site_id, drive_id, continue_on_error, verify, no_op_behavior)

    @mcp.tool(name="bulk_delete_items")
    def bulk_delete_items(paths: list[str], site_id: str = "", drive_id: str = "", missing_behavior: str = "skip", continue_on_error: bool = True, verify: bool = True):
        return handle_bulk_delete_items(paths, site_id, drive_id, missing_behavior, continue_on_error, verify)
