import tkinter as tk
from tkinter import ttk, filedialog

from .openfiles import OpenFiles


class OpenFolder(OpenFiles):
    def __init__(self):
        super().__init__()
        self.name = "Open Folder"

    def build_ui(self):
        super().build_ui()
        self.source_button.configure(text="Select Folder")

    def select_source(self):
        file_path = filedialog.askdirectory()
        self.source_path.set(file_path)

    def create_tooltip(self):
        tooltip = """
This command is used to open files or directories from your computer.
        """

        self.explanatory_tooltip(tooltip)
