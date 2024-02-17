import tkinter as tk
from .action import Action


class CreateFolder(Action):
    def __init__(self):
        super().__init__()
        self.file_or_folder = tk.StringVar(value="File")  # Default to creating a file
        self.name = tk.StringVar(value="New File")
        self.location = tk.StringVar()

    def build_ui(self):
        parent_frame = self.parent_frame
        # Create and return UI elements for configuring the create options
        create_label = tk.Label(parent_frame, text="Create:")
        create_label.pack(side=tk.LEFT, padx=(0, 5))

        create_options = ['File', 'Folder']
        create_dropdown = tk.OptionMenu(parent_frame, self.file_or_folder, *create_options)
        create_dropdown.pack(side=tk.LEFT, padx=(0, 5))

        name_label = tk.Label(parent_frame, text="Name:")
        name_label.pack(side=tk.LEFT, padx=(0, 5))

        name_entry = tk.Entry(parent_frame, textvariable=self.name)
        name_entry.pack(side=tk.LEFT, padx=(0, 5))

        location_label = tk.Label(parent_frame, text="Location:")
        location_label.pack(side=tk.LEFT, padx=(0, 5))

        location_entry = tk.Entry(parent_frame, textvariable=self.location)
        location_entry.pack(side=tk.LEFT, padx=(0, 5))


    def check_for_errors(self):
        # Check if name and location are provided
        if not self.name.get() or not self.location.get():
            return "Action: Create\nError: Name and location are required."

        return None

    def get_command_string(self):
        command = "/create"

        if self.file_or_folder.get() == "File":
            command += " file"
        else:
            command += " folder"

        command += f' "{self.name.get()}" "{self.location.get()}"'

        return command


