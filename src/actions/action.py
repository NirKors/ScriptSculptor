from tkinter import ttk


class Action:
    def __init__(self):
        self.ui_engine = None
        self.parent_frame = None

    def build_ui(self):
        raise NotImplementedError("Subclasses must implement build_ui method")

    def check_for_errors(self):
        raise NotImplementedError("Subclasses must implement build_ui method")

    def get_command_string(self):
        raise NotImplementedError("Subclasses must implement get_command_string method")

    def explanatory_tooltip(self, text):
        # Create the tooltip frame
        tooltip_frame = ttk.Frame(self.parent_frame, style="buttons_frame.TFrame", width=20, height=20, borderwidth=1)
        tooltip_frame.pack(side="right", padx=5)

        # Add a question mark label
        tooltip_label = ttk.Label(tooltip_frame, text="?", font=("Arial", 15),
                                  foreground="blue")  # Adjust font and color as needed
        tooltip_label.pack(expand=True, fill="both")  # Center the label within the frame
        self.ui_engine.create_tooltip(text, tooltip_frame)
