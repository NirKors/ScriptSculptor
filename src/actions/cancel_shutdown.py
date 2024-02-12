import tkinter as tk
from .action import Action


class CancelShutdown(Action):
    def check_for_errors(self):
        pass

    def __init__(self):
        pass

    def build_ui(self, parent_frame):
        pass

    def get_command_string(self):
        return "/shutdown /a"

