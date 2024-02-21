import os
import tkinter as tk
from tkinter import ttk, filedialog

from .action import Action


class CreateFolder(Action):
    def __init__(self):
        super().__init__()
        self.path_entry = None
        self.folder_path = tk.StringVar()
        self.include_patterns = tk.StringVar()
        self.exclude_patterns = tk.StringVar()
        self.recursive = tk.BooleanVar()
        self.recursive.set(False)
        self.name = "Create Folder"

    def build_ui(self):
        parent_frame = self.parent_frame

        # Label and entry for folder path
        path_label = ttk.Label(parent_frame, text="Folder Path:")
        path_label.pack(side=tk.LEFT, padx=(0, 5))

        path_entry = ttk.Entry(parent_frame, textvariable=self.folder_path)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.path_entry = path_entry

        folder_button = tk.Button(parent_frame, text="Select Folder", command=self.select_destination)
        folder_button.pack(side=tk.LEFT, padx=(0, 5))

        # Checkbox for recursive creation
        self.add_flag_options("Recursive", self.recursive)

        tooltip = """
        Creates folders based on the specified path and options:

          - Folder Path: Enter the desired location for the new folder(s).
          - Recursive: Check this box to create the folder structure recursively if needed.
        """

        self.explanatory_tooltip(tooltip)

    def check_for_errors(self):
        # Check if path is valid and writable
        path = self.folder_path.get()
        if not path:
            return "Action: Create Folder\nError: Please specify a valid folder path."

        # Check if parent directories exist if not recursive
        if not self.recursive.get() and not os.path.exists(os.path.dirname(path)):
            return "Action: Create Folder\nError: Parent directory does not exist and `Recursive` is not selected."

        return None

    def check_for_warnings(self):
        return True

    def select_destination(self):
        folder_path = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, folder_path)

    def get_command_string(self):
        path = self.folder_path.get()
        flags = ""

        if self.recursive.get():
            flags += " /r"

        # Construct and return the `mkdir` command string
        return f"mkdir {flags} \"{path}\""
