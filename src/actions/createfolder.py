import os
import tkinter as tk
from tkinter import ttk

from .action import Action


class CreateFolder(Action):
    def __init__(self):
        super().__init__()
        self.folder_path = tk.StringVar()
        self.include_patterns = tk.StringVar()
        self.exclude_patterns = tk.StringVar()
        self.recursive = tk.BooleanVar()

        self.recursive.set(False)

    def build_ui(self):
        parent_frame = self.parent_frame

        # Label and entry for folder path
        path_label = ttk.Label(parent_frame, text="Folder Path:")
        path_label.pack(side=tk.LEFT, padx=(0, 5))

        path_entry = tk.Entry(parent_frame, textvariable=self.folder_path)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        # Include and exclude pattern entries
        include_label = ttk.Label(parent_frame, text="Include Patterns:")
        include_label.pack(side=tk.LEFT, padx=(0, 5))

        include_entry = tk.Entry(parent_frame, textvariable=self.include_patterns, width=20)
        include_entry.pack(side=tk.LEFT, padx=(0, 5))

        exclude_label = ttk.Label(parent_frame, text="Exclude Patterns:")
        exclude_label.pack(side=tk.LEFT, padx=(0, 5))

        exclude_entry = tk.Entry(parent_frame, textvariable=self.exclude_patterns, width=20)
        exclude_entry.pack(side=tk.LEFT, padx=(0, 5))

        # Checkbox for recursive creation
        recursive_checkbox = tk.Checkbutton(parent_frame, text="Recursive", variable=self.recursive)
        recursive_checkbox.pack(side=tk.LEFT, padx=(0, 5))

        tooltip = """
        Creates folders based on the specified path and options:

          - Folder Path: Enter the desired location for the new folder(s).
          - Include Patterns: Use wildcards or separators to specify files/folders to include (optional).
          - Exclude Patterns: Use wildcards or separators to specify files/folders to exclude (optional).
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

        # TODO: Add checks for valid patterns (syntax, potential conflicts)

        return None

    def get_command_string(self):
        path = self.folder_path.get()
        flags = ""

        if self.recursive.get():
            flags += " /r"

        # TODO: Generate flags for include/exclude patterns based on syntax and validation

        # Construct and return the `mkdir` command string
        return f"mkdir {flags} \"{path}\""
