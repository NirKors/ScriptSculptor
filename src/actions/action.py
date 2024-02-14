import tkinter as tk


class Action:
    def __init__(self):
        self.ui_engine = None
        self.parent_frame = None

    def build_ui(self):
        raise NotImplementedError("Subclasses must implement build_ui method")


    def check_for_errors(self):
        raise NotImplementedError("Subclasses must implement build_ui method")

    def get_command_string(self):
        raise NotImplementedError("Subclasses must implement get_command_string method")
