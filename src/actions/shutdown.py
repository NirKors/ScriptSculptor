import tkinter as tk

from .action import Action


class Shutdown(Action):
    def __init__(self, restart, delay, time_unit):
        self.restart = restart
        self.delay = delay
        self.time_unit = time_unit

    def perform_task(self):
        pass

    def build_ui(self, parent_frame):
        print("build_ui")
        return
        # Create and return UI elements for configuring shutdown options
        restart_var = tk.BooleanVar(value=self.restart)
        restart_checkbox = tk.Checkbutton(parent_frame, text="Restart", variable=restart_var)
        restart_checkbox.pack()

        time_label = tk.Label(parent_frame, text="Time:")
        time_label.pack()

        time_entry = tk.Entry(parent_frame, textvariable=tk.StringVar(value=str(self.time_value)))
        time_entry.pack()

        time_unit_options = ['seconds', 'minutes', 'hours', 'days']
        time_unit_dropdown = tk.OptionMenu(parent_frame, tk.StringVar(value=self.time_unit), *time_unit_options)
        time_unit_dropdown.pack()

        return restart_checkbox, time_entry, time_unit_dropdown
