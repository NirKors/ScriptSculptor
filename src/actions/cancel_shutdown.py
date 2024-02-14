import tkinter as tk
from .action import Action


class CancelShutdown(Action):
    def __init__(self):
        super().__init__()

    def build_ui(self):
        pass

    def check_for_errors(self):
        pass

    def get_command_string(self):
        return "/shutdown /a"

