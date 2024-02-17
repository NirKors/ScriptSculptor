import tkinter as tk
from .action import Action


class CancelShutdown(Action):
    def __init__(self):
        super().__init__()

    def build_ui(self):
        tooltip = """
        Includes the command to cancel a pending system shutdown.
        
        Adding this command to your script will ensure that the computer does not shut down automatically at a later 
        time."""
        # Set the tooltip text for your Cancel Shutdown action using this variable
        self.explanatory_tooltip(tooltip)

    def check_for_errors(self):
        pass

    def get_command_string(self):
        return "/shutdown /a"

