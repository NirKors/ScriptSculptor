import tkinter as tk
from tkinter import ttk

from .action import Action


class Ping(Action):
    def __init__(self):
        super().__init__()
        self.name = "Ping"
        self.data_size = tk.IntVar()
        self.data_size.set(32)
        self.echo_count = tk.IntVar()
        self.echo_count.set(4)
        self.host = tk.StringVar()
        self.continuous_flag = tk.BooleanVar()

    def build_ui(self):
        parent_frame = self.parent_frame
        # Create and return UI elements for configuring copy options
        source_label = ttk.Label(parent_frame, text="Host / IP:")
        source_label.pack(side=tk.LEFT, padx=(0, 5))

        host_entry = ttk.Entry(parent_frame, textvariable=self.host)
        host_entry.pack(side=tk.LEFT, padx=(0, 5), expand=True, fill="x")

        source_label = ttk.Label(parent_frame, text="Number of echo requests:")
        source_label.pack(side=tk.LEFT, padx=(0, 5))
        echo_spinbox = ttk.Spinbox(parent_frame, from_=1, to=9999999, textvariable=self.echo_count, width=15)
        echo_spinbox.pack(side=tk.LEFT, padx=(0, 5))
        self.add_flag_options("Continuous", self.continuous_flag,
                              command=lambda: self.checkbox_changed_entry(self.continuous_flag, echo_spinbox))

        source_label = ttk.Label(parent_frame, text="Data size(b):")
        source_label.pack(side=tk.LEFT, padx=(5, 5))
        data_size_spinbox = ttk.Spinbox(parent_frame, from_=1, to=65500, textvariable=self.data_size, width=5)
        data_size_spinbox.pack(side=tk.LEFT, padx=(0, 5))

        tooltip = """
        This tool allows you to send ping requests to a specified host or IP address to test network 
        connectivity and measure response times. 
        
        Options:
        
            - Host / IP: Enter the hostname or IP address of the target device you want to ping.
            - Number of echo requests: Specify the number of ping packets to send (typically between 1 and 10).
            - Continuous: Enable this option to send pings repeatedly until stopped manually using `CTRL+C`.
            - Data size(b): Define the size of the data payload included in each ping packet. Valid values range from
              1 byte to 65500 bytes.
        
        Additional Notes:
        
            - For basic connectivity testing, using 4 echo requests with the default data size is sufficient.
            - Larger data sizes can provide more accurate measurements of network bandwidth and performance, but might take
              longer to complete.
        """
        self.explanatory_tooltip(tooltip)

    def checkbox_changed_entry(self, flag, entry):
        if not flag.get():
            entry.config(state='normal')
        else:
            entry.config(state='disabled')

    def check_for_warnings(self):
        return True

    def check_for_errors(self):
        if not self.continuous_flag.get():
            try:
                if self.echo_count.get() <= 0:
                    raise Exception
            except:
                return "Invalid echo amount. Please enter a non-negative numerical value."
        try:
            if self.data_size.get() <= 0 or self.data_size.get() > 65500:
                raise Exception
        except:
            return "Invalid data size value. Please enter a non-negative numerical value between 1-65500."

    def get_command_string(self):
        command = "ping "
        command += "/t " if self.continuous_flag.get() else f"/n {self.echo_count.get()} "
        command += f"/l {self.data_size.get()}"
        return command
