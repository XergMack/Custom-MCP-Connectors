class PathPolicy:
    def normalize_drive_relative_path(self, item_path):
        clean = (item_path or "").strip().strip("/")

        if clean == "":
            return "Forge"

        if clean.startswith("Shared Documents/Forge"):
            return clean.replace("Shared Documents/", "", 1)

        if clean == "Forge" or clean.startswith("Forge/"):
            return clean

        if clean.startswith("Shared Documents/"):
            clean = clean.replace("Shared Documents/", "", 1)

        return f"Forge/{clean}"

    def split_parent_and_name(self, path):
        path = path.strip().strip("/")
        if "/" not in path:
            raise Exception("Path must include parent and name")
        return path.rsplit("/", 1)
