import tkinter as tk
from tkinter import filedialog, ttk

from .action import Action


class DeleteFiles(Action):
    def __init__(self):
        super().__init__()
        self.prompt_confirmation = tk.IntVar()
        self.recursive = tk.BooleanVar()
        self.destination_path = tk.StringVar()
        self.not_flag = tk.BooleanVar()
        self.read_only = tk.BooleanVar()
        self.hidden = tk.BooleanVar()
        self.name = "Delete Files"

    def build_ui(self):
        parent_frame = self.parent_frame
        # Create and return UI elements for configuring copy options

        destination_label = ttk.Label(parent_frame, text="Deletion Path:")
        destination_label.pack(side=tk.LEFT, padx=(0, 5))

        destination_entry = ttk.Entry(parent_frame, textvariable=self.destination_path)
        destination_entry.pack(side=tk.LEFT, padx=(0, 5), fill="x", expand=True)

        folder_button = ttk.Button(parent_frame, style="frame.TButton", text="Select Path", command=self.select_destination)
        folder_button.pack(side=tk.LEFT, padx=(0, 5))

        radio_frame = ttk.Frame(parent_frame)
        radio_frame.pack(side=tk.LEFT, padx=5)
        prompt = ttk.Radiobutton(radio_frame, text="Prompt For Confirmation", variable=self.prompt_confirmation,
                                 value=1)
        prompt.pack(anchor=tk.NW)
        silent = ttk.Radiobutton(radio_frame, text="Quiet Mode", variable=self.prompt_confirmation, value=2)
        silent.pack(anchor=tk.NW)

        self.add_flag_options("Recursive", self.recursive)

        file_options = ttk.Frame(self.parent_frame)
        file_options.pack(side=tk.LEFT, padx=5)

        checkbox_n = ttk.Checkbutton(file_options, text="Not", variable=self.not_flag)
        checkbox_n.pack(side=tk.LEFT)
        checkbox_ro = ttk.Checkbutton(file_options, text="Read Only", variable=self.read_only)
        checkbox_ro.pack(anchor=tk.NW)
        checkbox_h = ttk.Checkbutton(file_options, text="Hidden", variable=self.hidden)
        checkbox_h.pack(anchor=tk.NW)

        self.prompt_confirmation.set(True)

        tooltip = """
        This command is used to permanently delete files and directories from your computer.
        
        Options:    
            
            - `Prompt For Confirmation`: Prompts for confirmation before deleting each file.
            - `Quiet Mode`: Deletes files silently without any prompts.
            - `Recursive`: Recursively deletes files in the directory, and in subdirectories within the specified path.
        
        Important Points:
        
            - Double-check the files and paths you're targeting before deleting.
            - Consider using the `/p` option for confirmation if unsure.
        
        Additional options available in this tool:
        
            - Not: Select files based on the "Not" attribute (opposite of selected attributes).
            - Read Only: Include read-only files in the deletion.
            - Hidden: Include hidden files in the deletion.
        
        Warning!
        
            - Using options like "Not", "Read Only", and "Hidden" can unintentionally target unintended files. Be cautious
              and review your selections before executing the deletion.
        """

        self.explanatory_tooltip(tooltip)

    def select_destination(self):
        folder_path = filedialog.askdirectory()
        self.destination_path.set(folder_path)
        # Use the selected folder path as needed

    def check_for_errors(self):
        # Check if source and destination paths are provided
        if not self.destination_path.get():
            return "Destination path is required."

        return None

    def check_for_warnings(self):
        if self.prompt_confirmation.get() == 2:
            message = "Enabling `Quiet Mode` will suppress confirmation prompts and progress updates during " \
                      "deletions. Ensure absolute certainty before proceeding to avoid unintended data loss. "
            if not self.warn(message):
                return False

        if self.recursive.get():
            message = "Enabling `Recursive` deletion permanently removes all files in the selected folder " \
                      "and the subfolders within the chosen path. Use with caution to avoid unintended data loss. "
            if not self.warn(message):
                return False
        return True

    def get_command_string(self):
        command = "del"
        if self.prompt_confirmation.get() == 1:
            command += " /p"
        else:
            command += " /q"

        if self.recursive.get():
            command += " /s"

        if self.read_only.get():
            if self.not_flag.get():
                command += " /-r"
            else:
                command += " /r"

        if self.hidden.get():
            if self.not_flag.get():
                command += " /-h"
            else:
                command += " /h"

        command += f" {self.destination_path.get()}"
        return command
