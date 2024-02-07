class Action:
    def perform_task(self):
        raise NotImplementedError("Subclasses must implement perform_task method")

    def build_ui(self, parent_frame):
        raise NotImplementedError("Subclasses must implement build_ui method")
