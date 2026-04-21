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

    def get_item_metadata(self, path):
        path = self.paths.normalize_drive_relative_path(path)
        return self.graph.resolve_by_path(path)

    def __init__(self):
        self.http = HttpTransport()
        self.ctx = GraphContext()
        self.graph = GraphClient(self.http, self.ctx)

        self.paths = PathPolicy()
        self.ext = ExtensionPolicy()

    def create_text_file(self, path, content, conflict="fail"):

        parent, name = self.paths.split_parent_and_name(path)
        self.ext.validate_allowed_extension(name)

        parent = self.paths.normalize_drive_relative_path(parent)
        full = self.paths.normalize_drive_relative_path(path)

        if conflict == "fail":
            try:
                self.graph.resolve_by_path(full)
                raise BackendRequestError("Item already exists.",409)
            except BackendRequestError as e:
                if e.status_code != 404:
                    raise

        created = self.graph.create_text_file(parent,name,content,conflict)
        return self.graph.get_by_id(created["id"])

    def update_text_file(self, path, content):
        path = self.paths.normalize_drive_relative_path(path)

        # parity: must exist
        try:
            existing = self.graph.resolve_by_path(path)
        except BackendRequestError as e:
            if e.status_code == 404:
                raise BackendRequestError("Item does not exist.", 404)
            raise

        updated = self.graph.update_text_file(path, content)
        return self.graph.get_by_id(updated["id"])

    def create_folder(self, path):
        parent, name = self.paths.split_parent_and_name(path)
        parent = self.paths.normalize_drive_relative_path(parent)
        created = self.graph.create_folder(parent, name)
        return self.graph.get_by_id(created["id"])

    def move_or_rename_item(self, source, destination):
        # no-op guard (parity requirement)
        src_parent, src_name = source.rsplit("/",1)
        dst_parent, dst_name = destination.rsplit("/",1)

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

        # verification
        try:
            self.graph.get_by_id(item["id"])
            return {"Deleted": False}
        except BackendRequestError as e:
            if e.status_code == 404:
                return {"Deleted": True}
            raise
