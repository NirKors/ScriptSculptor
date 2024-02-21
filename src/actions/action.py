import tkinter as tk
from tkinter import ttk, messagebox





class Action:
    def __init__(self):
        self.ui_engine = None
        self.parent_frame = None
        self.options_frame = None

    def build_ui(self):
        """
        Builds the user interface elements for configuring the action.

        Subclasses must implement this method to create and pack UI elements necessary for configuring the action's
        parameters. This method is called when initializing the action.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.

        """
        raise NotImplementedError("Subclasses must implement build_ui method")

    def add_flag_options(self, text, variable, **kwargs):
        """
        Adds a checkbutton representing a flag option to the UI.

        Args:
            text (str): The text to display next to the checkbutton.
            variable (tk.BooleanVar): The BooleanVar object tracking the state of the checkbutton.
            **kwargs: Additional keyword arguments to pass to the Checkbutton constructor.

        Returns:
            ttk.Checkbutton: The created checkbutton widget.
        """

        if not self.options_frame:
            self.options_frame = ttk.Frame(self.parent_frame)
            self.options_frame.pack(side=tk.LEFT)

        saved_var = ttk.Checkbutton(self.options_frame, text=text, variable=variable, **kwargs)
        saved_var.pack(anchor=tk.NW)
        return saved_var

    def check_for_warnings(self):
        """
        Checks for potential warnings before executing the action.

        This method is called before performing the action to identify potential issues or risky configurations. Subclasses
        should implement their own logic based on the specific action requirements.

        Returns:
            bool: True if no warnings are found or warnings are acknowledged; False otherwise.

        Example:
            In the context of deleting files or directories, the method checks for the combination of `Quiet Mode` and
            `Recursive` settings. If both are enabled, it suppresses confirmation prompts, potentially leading to unintended
            data loss. The method warns the user and returns False if these conditions are detected.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.

        """
        raise NotImplementedError("Subclasses must implement build_ui method")

    def check_for_errors(self):
        """
        Checks for potential errors in the action configuration.

        Subclasses must implement this method to perform specific error checks based on the configured parameters. This
        method is called before executing the action to identify and handle errors.

        Returns:
            str or None: An error message string if an error is detected, or None if no errors are found.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.

        """
        raise NotImplementedError("Subclasses must implement check_for_errors method")

    def get_command_string(self):
        """
        Generates the command string for executing the action.

        Subclasses must implement this method to construct the appropriate command string based on the configured
        parameters. This method is called when generating the final command to execute the action.

        Returns:
            str: The command string for executing the action.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.

        """
        raise NotImplementedError("Subclasses must implement get_command_string method")

    def explanatory_tooltip(self, text):
        """
        Displays an explanatory tooltip with a question mark icon.

        Creates a frame containing a question mark icon and binds a tooltip with explanatory text to it.

        Args:
            text (str): The explanatory text to be displayed in the tooltip.

        """
        # Create the tooltip frame
        tooltip_frame = ttk.Frame(self.parent_frame, style="buttons_frame.TFrame", width=20, height=20, borderwidth=1)
        tooltip_frame.pack(side="right", padx=5)

        # Add a question mark label
        tooltip_label = ttk.Label(tooltip_frame, text="?", font=("Arial", 15),
                                  foreground="blue")  # Adjust font and color as needed
        tooltip_label.pack(expand=True, fill="both")  # Center the label within the frame
        self.ui_engine.create_tooltip(text, tooltip_frame)

    def warn(self, message):
        """
        Displays a warning message dialog with an OK and Cancel option.

        Args:
            message (str): The warning message to be displayed.

        Returns:
            bool: True if the user clicks OK, False if the user clicks Cancel.

        """
        return messagebox.askokcancel(title=f"Warning - {self.name}", message=message, icon=messagebox.WARNING)
