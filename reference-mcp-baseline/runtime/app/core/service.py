import base64
import os
from azure.identity import DefaultAzureCredential
from app.transport.http_transport import HttpTransport, BackendRequestError
from app.graph.graph_client import GraphClient
from app.policies.path_policy import PathPolicy
from app.policies.extension_policy import ExtensionPolicy

class GraphContext:
    def __init__(self):
        self.default_site_id = os.environ.get("CABERLINK_SITE_ID", "").strip()
        self.default_drive_id = os.environ.get("CABERLINK_DRIVE_ID", "").strip()

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

    def _site(self, site_id):
        return site_id or self.ctx.default_site_id

    def _drive(self, drive_id):
        return drive_id or self.ctx.default_drive_id

    def _path(self, path):
        return self.paths.normalize_drive_relative_path(path)

    def list_sites(self):
        return self.graph.list_sites()

    def list_drives(self, site_id=""):
        return self.graph.list_drives(site_id=self._site(site_id))

    def get_item_metadata(self, path, site_id="", drive_id=""):
        path = self._path(path)
        if not path:
            return self.graph.get_root(site_id=self._site(site_id), drive_id=self._drive(drive_id))
        return self.graph.resolve_by_path(path, site_id=self._site(site_id), drive_id=self._drive(drive_id))

    def resolve_path_to_item(self, path, site_id="", drive_id=""):
        path = self._path(path)
        if not path:
            return self.graph.get_root(site_id=self._site(site_id), drive_id=self._drive(drive_id))
        return self.graph.resolve_by_path(path, site_id=self._site(site_id), drive_id=self._drive(drive_id))

    def list_children(self, path="", site_id="", drive_id=""):
        path = self._path(path)
        return self.graph.list_children(path=path, site_id=self._site(site_id), drive_id=self._drive(drive_id))

    def search_items(self, query, site_id="", drive_id=""):
        return self.graph.search_items(query, site_id=self._site(site_id), drive_id=self._drive(drive_id))

    def read_text_file(self, path, site_id="", drive_id=""):
        path = self._path(path)
        item = self.graph.resolve_by_path(path, site_id=self._site(site_id), drive_id=self._drive(drive_id))
        text = self.graph.get_content_text_by_id(item["id"], site_id=self._site(site_id), drive_id=self._drive(drive_id))
        return {
            "Item": item,
            "Text": text
        }

    def download_file(self, path, site_id="", drive_id=""):
        path = self._path(path)
        item = self.graph.resolve_by_path(path, site_id=self._site(site_id), drive_id=self._drive(drive_id))
        raw = self.graph.get_content_bytes_by_id(item["id"], site_id=self._site(site_id), drive_id=self._drive(drive_id))
        return {
            "Item": item,
            "ContentBase64": base64.b64encode(raw).decode("ascii")
        }

    def get_item_versions(self, path, site_id="", drive_id=""):
        path = self._path(path)
        item = self.graph.resolve_by_path(path, site_id=self._site(site_id), drive_id=self._drive(drive_id))
        return self.graph.get_versions(item["id"], site_id=self._site(site_id), drive_id=self._drive(drive_id))

    def create_text_file(self, path, content, conflict="fail", site_id="", drive_id=""):
        parent, name = self.paths.split_parent_and_name(path)
        self.ext.validate_allowed_extension(name)

        parent = self._path(parent)
        full = self._path(path)
        sid = self._site(site_id)
        did = self._drive(drive_id)

        if conflict == "fail":
            try:
                self.graph.resolve_by_path(full, site_id=sid, drive_id=did)
                raise BackendRequestError("Item already exists.", 409)
            except BackendRequestError as e:
                if e.status_code != 404:
                    raise

        created = self.graph.create_text_file(parent, name, content, site_id=sid, drive_id=did)
        return self.graph.get_by_id(created["id"], site_id=sid, drive_id=did)

    def update_text_file(self, path, content, site_id="", drive_id=""):
        path = self._path(path)
        sid = self._site(site_id)
        did = self._drive(drive_id)

        try:
            existing = self.graph.resolve_by_path(path, site_id=sid, drive_id=did)
        except BackendRequestError as e:
            if e.status_code == 404:
                raise BackendRequestError("Item does not exist.", 404)
            raise

        self.ext.validate_allowed_extension(existing["name"])
        updated = self.graph.update_text_file(path, content, site_id=sid, drive_id=did)
        return self.graph.get_by_id(updated["id"], site_id=sid, drive_id=did)

    def upload_file_small(self, path, content_b64, conflict="replace", site_id="", drive_id=""):
        parent, name = self.paths.split_parent_and_name(path)
        self.ext.validate_allowed_extension(name)

        full = self._path(path)
        sid = self._site(site_id)
        did = self._drive(drive_id)
        data = base64.b64decode(content_b64)

        if conflict == "fail":
            try:
                self.graph.resolve_by_path(full, site_id=sid, drive_id=did)
                raise BackendRequestError("Item already exists.", 409)
            except BackendRequestError as e:
                if e.status_code != 404:
                    raise

        uploaded = self.graph.upload_bytes(full, data, site_id=sid, drive_id=did)
        return self.graph.get_by_id(uploaded["id"], site_id=sid, drive_id=did)

    def create_folder(self, path, site_id="", drive_id=""):
        parent, name = self.paths.split_parent_and_name(path)
        sid = self._site(site_id)
        did = self._drive(drive_id)
        parent = self._path(parent)
        created = self.graph.create_folder(parent, name, site_id=sid, drive_id=did)
        return self.graph.get_by_id(created["id"], site_id=sid, drive_id=did)

    def rename_item(self, path, new_name, site_id="", drive_id=""):
        if "." in new_name:
            self.ext.validate_allowed_extension(new_name)
        sid = self._site(site_id)
        did = self._drive(drive_id)
        path = self._path(path)
        item = self.graph.resolve_by_path(path, site_id=sid, drive_id=did)
        updated = self.graph.rename_item(item["id"], new_name, site_id=sid, drive_id=did)
        return self.graph.get_by_id(updated["id"], site_id=sid, drive_id=did)

    def copy_item(self, source, destination, site_id="", drive_id=""):
        sid = self._site(site_id)
        did = self._drive(drive_id)
        source = self._path(source)
        dst_parent, dst_name = self.paths.split_parent_and_name(destination)
        dst_parent = self._path(dst_parent)

        src_item = self.graph.resolve_by_path(source, site_id=sid, drive_id=did)
        parent_item = self.graph.resolve_by_path(dst_parent, site_id=sid, drive_id=did)

        result = self.graph.copy_item(
            src_item["id"],
            new_name=dst_name,
            new_parent_id=parent_item["id"],
            site_id=sid,
            drive_id=did
        )
        return {
            "Accepted": True,
            "CopyResult": result
        }

    def move_or_rename_item(self, source, destination, site_id="", drive_id=""):
        src_parent, src_name = source.rsplit("/", 1)
        dst_parent, dst_name = destination.rsplit("/", 1)

        if src_parent == dst_parent and src_name == dst_name:
            raise Exception("No-op move not allowed")

        sid = self._site(site_id)
        did = self._drive(drive_id)
        src = self._path(source)
        dst_parent, dst_name = self.paths.split_parent_and_name(destination)

        src_item = self.graph.resolve_by_path(src, site_id=sid, drive_id=did)

        parent = self._path(dst_parent)
        parent_item = self.graph.resolve_by_path(parent, site_id=sid, drive_id=did)

        updated = self.graph.move_or_rename_item(
            src_item["id"],
            new_name=dst_name,
            new_parent_id=parent_item["id"],
            site_id=sid,
            drive_id=did
        )

        return self.graph.get_by_id(updated["id"], site_id=sid, drive_id=did)

    def delete_item(self, path, site_id="", drive_id=""):
        sid = self._site(site_id)
        did = self._drive(drive_id)
        path = self._path(path)
        try:
            item = self.graph.resolve_by_path(path, site_id=sid, drive_id=did)
        except BackendRequestError as e:
            if e.status_code == 404:
                raise BackendRequestError("Item does not exist.", 404)
            raise

        self.graph.delete_item(item["id"], site_id=sid, drive_id=did)

        try:
            self.graph.get_by_id(item["id"], site_id=sid, drive_id=did)
            return {"Deleted": False}
        except BackendRequestError as e:
            if e.status_code == 404:
                return {"Deleted": True}
            raise
