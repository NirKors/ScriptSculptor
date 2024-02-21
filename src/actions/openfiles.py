import tkinter as tk
from tkinter import ttk, filedialog

from .action import Action


class OpenFiles(Action):
    def __init__(self):
        super().__init__()
        self.source_path = tk.StringVar()
        self.source_entry = None
        self.name = "Open Files"

    def build_ui(self):
        parent_frame = self.parent_frame
        # Create and return UI elements for configuring copy options
        source_label = ttk.Label(parent_frame, text="Source Path:")
        source_label.pack(side=tk.LEFT, padx=(0, 5))

        self.source_entry = ttk.Entry(parent_frame, textvariable=self.source_path)
        self.source_entry.state(["readonly"])

        self.source_entry.pack(side=tk.LEFT, padx=(0, 5), expand=True, fill="x")

        source_button = tk.Button(parent_frame, text="Select File(s)", command=self.select_source)
        source_button.pack(side=tk.LEFT, padx=(0, 5))

        tooltip = """
        This command is used to open files or directories from your computer.
        """

        self.explanatory_tooltip(tooltip)

    def select_source(self):
        file_path = filedialog.askopenfilenames()
        self.source_path.set(file_path)

    def check_for_errors(self):
        if not self.source_path.get():
            return f"Action: Open Files\nError: Source path is required."

        return None

    def check_for_warnings(self):
        return True

    def get_command_string(self):
        print(self.source_path.get())
        files = self.source_path.get()[1:-1].split(', ')
        if len(files) == 1:
            files[0] = files[0][:-1]

        files = [file[1:-1] for file in files]

        return [f"start \"\" \"{file}\"" for file in files]
