import tkinter as tk
from tkinter import filedialog, ttk

from .action import Action


class CopyFiles(Action):
    def __init__(self):
        super().__init__()
        self.source_path = tk.StringVar()
        self.destination_path = tk.StringVar()
        self.suppress_overwrite = tk.BooleanVar()
        self.copy_attributes = tk.BooleanVar()
        self.checkbox_frame = None
        self.name = "Copy Files"
        self.source_button = None

    def build_ui(self):
        parent_frame = self.parent_frame
        # Create and return UI elements for configuring copy options
        source_label = ttk.Label(parent_frame, text="Source Path:")
        source_label.pack(side=tk.LEFT, padx=(0, 5))

        source_entry = tk.Entry(parent_frame, textvariable=self.source_path)
        source_entry.pack(side=tk.LEFT, padx=(0, 5), fill="x", expand=True)

        self.source_button = tk.Button(parent_frame, text="Select File(s)", command=self.select_source)
        self.source_button.pack(side=tk.LEFT, padx=(0, 5))

        destination_label = ttk.Label(parent_frame, text="Destination Path:")
        destination_label.pack(side=tk.LEFT, padx=(0, 5))

        destination_entry = tk.Entry(parent_frame, textvariable=self.destination_path)
        destination_entry.pack(side=tk.LEFT, padx=(0, 5), fill="x", expand=True)

        folder_button = tk.Button(parent_frame, text="Select Folder", command=self.select_destination)
        folder_button.pack(side=tk.LEFT, padx=(0, 5))

        self.add_flag_options("Suppress Overwrite", self.suppress_overwrite)
        self.add_flag_options("Copy Attributes", self.copy_attributes)

        self.create_tooltip()

    def select_source(self):
        file_path = filedialog.askopenfilenames()
        self.source_path.set(file_path)

    def select_destination(self):
        folder_path = filedialog.askdirectory()
        self.destination_path.set(folder_path)

    def check_for_errors(self):
        # Check if source and destination paths are provided
        if not self.source_path.get() or not self.destination_path.get():
            return "Source and destination paths are required."

        return None

    def check_for_warnings(self):
        if self.suppress_overwrite.get():
            message = "Selecting 'Suppress Overwrite' will automatically replace existing files in the " \
                      "destination folder. Ensure you intended to overwrite these files before proceeding. "
            return self.warn(message)
        return True

    def get_command_string(self):
        command = "copy"

        if self.suppress_overwrite.get():
            command += " /Y"
        else:
            command += " /-Y"

        if self.copy_attributes.get():
            command += " /K"  # Copy attributes, reset read-only attributes

        command += f' "{self.source_path.get()}" "{self.destination_path.get()}"'

        return command

    def create_tooltip(self):
        tooltip = """
Initiates a file copy operation:

Paths:

    - Source: Choose the file to copy using the "Select File(s)" button.
    - Destination: Select the destination folder using the "Select Folder" button.

Options:

    - Suppress Overwrite: Prevents overwriting existing files with the same name.
    - Copy Attributes: Copies additional file information like permissions and timestamps.

Warning!

    - Overwriting existing files without suppression can lead to data loss. Use this option cautiously.
        """
        self.explanatory_tooltip(tooltip)
