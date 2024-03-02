import tkinter as tk
from tkinter import ttk, filedialog

from .action import Action


class OpenFiles(Action):
    def __init__(self):
        super().__init__()
        self.source_path = tk.StringVar()
        self.source_entry = None
        self.name = "Open Files"
        self.source_button = None

    def build_ui(self):
        parent_frame = self.parent_frame
        # Create and return UI elements for configuring copy options
        source_label = ttk.Label(parent_frame, text="Source Path:")
        source_label.pack(side=tk.LEFT, padx=(0, 5))

        self.source_entry = ttk.Entry(parent_frame, textvariable=self.source_path)
        self.source_entry.state(["readonly"])

        self.source_entry.pack(side=tk.LEFT, padx=(0, 5), expand=True, fill="x")

        self.source_button = ttk.Button(parent_frame, style="frame.TButton", text="Select File(s)", command=self.select_source)
        self.source_button.pack(side=tk.LEFT, padx=(0, 5))

        self.create_tooltip()

    def select_source(self):
        file_path = filedialog.askopenfilenames()
        self.source_path.set(file_path)

    def check_for_errors(self):
        if not self.source_path.get():
            return "Source path is required."

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

    def create_tooltip(self):
        tooltip = """
        This command is used to open files in your computer using the default program set in your computer.
        """

        self.explanatory_tooltip(tooltip)
