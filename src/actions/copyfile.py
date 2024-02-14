import tkinter as tk
from tkinter import filedialog

from .action import Action


class CopyFile(Action):
    def __init__(self):
        super().__init__()
        self.source_button = None
        self.source_path = tk.StringVar()
        self.destination_path = tk.StringVar()
        self.suppress_overwrite = tk.BooleanVar()
        self.copy_attributes = tk.BooleanVar()

    def build_ui(self):
        parent_frame = self.parent_frame
        # Create and return UI elements for configuring copy options
        source_label = tk.Label(parent_frame, text="Source Path:")
        source_label.pack(side=tk.LEFT, padx=(0, 5))

        source_entry = tk.Entry(parent_frame, textvariable=self.source_path)
        source_entry.pack(side=tk.LEFT, padx=(0, 5))

        source_button = tk.Button(parent_frame, text="Select File(s)", command=self.select_source)
        source_button.pack(side=tk.LEFT, padx=(0, 5))
        self.source_button = source_button

        destination_label = tk.Label(parent_frame, text="Destination Path:")
        destination_label.pack(side=tk.LEFT, padx=(0, 5))

        destination_entry = tk.Entry(parent_frame, textvariable=self.destination_path)
        destination_entry.pack(side=tk.LEFT, padx=(0, 5))

        folder_button = tk.Button(parent_frame, text="Select Folder", command=self.select_destination)
        folder_button.pack(side=tk.LEFT, padx=(0, 5))

        suppress_overwrite_checkbox = tk.Checkbutton(parent_frame, text="Suppress Overwrite",
                                                     variable=self.suppress_overwrite)
        suppress_overwrite_checkbox.pack(side=tk.LEFT)

        copy_attributes_checkbox = tk.Checkbutton(parent_frame, text="Copy Attributes",
                                                  variable=self.copy_attributes)
        copy_attributes_checkbox.pack(side=tk.LEFT)

    def select_source(self):
        file_path = filedialog.askopenfilenames()
        self.source_path.set(file_path)
        # Use the selected file path as needed

    def select_destination(self):
        folder_path = filedialog.askdirectory()
        self.destination_path.set(folder_path)
        # Use the selected folder path as needed

    def check_for_errors(self):
        # Check if source and destination paths are provided
        if not self.source_path.get() or not self.destination_path.get():
            return "Action: Copy\nError: Source and destination paths are required."

        return None

    def get_command_string(self):
        command = "/copy"

        if self.suppress_overwrite.get():
            command += " /Y"
        else:
            command += " /-Y"

        if self.copy_attributes.get():
            command += " /K"  # Copy attributes, reset read-only attributes

        command += f' "{self.source_path.get()}" "{self.destination_path.get()}"'

        return command
