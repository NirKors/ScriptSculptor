import tkinter as tk
from tkinter import filedialog

from .copyfile import CopyFile


class CopyFolder(CopyFile):

    def __init__(self):
        super().__init__()
        self.copy_subdirectories = tk.BooleanVar()

    def build_ui(self):
        parent_frame = self.parent_frame
        super().build_ui()
        self.source_button["text"] = "Select Folder"

        copy_subdirectories_checkbox = tk.Checkbutton(parent_frame, text="Copy Subdirectories",
                                                      variable=self.copy_subdirectories)
        copy_subdirectories_checkbox.pack(side=tk.LEFT)

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
