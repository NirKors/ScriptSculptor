import tkinter as tk
from .action import Action


class Shutdown(Action):
    def __init__(self):
        self.restart = tk.BooleanVar()
        self.delay = tk.StringVar()
        self.time_unit = tk.StringVar()

    def build_ui(self, parent_frame):
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
        restart_checkbox = tk.Checkbutton(parent_frame, text="Restart", variable=self.restart)
        restart_checkbox.pack(side=tk.LEFT)

        return restart_checkbox, time_entry, time_unit_dropdown

    def check_for_errors(self):
        # Check if delay is a valid numerical value
        try:
            if float(self.delay.get()) < 0:
                raise ValueError

        except ValueError:
            return "Action: Shutdown\n\tError: Invalid delay value. Please enter a non-negative numerical value."
        return None

    def get_command_string(self):
        delay_value = int(self.delay.get())
        restart_value = '/r' if self.restart.get() else '/s'
        time_unit = self.time_unit.get()

        if time_unit == "Minutes":
            delay_value *= 60
        if time_unit == "Hours":
            delay_value *= 60 * 60
        if time_unit == "Days":
            delay_value *= 60 * 60 * 24

        return f"/shutdown {restart_value} /t {delay_value}"
