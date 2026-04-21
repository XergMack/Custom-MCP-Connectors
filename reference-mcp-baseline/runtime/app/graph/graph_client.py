from urllib.parse import quote

class GraphClient:

    def __init__(self, http, ctx):
        self.http = http
        self.ctx = ctx

    def _auth(self):
        return {"Authorization": f"Bearer {self.ctx.token}"}

    def _encode(self, p):
        return quote(p).replace("%2F","/")

    def resolve_by_path(self, path):
        url = f"https://graph.microsoft.com/v1.0/sites/{self.ctx.site_id}/drives/{self.ctx.drive_id}/root:/{self._encode(path)}"
        return self.http.get_json(url, self._auth())

    def get_by_id(self, id):
        url = f"https://graph.microsoft.com/v1.0/sites/{self.ctx.site_id}/drives/{self.ctx.drive_id}/items/{id}"
        return self.http.get_json(url, self._auth())

    def create_text_file(self, parent, name, content, conflict):
        url = f"https://graph.microsoft.com/v1.0/sites/{self.ctx.site_id}/drives/{self.ctx.drive_id}/root:/{parent}/{name}:/content"
        return self.http.put_bytes(url, self._auth(), content.encode())

    def delete_item(self, id):
        url = f"https://graph.microsoft.com/v1.0/sites/{self.ctx.site_id}/drives/{self.ctx.drive_id}/items/{id}"
        self.http.delete(url, self._auth())

    def update_text_file(self, path, content):
        url = f"https://graph.microsoft.com/v1.0/sites/{self.ctx.site_id}/drives/{self.ctx.drive_id}/root:/{self._encode(path)}:/content"
        return self.http.put_bytes(url, self._auth(), content.encode())

    def create_folder(self, parent_path, name):
        parent = self.resolve_by_path(parent_path)
        url = f"https://graph.microsoft.com/v1.0/sites/{self.ctx.site_id}/drives/{self.ctx.drive_id}/items/{parent['id']}/children"

        body = {
            "name": name,
            "folder": {}
        }

        return self.http.post_json(url, {**self._auth(), "Content-Type": "application/json"}, body)

    def move_or_rename_item(self, item_id, new_name=None, new_parent_id=None):
        url = f"https://graph.microsoft.com/v1.0/sites/{self.ctx.site_id}/drives/{self.ctx.drive_id}/items/{item_id}"

        body = {}
        if new_name:
            body["name"] = new_name
        if new_parent_id:
            body["parentReference"] = {"id": new_parent_id}

        return self.http.patch_json(url, {**self._auth(), "Content-Type": "application/json"}, body)
