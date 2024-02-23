import tkinter as tk
from .action import Action


class SystemInformation(Action):
    def __init__(self):
        super().__init__()


    def build_ui(self):



        tooltip = """
Displays detailed configuration information about a computer and its operating system, including operating
system configuration, security information, product ID, and hardware properties (such as RAM, disk space,
and network cards).
"""
        self.explanatory_tooltip(tooltip)

    def check_for_warnings(self):
        pass

    def check_for_errors(self):
        pass

    def get_command_string(self):
        pass

