class ExtensionPolicy:
    def validate_allowed_extension(self, name):
        if "." not in name:
            return
        if not name.endswith((".txt", ".md", ".json", ".csv", ".html", ".htm", ".xml", ".log")):
            raise Exception("Invalid extension")
