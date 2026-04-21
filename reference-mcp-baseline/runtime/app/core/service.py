import base64
import os
from azure.identity import DefaultAzureCredential
from app.transport.http_transport import HttpTransport, BackendRequestError
from app.graph.graph_client import GraphClient
from app.policies.path_policy import PathPolicy
from app.policies.extension_policy import ExtensionPolicy

class GraphContext:
    def __init__(self):
        self.site_id = os.environ["CABERLINK_SITE_ID"]
        self.drive_id = os.environ["CABERLINK_DRIVE_ID"]

        explicit = os.environ.get("CABERLINK_GRAPH_ACCESS_TOKEN", "").strip()
        if explicit:
            self.token = explicit
        else:
            cred = DefaultAzureCredential()
            self.token = cred.get_token("https://graph.microsoft.com/.default").token

class Service:
    def __init__(self):
        self.http = HttpTransport()
        self.ctx = GraphContext()
        self.graph = GraphClient(self.http, self.ctx)
        self.paths = PathPolicy()
        self.ext = ExtensionPolicy()

    def get_item_metadata(self, path):
        path = self.paths.normalize_drive_relative_path(path)
        return self.graph.resolve_by_path(path)

    def list_drives(self):
        return self.graph.list_drives()

    def resolve_path_to_item(self, path):
        path = self.paths.normalize_drive_relative_path(path)
        return self.graph.resolve_by_path(path)

    def list_children(self, path=""):
        path = self.paths.normalize_drive_relative_path(path)
        return self.graph.list_children(path=path)

    def search_items(self, query):
        return self.graph.search_items(query)

    def read_text_file(self, path):
        path = self.paths.normalize_drive_relative_path(path)
        item = self.graph.resolve_by_path(path)
        text = self.graph.get_content_text_by_id(item["id"])
        return {
            "Item": item,
            "Text": text
        }

    def download_file(self, path):
        path = self.paths.normalize_drive_relative_path(path)
        item = self.graph.resolve_by_path(path)
        raw = self.graph.get_content_bytes_by_id(item["id"])
        return {
            "Item": item,
            "ContentBase64": base64.b64encode(raw).decode("ascii")
        }

    def get_item_versions(self, path):
        path = self.paths.normalize_drive_relative_path(path)
        item = self.graph.resolve_by_path(path)
        return self.graph.get_versions(item["id"])

    def create_text_file(self, path, content, conflict="fail"):
        parent, name = self.paths.split_parent_and_name(path)
        self.ext.validate_allowed_extension(name)

        parent = self.paths.normalize_drive_relative_path(parent)
        full = self.paths.normalize_drive_relative_path(path)

        if conflict == "fail":
            try:
                self.graph.resolve_by_path(full)
                raise BackendRequestError("Item already exists.", 409)
            except BackendRequestError as e:
                if e.status_code != 404:
                    raise

        created = self.graph.create_text_file(parent, name, content)
        return self.graph.get_by_id(created["id"])

    def update_text_file(self, path, content):
        path = self.paths.normalize_drive_relative_path(path)

        try:
            existing = self.graph.resolve_by_path(path)
        except BackendRequestError as e:
            if e.status_code == 404:
                raise BackendRequestError("Item does not exist.", 404)
            raise

        self.ext.validate_allowed_extension(existing["name"])
        updated = self.graph.update_text_file(path, content)
        return self.graph.get_by_id(updated["id"])

    def upload_file_small(self, path, content_b64, conflict="replace"):
        parent, name = self.paths.split_parent_and_name(path)
        self.ext.validate_allowed_extension(name)

        full = self.paths.normalize_drive_relative_path(path)
        data = base64.b64decode(content_b64)

        if conflict == "fail":
            try:
                self.graph.resolve_by_path(full)
                raise BackendRequestError("Item already exists.", 409)
            except BackendRequestError as e:
                if e.status_code != 404:
                    raise

        uploaded = self.graph.upload_bytes(full, data)
        return self.graph.get_by_id(uploaded["id"])

    def create_folder(self, path):
        parent, name = self.paths.split_parent_and_name(path)
        parent = self.paths.normalize_drive_relative_path(parent)
        created = self.graph.create_folder(parent, name)
        return self.graph.get_by_id(created["id"])

    def rename_item(self, path, new_name):
        self.ext.validate_allowed_extension(new_name) if "." in new_name else None
        path = self.paths.normalize_drive_relative_path(path)
        item = self.graph.resolve_by_path(path)
        updated = self.graph.rename_item(item["id"], new_name)
        return self.graph.get_by_id(updated["id"])

    def copy_item(self, source, destination):
        source = self.paths.normalize_drive_relative_path(source)
        dst_parent, dst_name = self.paths.split_parent_and_name(destination)
        dst_parent = self.paths.normalize_drive_relative_path(dst_parent)

        src_item = self.graph.resolve_by_path(source)
        parent_item = self.graph.resolve_by_path(dst_parent)

        result = self.graph.copy_item(
            src_item["id"],
            new_name=dst_name,
            new_parent_id=parent_item["id"]
        )
        return {
            "Accepted": True,
            "CopyResult": result
        }

    def move_or_rename_item(self, source, destination):
        src_parent, src_name = source.rsplit("/", 1)
        dst_parent, dst_name = destination.rsplit("/", 1)

        if src_parent == dst_parent and src_name == dst_name:
            raise Exception("No-op move not allowed")

        src = self.paths.normalize_drive_relative_path(source)
        dst_parent, dst_name = self.paths.split_parent_and_name(destination)

        src_item = self.graph.resolve_by_path(src)

        parent = self.paths.normalize_drive_relative_path(dst_parent)
        parent_item = self.graph.resolve_by_path(parent)

        updated = self.graph.move_or_rename_item(
            src_item["id"],
            new_name=dst_name,
            new_parent_id=parent_item["id"]
        )

        return self.graph.get_by_id(updated["id"])

    def delete_item(self, path):
        path = self.paths.normalize_drive_relative_path(path)
        try:
            item = self.graph.resolve_by_path(path)
        except BackendRequestError as e:
            if e.status_code == 404:
                raise BackendRequestError("Item does not exist.", 404)
            raise

        self.graph.delete_item(item["id"])

        try:
            self.graph.get_by_id(item["id"])
            return {"Deleted": False}
        except BackendRequestError as e:
            if e.status_code == 404:
                return {"Deleted": True}
            raise
