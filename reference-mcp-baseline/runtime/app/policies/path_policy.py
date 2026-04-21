class PathPolicy:

    def normalize_drive_relative_path(self, item_path):
        clean = item_path.strip().strip("/")

        if clean.startswith("Shared Documents/Forge"):
            return clean.replace("Shared Documents/", "")

        if clean == "Forge" or clean.startswith("Forge/"):
            return clean

        return f"Forge/{clean}"

    def split_parent_and_name(self, path):
        return path.rsplit("/",1)
