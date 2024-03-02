import tkinter as tk
from tkinter import ttk

from .action import Action


class Shutdown(Action):
    def __init__(self):
        super().__init__()
        self.restart = tk.BooleanVar()
        self.force = tk.BooleanVar()
        self.delay = tk.IntVar()
        self.time_unit = tk.StringVar()

        self.time_unit.set('Seconds')
        self.delay.set(0)
        self.name = "Shutdown"

    def build_ui(self):
        parent_frame = self.parent_frame
        # Create and return UI elements for configuring shutdown options
        time_label = ttk.Label(parent_frame, text="Time before shutdown:")
        time_label.pack(side=tk.LEFT, padx=(0, 5))

        time_entry = ttk.Spinbox(parent_frame, textvariable=self.delay, from_=0, to=9999999)
        time_entry.pack(side=tk.LEFT, padx=(0, 5))

        time_unit_options = ['Seconds', 'Minutes', 'Hours', 'Days']
        time_unit_dropdown = ttk.OptionMenu(parent_frame, self.time_unit, *time_unit_options)
        time_unit_dropdown.pack(side=tk.LEFT, padx=(0, 5))

        self.add_flag_options("Restart", self.restart)
        self.add_flag_options("Force Shutdown", self.force)

        tooltip = """
        This command shuts down your computer.
        
        Options:
        
            - Force Shutdown: Terminates all running programs and processes immediately.
              Use with caution, as unsaved data may be lost.
            - Restart: Shuts down the computer and automatically restarts it.
            - Log Off: Closes all open programs and user sessions, but keeps the computer running.
        
        Important Points:
        
            - Save any unsaved work before proceeding, as this action cannot be undone.
            - If you're not certain about shutting down, consider using the Log Off option instead.
            - Force Shutdown should only be used as a last resort, as it can potentially lead to data corruption.
        
        Warning!
                
            - Force Shutdown can cause data loss if unsaved files are open.
            - Always attempt a normal shutdown or log off before resorting to Force Shutdown.
        """

        self.explanatory_tooltip(tooltip)

    def check_for_errors(self):
        # Check if delay is a valid numerical value
        try:
            if self.delay.get() < 0:
                raise ValueError

        except:
            return "Invalid delay value. Please enter a non-negative numerical value."

        return None

    def check_for_warnings(self):
        if self.force.get():
            message = "Forcing your computer to shut down can corrupt open files and unsaved work."
            return self.warn(message)
        return True

    def get_command_string(self):
        delay_value = int(self.delay.get())
        restart_value = ' /r' if self.restart.get() else ' /s'
        force_value = ' /f' if self.force.get() else ''
        time_unit = self.time_unit.get()

        if time_unit == "Minutes":
            delay_value *= 60
        if time_unit == "Hours":
            delay_value *= 60 * 60
        if time_unit == "Days":
            delay_value *= 60 * 60 * 24

        return f"shutdown{force_value}{restart_value} /t {delay_value}"
