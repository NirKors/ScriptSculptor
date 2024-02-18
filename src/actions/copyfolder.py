import tkinter as tk
from tkinter import filedialog

from .copyfiles import CopyFiles


class CopyFolder(CopyFiles):

    def __init__(self):
        super().__init__()
        self.copy_subdirectories = tk.BooleanVar()

    def build_ui(self):
        super().build_ui()
        parent_frame = self.parent_frame
        self.source_button["text"] = "Select Folder"

        copy_subdirectories_checkbox = tk.Checkbutton(self.checkbox_frame, text="Copy Subdirectories",
                                                      variable=self.copy_subdirectories)
        copy_subdirectories_checkbox.pack(anchor=tk.NW)

    def select_source(self):
        file_path = filedialog.askdirectory()
        self.source_path.set(file_path)
        # Use the selected file path as needed

    def get_command_string(self):
        command = "/copy"

        if self.suppress_overwrite.get():
            command += " /Y"
        else:
            command += " /-Y"

        if self.copy_attributes.get():
            command += " /K"  # Copy attributes, reset read-only attributes

        if self.copy_subdirectories.get():
            command += " /S"

        command += f' "{self.source_path.get()}" "{self.destination_path.get()}"'

        return command

    def create_tooltip(self):
        tooltip = """
        Initiates a folder copy operation:
        
          - Source: Choose the folder to copy using the "Select Folder" button.
          - Destination: Select the destination folder using the "Select Folder" button.
        
          Options:
        
            - Suppress Overwrite: Prevents overwriting existing files with the same name.
            - Copy Subdirectories: Includes subfolders and their contents within the source folder.
            - Copy Attributes: Copies additional file information like permissions and timestamps.
        
          **Warning:** Overwriting existing files without suppression can lead to data loss. Use this option cautiously.
        """
        self.explanatory_tooltip(tooltip)
