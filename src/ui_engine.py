# ui_engine.py
import tkinter as tk
from configparser import ConfigParser
from tkinter import messagebox

import action_handler
from processing import Processing


class UIEngine:
    def __init__(self, master):
        self.master = master
        master.title("ScriptSculptor")
        master.configure(bg="black")

        config = ConfigParser()
        config.read('config/configuration.ini')
        self.dropdown_options = config.get('options', 'dropdown_options').split(', ')
        config.read('config/settings.ini')

        self.colors = config["colors"]
        self.processing = Processing()
        self.frame_order = []

        window_width = 1200
        window_height = 600
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        master.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        top_buttons_frame = tk.Frame(self.master, borderwidth=2, relief=self.processing.get_relief(),
                                     background=self.colors["buttons_frame"], name="top_buttons_frame")

        newFrameButton = tk.Button(top_buttons_frame, text="Add New Frame", command=self.create_new_frame)
        newFrameButton.pack(side=tk.LEFT, padx=5)

        deleteFrameButton = tk.Button(top_buttons_frame, text="Delete Frame", command=self.delete_frame)
        deleteFrameButton.pack(side=tk.LEFT, padx=5)

        reliefFrameButton = tk.Button(top_buttons_frame, text="Change Style", command=self.change_style)
        reliefFrameButton.pack(side=tk.LEFT, padx=5)

        top_buttons_frame.pack(anchor="nw", pady=5, padx=5)

        self.selected_frame = None

        scriptFrame = tk.Frame(self.master, borderwidth=2, relief=self.processing.get_relief(),
                               background=self.colors["background"], name="script_frame")
        scriptFrame.pack(expand=True, fill="both")

        self.scriptFrame = scriptFrame

        create_script_button_frame = tk.Frame(self.master, borderwidth=2, relief=self.processing.get_relief(),
                                              background=self.colors["buttons_frame"], name="create_button_frame")
        check_script_button = tk.Button(create_script_button_frame, text="Check For Errors",
                                        command=lambda: self.check_for_errors())
        check_script_button.pack(side=tk.LEFT, padx=5)
        create_script_button = tk.Button(create_script_button_frame, text="Create Script",
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
        # New frame
        newFrame = tk.Frame(self.scriptFrame, borderwidth=15, relief=self.processing.get_relief(),
                            background=self.colors["script_frame"])

        label = tk.Label(newFrame, text="Action:", padx=10)
        label.pack(side=tk.LEFT)

        # Dropdown Menu
        selected_action = tk.StringVar(newFrame)
        selected_action.set(self.dropdown_options[0])  # Set default option
        action_dropdown = tk.OptionMenu(newFrame, selected_action, *self.dropdown_options,
                                        command=lambda selected_action_value:
                                        self.handle_action_selection(selected_action_value, newFrame))
        action_dropdown.pack(side=tk.LEFT, padx=5)

        # Arrow buttons for reorganizing frames
        button_frame = tk.Frame(newFrame, name="navigation_frame")
        move_up_button = tk.Button(button_frame, text="↑", command=lambda frame=newFrame: self.move_frame_up(frame),
                                   font="bold")
        move_up_button.pack(side=tk.TOP)
        move_down_button = tk.Button(button_frame, text="↓", command=lambda frame=newFrame: self.move_frame_down(frame),
                                     font="bold")
        move_down_button.pack(side=tk.TOP)
        button_frame.pack(side=tk.RIGHT)
        button_frame.widgetName = "nav_button_frame"

        # Bind click event to the frame
        newFrame.bind("<Button-1>", lambda event, frame=newFrame: self.select_frame(frame))

        # Bind click event to its children
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

    def repack_frames(self):
        # Unpack all frames
        for frame in self.frame_order:
            frame.pack_forget()

        # Pack frames in the updated order
        for frame in self.frame_order:
            frame.pack(pady=5, padx=5, fill="x", anchor='n')

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

    def handle_action_selection(self, selected_action, master_frame):
        # Destroy previous UI components
        action_handler.clear_frame(master_frame)

        # Create an instance of the selected action class
        action = action_handler.create_action(selected_action)
        action.build_ui(master_frame)
        master_frame.action = action

        self.bind_children_click(master_frame)

    def change_style(self, parent=None):
        if parent is None:
            parent = self.master
            relief = self.processing.cycle_relief()
        else:
            relief = self.processing.get_relief()

        # Apply relief to the parent frame
        if isinstance(parent, tk.Frame):
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

    def check_for_errors(self, create_call=False):
        errors = []
        values = self.scriptFrame.children.values()
        if not values:
            messagebox.showwarning("Error Check", "No actions found.")
            return False

        for frame in values:
            check = frame.action.check_for_errors()
            if check:
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
                for frame in self.scriptFrame.children.values():
                    commands.append(frame.action.get_command_string())
                self.processing.save_script(commands)

            except Exception as e:
                messagebox.showerror("Error", str(e))
        return

    def select_frame(self, frame):
        # Method to select a frame and highlight it with a different colored border
        if frame.widgetName == "nav_button_frame":
            return
        if frame.master != self.scriptFrame:
            self.select_frame(frame.master)
            return

        if self.selected_frame:
            self.selected_frame.configure(bg=self.colors["script_frame"])  # Reset the previously selected frame color

        self.selected_frame = frame
        frame.configure(bg=self.colors["selected_frame_highlight"])  # Highlight the selected frame


def print_info(master, depth=1):
    for child, value in master.children.items():
        print('\t' * depth + f" {child}")
        if isinstance(value, tk.Frame):
            print_info(value, depth + 1)

    return
