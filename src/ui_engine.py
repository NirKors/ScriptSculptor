# ui_engine.py
import tkinter as tk
import tkinter.ttk as ttk
from configparser import ConfigParser
from tkinter import messagebox

from tktooltip import ToolTip

import action_handler
from processing import Processing


class UIEngine:
    def __init__(self, master, config_path):
        """
        Initializes the user interface engine.

        Args:
            master: The root window of the Tkinter application.
            config_path: The path to the configuration directory.
        """

        self.master = master
        self.master.title("ScriptSculptor")
        self.master.configure(bg="black")

        # Read configuration files
        config = ConfigParser()
        config.read(f'{config_path}\\configuration.ini')
        self.dropdown_options = config.get('options', 'dropdown_options').split(', ')
        config.read(f'{config_path}\\settings.ini')
        self.colors = config["colors"]

        # Setup processing and frame order
        self.processing = Processing()
        self.frame_order = []

        # Calculate window dimensions and position
        window_width = 1200
        window_height = 600
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        master.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Create UI elements
        self._create_top_buttons_frame()
        self._create_script_frame()
        self._create_create_script_buttons_frame()

        # Initialize selected frame
        self.selected_frame = None

    def _create_top_buttons_frame(self):
        """
        Creates and configures the frame containing buttons for adding, deleting, and changing frame styles.
        """

        top_buttons_frame = ttk.Frame(self.master, borderwidth=2, relief=self.processing.get_relief(),
                                      style="background.TFrame", name="top_buttons_frame")

        newFrameButton = ttk.Button(top_buttons_frame, text="Add New Frame", command=self.create_new_frame)
        newFrameButton.pack(side=tk.LEFT, padx=5)

        deleteFrameButton = ttk.Button(top_buttons_frame, text="Delete Frame", command=self.delete_frame)
        deleteFrameButton.pack(side=tk.LEFT, padx=5)

        reliefFrameButton = ttk.Button(top_buttons_frame, text="Change Style", command=self.change_style)
        reliefFrameButton.pack(side=tk.LEFT, padx=5)

        top_buttons_frame.pack(anchor="nw", pady=5, padx=5)

    def _create_script_frame(self):
        """
        Creates and configures the frame where the script content is displayed.
        """

        scriptFrame = ttk.Frame(self.master, borderwidth=2, relief=self.processing.get_relief(),
                                style="background.TFrame", name="script_frame")
        scriptFrame.pack(expand=True, fill="both")

        self.scriptFrame = scriptFrame

    def _create_create_script_buttons_frame(self):
        """
        Creates and configures the frame containing buttons for checking errors and creating the script.
        """

        create_script_button_frame = ttk.Frame(self.master, borderwidth=2, relief=self.processing.get_relief(),
                                               style="background.TFrame", name="create_button_frame")

        check_script_button = ttk.Button(create_script_button_frame, text="Check For Errors",
                                         command=lambda: self.check_for_errors())
        check_script_button.pack(side=tk.LEFT, padx=5)

        create_script_button = ttk.Button(create_script_button_frame, text="Create Script",
                                          command=lambda: self.create_script())
        create_script_button.pack(side=tk.LEFT, padx=5)

        create_script_button_frame.pack(anchor="se")

    def delete_frame(self):

        if self.selected_frame:
            self.frame_order.remove(self.selected_frame)
            self.selected_frame.destroy()
            self.selected_frame = None
        return

    def create_new_frame(self):
        # New frame using ttk.Frame with the specified style
        newFrame = ttk.Frame(self.scriptFrame, style="script_frame.TFrame", borderwidth=15,
                             relief=self.processing.get_relief())

        # ttk.Label for consistency
        label = ttk.Label(newFrame, text="Action:")
        label.pack(side=tk.LEFT)

        # ttk.OptionMenu isn't available, keep tk.OptionMenu
        selected_action = tk.StringVar(newFrame)
        selected_action.set(self.dropdown_options[0])  # Set default option
        action_dropdown = tk.OptionMenu(newFrame, selected_action, *self.dropdown_options,
                                        command=lambda selected_action_value:
                                        self.handle_action_selection(selected_action_value, newFrame))
        action_dropdown.pack(side=tk.LEFT, padx=5)

        # Arrow buttons using ttk.Button with the specified style
        button_frame = ttk.Frame(newFrame, style="buttons_frame.TFrame", name="navigation_frame")
        move_up_button = ttk.Button(button_frame, text="↑", style="buttons_frame.TButton",
                                    command=lambda frame=newFrame: self.move_frame_up(frame), width=1)
        move_up_button.pack(side=tk.TOP)
        move_down_button = ttk.Button(button_frame, text="↓", style="buttons_frame.TButton",
                                      command=lambda frame=newFrame: self.move_frame_down(frame), width=1)
        move_down_button.pack(side=tk.TOP)
        button_frame.pack(side=tk.RIGHT)
        button_frame.widgetName = "nav_button_frame"

        # Event binding remains the same
        newFrame.bind("<Button-1>", lambda event, frame=newFrame: self.select_frame(frame))

        # Pack and handle action selection
        newFrame.pack(pady=5, padx=5, fill="x", anchor='n')
        self.handle_action_selection(self.dropdown_options[0], newFrame)
        self.frame_order.append(newFrame)

    def move_frame_up(self, frame):
        # Check if the frame is already at the top
        if frame not in self.frame_order or self.frame_order.index(frame) == 0:
            return

        # Get the index of the frame in the order list
        current_index = self.frame_order.index(frame)

        # Swap the frame with the one above it in the order list
        self.frame_order[current_index], self.frame_order[current_index - 1] = (
            self.frame_order[current_index - 1],
            self.frame_order[current_index],
        )

        # Repack frames based on the updated order
        self.repack_frames()

    def move_frame_down(self, frame):
        # Check if the frame is already at the bottom
        if frame not in self.frame_order or self.frame_order.index(frame) == len(self.frame_order) - 1:
            return

        # Get the index of the frame in the order list
        current_index = self.frame_order.index(frame)

        # Swap the frame with the one below it in the order list
        self.frame_order[current_index], self.frame_order[current_index + 1] = (
            self.frame_order[current_index + 1],
            self.frame_order[current_index],
        )

        # Repack frames based on the updated order
        self.repack_frames()

    def repack_frames(self):
        # Unpack all frames
        for frame in self.frame_order:
            frame.pack_forget()

        # Pack frames in the updated order
        for frame in self.frame_order:
            frame.pack(pady=5, padx=5, fill="x", anchor='n')

    def handle_action_selection(self, selected_action, master_frame):
        # Destroy previous UI components
        action_handler.clear_frame(master_frame)

        # Create an instance of the selected action class
        action = action_handler.create_action(selected_action, self.dropdown_options)
        action.ui_engine = self
        action.parent_frame = master_frame
        action.build_ui()
        master_frame.action = action

        self.bind_children_click(master_frame)

    def change_style(self, parent=None):
        if parent is None:
            parent = self.master
            relief = self.processing.cycle_relief()
        else:
            relief = self.processing.get_relief()

        # Apply relief to the parent frame
        if isinstance(parent, ttk.Frame) or isinstance(parent, tk.Frame):
            parent.configure(relief=relief)

        # Recursively apply relief to children frames
        for child in parent.winfo_children():
            self.change_style(child)

        return

    def bind_children_click(self, widget):
        # Method to bind the click event to all children of a widget
        for child in widget.winfo_children():
            child.bind("<Button-1>", lambda event, frame=widget: self.select_frame(frame))
            self.bind_children_click(child)

    def check_for_errors(self, create_call=False):  # TODO: Split to processing
        errors = []
        values = self.scriptFrame.children.values()
        if not values:
            messagebox.showwarning("Error Check", "No actions found.")
            return False

        for frame in values:
            check = frame.action.check_for_errors()
            if check:
                if check == 2:
                    return False
                else:
                    errors.append(check)
        if errors:
            error_message = "\n\n".join(errors)
            messagebox.showerror("Error Check", error_message)
            return False
        if not errors and not create_call:
            response = messagebox.askquestion("Error Check", "No errors were found. Do you want to create the script?")
            if response == "yes":
                self.create_script()
        return True

    def create_script(self):
        if self.check_for_errors(True):
            try:
                commands = []
                for action in (frame.action for frame in self.frame_order):
                    if not action.check_for_warnings():
                        return
                    commands.append(action.get_command_string())
                self.processing.save_script(commands)

            except Exception as e:
                messagebox.showerror("Error", str(e))
        return

    def select_frame(self, frame):
        # Method to select a frame and highlight it with a different colored border
        if frame == self.selected_frame or frame.widgetName == "nav_button_frame":
            return
        if frame.master != self.scriptFrame:
            self.select_frame(frame.master)
            return

        if self.selected_frame:
            self.selected_frame.configure(style="script_frame.TFrame")  # Reset the previously selected frame color

        self.selected_frame = frame
        frame.configure(style="selected_frame_highlight.TFrame")  # Highlight the selected frame

    def create_tooltip(self, string, widget):
        x_offset = -200
        ToolTip(widget, msg=string, delay=0.3, x_offset=x_offset)


def print_info(master, depth=1):
    for child, value in master.children.items():
        print('\t' * depth + f" {child}")
        if isinstance(value, tk.Frame):
            print_info(value, depth + 1)

    return
