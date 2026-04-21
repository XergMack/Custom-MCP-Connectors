class PathPolicy:
    def normalize_drive_relative_path(self, item_path):
        clean = (item_path or "").strip().strip("/")

        if clean.startswith("Shared Documents/"):
            clean = clean.replace("Shared Documents/", "", 1)

        return clean

    def split_parent_and_name(self, path):
        path = (path or "").strip().strip("/")
        if "/" not in path:
            return "", path
        return path.rsplit("/", 1)
