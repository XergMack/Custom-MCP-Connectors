class ExtensionPolicy:

    def validate_allowed_extension(self, name):
        if not name.endswith((".txt",".md",".json")):
            raise Exception("Invalid extension")
