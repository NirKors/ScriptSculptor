import tkinter as tk
from .action import Action


class Shutdown(Action):
    def __init__(self):
        self.restart = tk.BooleanVar()
        self.delay = tk.StringVar()
        self.time_unit = tk.StringVar()

    def build_ui(self, parent_frame):
        print("build_ui")
        # Create and return UI elements for configuring shutdown options

        time_label = tk.Label(parent_frame, text="Time before shutdown:")
        time_label.pack(side=tk.LEFT, padx=(0, 5))

        time_entry = tk.Entry(parent_frame, textvariable=self.delay)
        time_entry.pack(side=tk.LEFT, padx=(0, 5))

        time_unit_options = ['Seconds', 'Minutes', 'Hours', 'Days']
        self.time_unit.set('Minutes')  # Set the default value to "Minutes"
        time_unit_dropdown = tk.OptionMenu(parent_frame, self.time_unit, *time_unit_options)
        time_unit_dropdown.pack(side=tk.LEFT, padx=(0, 5))

        restart_var = tk.BooleanVar(parent_frame, value=bool(self.restart.get()))
        restart_checkbox = tk.Checkbutton(parent_frame, text="Restart", variable=restart_var)
        restart_checkbox.pack(side=tk.LEFT)

        return restart_checkbox, time_entry, time_unit_dropdown

    def perform_task(self):
        pass
