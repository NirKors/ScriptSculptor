import tkinter as tk
from tkinter import filedialog, ttk

from .action import Action


class DeleteFiles(Action):
    def __init__(self):
        super().__init__()
        self.recursive = tk.BooleanVar()
        self.checkbox_frame = None
        self.prompt_confirmation = None
        self.destination_path = tk.StringVar()

    def build_ui(self):
        parent_frame = self.parent_frame
        # Create and return UI elements for configuring copy options

        destination_label = ttk.Label(parent_frame, text="Deletion Path:")
        destination_label.pack(side=tk.LEFT, padx=(0, 5))

        destination_entry = tk.Entry(parent_frame, textvariable=self.destination_path)
        destination_entry.pack(side=tk.LEFT, padx=(0, 5))

        folder_button = tk.Button(parent_frame, text="Select Path", command=self.select_destination)
        folder_button.pack(side=tk.LEFT, padx=(0, 5))

        self.add_flag_options("Recursive", self.recursive)

        tooltip = "***Warning: If you use del to delete a file from your disk, you can't retrieve it."

        self.explanatory_tooltip(tooltip)

    def select_destination(self):
        folder_path = filedialog.askdirectory()
        self.destination_path.set(folder_path)
        # Use the selected folder path as needed

    def check_for_errors(self):
        # Check if source and destination paths are provided
        if not self.destination_path.get():
            return f"Action: Delete Files\nError: Destination paths are required."

        return None

    def get_command_string(self):
        command = "/copy"

        print(self.recursive.get())

        return command

    def create_tooltip(self):
        tooltip = """
        Initiates a file copy operation:

          - Source: Choose the file to copy using the "Select File(s)" button.
          - Destination: Select the destination folder using the "Select Folder" button.

          Options:

            - Suppress Overwrite: Prevents overwriting existing files with the same name.
            - Copy Attributes: Copies additional file information like permissions and timestamps.

          **Warning:** Overwriting existing files without suppression can lead to data loss. Use this option cautiously.
        """
        self.explanatory_tooltip(tooltip)
