from urllib.parse import quote

class GraphClient:
    def __init__(self, http, ctx):
        self.http = http
        self.ctx = ctx

    def _auth(self):
        return {"Authorization": f"Bearer {self.ctx.token}"}

    def _json_headers(self):
        return {**self._auth(), "Content-Type": "application/json"}

    def _site(self, site_id):
        sid = site_id or self.ctx.default_site_id
        if not sid:
            raise Exception("site_id is required")
        return sid

    def _drive(self, drive_id):
        did = drive_id or self.ctx.default_drive_id
        if not did:
            raise Exception("drive_id is required")
        return did

    def _encode(self, p):
        return quote(p).replace("%2F", "/")

    def _base(self, site_id=None, drive_id=None):
        sid = self._site(site_id)
        did = self._drive(drive_id)
        return f"https://graph.microsoft.com/v1.0/sites/{sid}/drives/{did}"

    def list_sites(self):
        url = "https://graph.microsoft.com/v1.0/sites?search=*"
        return self.http.get_json(url, self._auth())

    def list_drives(self, site_id=None):
        sid = self._site(site_id)
        url = f"https://graph.microsoft.com/v1.0/sites/{sid}/drives"
        return self.http.get_json(url, self._auth())

    def get_root(self, site_id=None, drive_id=None):
        url = f"{self._base(site_id=site_id, drive_id=drive_id)}/root"
        return self.http.get_json(url, self._auth())

    def search_items(self, query, site_id=None, drive_id=None):
        q = quote(query, safe="")
        url = f"{self._base(site_id=site_id, drive_id=drive_id)}/root/search(q='{q}')"
        return self.http.get_json(url, self._auth())

    def resolve_by_path(self, path, site_id=None, drive_id=None):
        url = f"{self._base(site_id=site_id, drive_id=drive_id)}/root:/{self._encode(path)}"
        return self.http.get_json(url, self._auth())

    def get_by_id(self, id, site_id=None, drive_id=None):
        url = f"{self._base(site_id=site_id, drive_id=drive_id)}/items/{id}"
        return self.http.get_json(url, self._auth())

    def list_children(self, path=None, item_id=None, site_id=None, drive_id=None):
        if item_id:
            url = f"{self._base(site_id=site_id, drive_id=drive_id)}/items/{item_id}/children"
            return self.http.get_json(url, self._auth())

        if path:
            parent = self.resolve_by_path(path, site_id=site_id, drive_id=drive_id)
            url = f"{self._base(site_id=site_id, drive_id=drive_id)}/items/{parent['id']}/children"
            return self.http.get_json(url, self._auth())

        url = f"{self._base(site_id=site_id, drive_id=drive_id)}/root/children"
        return self.http.get_json(url, self._auth())

    def get_versions(self, item_id, site_id=None, drive_id=None):
        url = f"{self._base(site_id=site_id, drive_id=drive_id)}/items/{item_id}/versions"
        return self.http.get_json(url, self._auth())

    def get_content_text_by_id(self, item_id, site_id=None, drive_id=None):
        url = f"{self._base(site_id=site_id, drive_id=drive_id)}/items/{item_id}/content"
        return self.http.get_text(url, self._auth())

    def get_content_bytes_by_id(self, item_id, site_id=None, drive_id=None):
        url = f"{self._base(site_id=site_id, drive_id=drive_id)}/items/{item_id}/content"
        return self.http.get_bytes(url, self._auth())

    def create_text_file(self, parent, name, content, site_id=None, drive_id=None):
        if parent:
            url = f"{self._base(site_id=site_id, drive_id=drive_id)}/root:/{parent}/{name}:/content"
        else:
            url = f"{self._base(site_id=site_id, drive_id=drive_id)}/root:/{name}:/content"
        return self.http.put_bytes(url, self._auth(), content.encode())

    def upload_bytes(self, path, data, site_id=None, drive_id=None):
        url = f"{self._base(site_id=site_id, drive_id=drive_id)}/root:/{self._encode(path)}:/content"
        return self.http.put_bytes(url, self._auth(), data)

    def delete_item(self, id, site_id=None, drive_id=None):
        url = f"{self._base(site_id=site_id, drive_id=drive_id)}/items/{id}"
        self.http.delete(url, self._auth())

    def update_text_file(self, path, content, site_id=None, drive_id=None):
        url = f"{self._base(site_id=site_id, drive_id=drive_id)}/root:/{self._encode(path)}:/content"
        return self.http.put_bytes(url, self._auth(), content.encode())

    def create_folder(self, parent_path, name, site_id=None, drive_id=None):
        if parent_path:
            parent = self.resolve_by_path(parent_path, site_id=site_id, drive_id=drive_id)
            url = f"{self._base(site_id=site_id, drive_id=drive_id)}/items/{parent['id']}/children"
        else:
            url = f"{self._base(site_id=site_id, drive_id=drive_id)}/root/children"
        body = {
            "name": name,
            "folder": {}
        }
        return self.http.post_json(url, self._json_headers(), body)

    def rename_item(self, item_id, new_name, site_id=None, drive_id=None):
        url = f"{self._base(site_id=site_id, drive_id=drive_id)}/items/{item_id}"
        return self.http.patch_json(url, self._json_headers(), {"name": new_name})

    def copy_item(self, item_id, new_name=None, new_parent_id=None, site_id=None, drive_id=None):
        url = f"{self._base(site_id=site_id, drive_id=drive_id)}/items/{item_id}/copy"
        body = {}
        if new_name:
            body["name"] = new_name
        if new_parent_id:
            body["parentReference"] = {"id": new_parent_id}
        return self.http.post_json(url, self._json_headers(), body)

    def move_or_rename_item(self, item_id, new_name=None, new_parent_id=None, site_id=None, drive_id=None):
        url = f"{self._base(site_id=site_id, drive_id=drive_id)}/items/{item_id}"
        body = {}
        if new_name:
            body["name"] = new_name
        if new_parent_id:
            body["parentReference"] = {"id": new_parent_id}
        return self.http.patch_json(url, self._json_headers(), body)
