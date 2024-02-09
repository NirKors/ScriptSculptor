# ui_engine.py
import tkinter as tk
from configparser import ConfigParser

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

        window_width = 800
        window_height = 600
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        master.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        top_buttons_frame = tk.Frame(self.master, borderwidth=2, relief=self.processing.get_relief(),
                                     background=self.colors["buttons_frame"], name="top_buttons_frame")

        newFrameButton = tk.Button(top_buttons_frame, text="Add New Frame", command=self.createNewFrame)
        newFrameButton.pack(side=tk.LEFT, padx=5)

        deleteFrameButton = tk.Button(top_buttons_frame, text="Delete Frame", command=self.deleteFrame)
        deleteFrameButton.pack(side=tk.LEFT, padx=5)

        reliefFrameButton = tk.Button(top_buttons_frame, text="Change Style", command=self.changeStyle)
        reliefFrameButton.pack(side=tk.LEFT, padx=5)

        top_buttons_frame.pack(anchor="nw", pady=5, padx=5)

        self.selected_frame = None

        scriptFrame = tk.Frame(self.master, borderwidth=2, relief=self.processing.get_relief(),
                               background=self.colors["background"], name="script_frame")
        scriptFrame.pack(expand=True, fill="both")

        self.scriptFrame = scriptFrame

        create_script_button_frame = tk.Frame(self.master, borderwidth=2, relief=self.processing.get_relief(),
                                              background=self.colors["buttons_frame"], name="create_button_frame")
        create_script_button = tk.Button(create_script_button_frame, text="Create script",
                                         command=lambda: self.sendInfo())
        create_script_button.pack(side=tk.LEFT, padx=5)
        create_script_button_frame.pack(anchor="se")

    def deleteFrame(self):

        if self.selected_frame:
            self.selected_frame.destroy()
            self.selected_frame = None
        return

    def createNewFrame(self):
        # New frame
        newFrame = tk.Frame(self.scriptFrame, borderwidth=15, relief=self.processing.get_relief(),
                            background=self.colors["script_frame"])

        label = tk.Label(newFrame, text="Placeholder label", padx=10)
        label.pack(side=tk.LEFT)

        # Dropdown Menu
        selected_action = tk.StringVar(newFrame)
        selected_action.set(self.dropdown_options[0])  # Set default option
        action_dropdown = tk.OptionMenu(newFrame, selected_action, *self.dropdown_options,
                                        command=lambda selected_action_value:
                                        action_handler.handle_action_selection(selected_action_value, newFrame))
        action_dropdown.pack(side=tk.LEFT)

        newButton = tk.Button(newFrame, text="X")
        newButton.pack(side=tk.RIGHT)

        # Bind click event to the frame
        newFrame.bind("<Button-1>", lambda event, frame=newFrame: self.selectFrame(frame))

        # Bind click event to its children
        self.bind_children_click(newFrame)
        newFrame.pack(pady=5, padx=5, fill="x", anchor='n')
        action_handler.handle_action_selection(self.dropdown_options[0], newFrame)

    def changeStyle(self, parent=None):
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
            self.changeStyle(child)

        return

    def bind_children_click(self, widget):
        # Method to bind the click event to all children of a widget
        for child in widget.winfo_children():
            child.bind("<Button-1>", lambda event, frame=widget: self.selectFrame(frame))
            self.bind_children_click(child)

    def sendInfo(self):
        for frame in self.scriptFrame.children:
            print(frame)
        return

    def selectFrame(self, frame):
        # Method to select a frame and highlight it with a different colored border
        if self.selected_frame:
            self.selected_frame.configure(bg=self.colors["script_frame"])  # Reset the previously selected frame color

        self.selected_frame = frame
        frame.configure(bg=self.colors["selected_frame_highlight"])  # Highlight the selected frame


def printinfo(master, depth=1):
    for child, value in master.children.items():
        print('\t' * depth + f" {child}")
        if isinstance(value, tk.Frame):
            printinfo(value, depth + 1)

    return
