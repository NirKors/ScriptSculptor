class Action:
    def get_command_string(self):
        raise NotImplementedError("Subclasses must implement get_command_string method")

    def build_ui(self, parent_frame):
        raise NotImplementedError("Subclasses must implement build_ui method")

    def check_for_errors(self):
        raise NotImplementedError("Subclasses must implement build_ui method")
