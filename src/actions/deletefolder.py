import tkinter as tk
from tkinter import filedialog, ttk

from .action import Action


class DeleteFolder(Action):
    def __init__(self):
        super().__init__()
        self.quiet_mode = tk.BooleanVar()
        self.recursive = tk.BooleanVar()
        self.destination_path = tk.StringVar()
        self.checkbox_qm = None
        self.name = "Delete Folder"

    def build_ui(self):
        parent_frame = self.parent_frame
        # Create and return UI elements for configuring copy options

        destination_label = ttk.Label(parent_frame, text="Deletion Path:")
        destination_label.pack(side=tk.LEFT, padx=(0, 5))

        destination_entry = ttk.Entry(parent_frame, textvariable=self.destination_path)
        destination_entry.pack(side=tk.LEFT, padx=(0, 5), fill="x", expand=True)

        folder_button = tk.Button(parent_frame, text="Select Path", command=self.select_destination)
        folder_button.pack(side=tk.LEFT, padx=(0, 5))

        self.add_flag_options("Recursive", self.recursive, command=self.s_checkbox_changed)
        self.checkbox_qm = self.add_flag_options("Quiet Mode", self.quiet_mode, state="disabled")

        tooltip = """
        This command is used to permanently remove directories from your computer.

        Options:    

            - `Recursive`: Deletes a directory tree (the specified directory and all its subdirectories, including 
                all files).
            - `Quiet Mode`: Specifies quiet mode. Does not prompt for confirmation when deleting a directory tree.
                This parameter works only if `Recursive` is also enabled. 

        Important Points:
        
            - This tool only works on empty directories unless using Recursive. Consider using a tool like
                `Delete Files` to remove files before using this.
            - You can't delete a directory that contains files, including hidden or system files. If you attempt to 
                do so, the following message appears: `The directory is not empty`
            - You can't use this command to delete the current directory. If you attempt to delete the current
                directory, the following error message appears: `The process can't access the file because it is being
                used by another process.` If you receive this error message, you must change to a different directory
                 (not a subdirectory of the current directory), and then try again. 

        Warning!
            - Files and folders deleted with this tool are permanently removed from your device.
            - When you run in quiet mode, the entire directory tree is deleted without confirmation. Make sure that 
                important files are moved or backed up before using this option. """

        self.explanatory_tooltip(tooltip)

    def s_checkbox_changed(self):
        if self.recursive.get():
            self.checkbox_qm.config(state='normal')
        else:
            self.quiet_mode.set(False)
            self.checkbox_qm.config(state='disabled')

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
        if self.quiet_mode.get():
            message = "Enabling `Quiet Mode` and `Recursive` will suppress confirmation prompts when" \
                      " deleting all files, directories, and subdirectories. Ensure absolute certainty before" \
                      " proceeding to avoid unintended data loss."
            if not self.warn(message):
                return False
        elif self.recursive.get():
            message = "Enabling `Recursive` will delete all files, directories, and subdirectories in" \
                      " the specified path. Ensure absolute certainty before proceeding to avoid unintended data loss."
            if not self.warn(message):
                return False
        return True

    def get_command_string(self):
        command = "rmdir"
        if self.recursive.get():
            command += " /s"

        if self.quiet_mode.get():
            command += " /q"

        command += f" {self.destination_path.get()}"
        return command
