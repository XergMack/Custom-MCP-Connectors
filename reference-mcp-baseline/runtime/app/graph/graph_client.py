from urllib.parse import quote

class GraphClient:
    def __init__(self, http, ctx):
        self.http = http
        self.ctx = ctx

    def _auth(self):
        return {"Authorization": f"Bearer {self.ctx.token}"}

    def _json_headers(self):
        return {**self._auth(), "Content-Type": "application/json"}

    def _encode(self, p):
        return quote(p).replace("%2F", "/")

    def _base(self):
        return f"https://graph.microsoft.com/v1.0/sites/{self.ctx.site_id}/drives/{self.ctx.drive_id}"

    def list_drives(self):
        url = f"https://graph.microsoft.com/v1.0/sites/{self.ctx.site_id}/drives"
        return self.http.get_json(url, self._auth())

    def search_items(self, query):
        q = quote(query, safe="")
        url = f"{self._base()}/root/search(q='{q}')"
        return self.http.get_json(url, self._auth())

    def resolve_by_path(self, path):
        url = f"{self._base()}/root:/{self._encode(path)}"
        return self.http.get_json(url, self._auth())

    def get_by_id(self, id):
        url = f"{self._base()}/items/{id}"
        return self.http.get_json(url, self._auth())

    def list_children(self, path=None, item_id=None):
        if item_id:
            url = f"{self._base()}/items/{item_id}/children"
            return self.http.get_json(url, self._auth())

        if path:
            parent = self.resolve_by_path(path)
            url = f"{self._base()}/items/{parent['id']}/children"
            return self.http.get_json(url, self._auth())

        url = f"{self._base()}/root/children"
        return self.http.get_json(url, self._auth())

    def get_versions(self, item_id):
        url = f"{self._base()}/items/{item_id}/versions"
        return self.http.get_json(url, self._auth())

    def get_content_text_by_id(self, item_id):
        url = f"{self._base()}/items/{item_id}/content"
        return self.http.get_text(url, self._auth())

    def get_content_bytes_by_id(self, item_id):
        url = f"{self._base()}/items/{item_id}/content"
        return self.http.get_bytes(url, self._auth())

    def create_text_file(self, parent, name, content):
        url = f"{self._base()}/root:/{parent}/{name}:/content"
        return self.http.put_bytes(url, self._auth(), content.encode())

    def upload_bytes(self, path, data):
        url = f"{self._base()}/root:/{self._encode(path)}:/content"
        return self.http.put_bytes(url, self._auth(), data)

    def delete_item(self, id):
        url = f"{self._base()}/items/{id}"
        self.http.delete(url, self._auth())

    def update_text_file(self, path, content):
        url = f"{self._base()}/root:/{self._encode(path)}:/content"
        return self.http.put_bytes(url, self._auth(), content.encode())

    def create_folder(self, parent_path, name):
        parent = self.resolve_by_path(parent_path)
        url = f"{self._base()}/items/{parent['id']}/children"
        body = {
            "name": name,
            "folder": {}
        }
        return self.http.post_json(url, self._json_headers(), body)

    def rename_item(self, item_id, new_name):
        url = f"{self._base()}/items/{item_id}"
        return self.http.patch_json(url, self._json_headers(), {"name": new_name})

    def copy_item(self, item_id, new_name=None, new_parent_id=None):
        url = f"{self._base()}/items/{item_id}/copy"
        body = {}
        if new_name:
            body["name"] = new_name
        if new_parent_id:
            body["parentReference"] = {"id": new_parent_id}
        return self.http.post_json(url, self._json_headers(), body)

    def move_or_rename_item(self, item_id, new_name=None, new_parent_id=None):
        url = f"{self._base()}/items/{item_id}"
        body = {}
        if new_name:
            body["name"] = new_name
        if new_parent_id:
            body["parentReference"] = {"id": new_parent_id}
        return self.http.patch_json(url, self._json_headers(), body)
