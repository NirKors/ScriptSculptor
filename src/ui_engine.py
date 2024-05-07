# ui_engine.py
import os
import textwrap
import tkinter as tk
import tkinter.ttk as ttk
from configparser import ConfigParser
from tkinter import messagebox, font

import sv_ttk
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
        sv_ttk.set_theme("dark")
        self.style()

    def style(self):
        """
        Configures the style of various UI elements in the application.

        This function uses the `ttk.Style` class to customize the appearance of frames, buttons, labels, and other widgets.
        It leverages a color dictionary (`self.colors`) to define consistent color schemes throughout the UI.
        """
        colors = self.colors
        style = ttk.Style()

        style.theme_use("default")
        style.configure("buttons_frame.TFrame", padding=6, background=colors["buttons_frame"])
        style.configure("background.TFrame", padding=6, background=colors["background"])
        style.configure("script_frame.TFrame", padding=6, background=colors["script_frame"])
        style.configure("selected_frame_highlight.TFrame", padding=6, background=colors["selected_frame_highlight"])
        style.configure("TLabel", background=colors["labels"])
        style.configure("TRadiobutton", background=colors["radio_button"])
        style.configure("QuestionMark.TLabel", background=colors["question_mark_bg"],
                        foreground=colors["question_mark_fg"])
        style.configure("TCheckbutton", background="white")

        style.configure("TCombobox",
                        # selectbackground=colors["combobox_selectbackground"],
                        # fieldbackground=colors["combobox_fieldbackground"],
                        foreground=colors["combobox_background"])
        self.master.option_add("*TCombobox*Listbox*Background", colors["combobox_lb_bg"])
        self.master.option_add('*TCombobox*Listbox*Foreground', colors["combobox_lb_fg"])

        style.map("TButton",
                  background=[("active", colors["TButton_bg_active"]), ("!active", colors["TButton_bg_inactive"])],
                  foreground=[("active", colors["TButton_fg_active"]), ("!active", colors["TButton_fg_inactive"])])

        style.configure("frame.TButton")
        style.map("frame.TButton",
                  background=[("active", colors["script_frame.TButton_bg_active"]),
                              ("!active", colors["script_frame.TButton_bg_inactive"])],
                  foreground=[("active", colors["script_frame.TButton_fg_active"]),
                              ("!active", colors["script_frame.TButton_fg_inactive"])])

    def _create_top_buttons_frame(self):
        """
        Creates and configures the frame containing buttons for adding, deleting, and changing frame styles.
        """
        tooltip_delay = 0.7

        top_buttons_frame = ttk.Frame(self.master, borderwidth=0, relief=self.processing.get_relief(),
                                      style="background.TFrame", name="top_buttons_frame")

        newFrameButton = ttk.Button(top_buttons_frame, text="New Action", command=self.create_new_frame)
        newFrameButton.pack(side=tk.LEFT, padx=5)
        tooltip = """
        Click this button to add a new action frame.
        Each frame represents a specific action to be executed.
        Customize the settings for each action in its respective frame.
        """
        self.create_tooltip(tooltip, newFrameButton, delay=tooltip_delay)

        deleteFrameButton = ttk.Button(top_buttons_frame, text="Delete Action", command=self.delete_frame)
        deleteFrameButton.pack(side=tk.LEFT, padx=5)
        tooltip = """
        Click this button to delete the currently selected action frame.
        """
        self.create_tooltip(tooltip, deleteFrameButton, delay=tooltip_delay)

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

        create_script_button_frame = ttk.Frame(self.master, borderwidth=0, relief=self.processing.get_relief(),
                                               style="background.TFrame", name="create_button_frame")

        check_script_button = ttk.Button(create_script_button_frame, text="Check For Errors",
                                         command=lambda: self.check_for_errors())
        check_script_button.pack(side=tk.LEFT, padx=5)

        copy_script_button = ttk.Button(create_script_button_frame, text="Copy Script to Clipboard",
                                        command=lambda: self.create_script(True, copy_script_button), width=22)

        copy_script_button.pack(side=tk.LEFT, padx=5)

        create_script_button = ttk.Button(create_script_button_frame, text="Create Script File",
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
        """
        Creates a new frame within the script frame and populates it with UI elements.

        This function generates a new ttk.Frame instance with a predefined style ("script_frame.TFrame"), sets border width,
        and adjusts relief based on the `self.processing.get_relief()` method.

        It then adds the following UI elements to the new frame:

        - Label: A label displaying "Action:".
        - OptionMenu: A dropdown menu populated with options from the `self.dropdown_options` list. It utilizes a `tk.StringVar`
          to store the selected option and calls `self.handle_action_selection` when the selection changes.
        - Navigation buttons: These buttons are added using the `self.add_nav_buttons` method (implementation not shown).

        Finally, the function binds a click event to the new frame, triggering the `self.select_frame` method with the frame as an argument.
        The new frame is packed with padding, fills horizontally, and is anchored to the north.

        Additionally, it calls `self.handle_action_selection` with the default option and appends the newly created frame to the `self.frame_order` list.
        """
        newFrame = ttk.Frame(self.scriptFrame, style="script_frame.TFrame", borderwidth=15,
                             relief=self.processing.get_relief())

        label = ttk.Label(newFrame, text="Action:")
        label.pack(side=tk.LEFT)

        selected_action = tk.StringVar(newFrame)
        selected_action.set(self.dropdown_options[0])  # Set default option
        action_dropdown = ttk.OptionMenu(newFrame, selected_action, *self.dropdown_options,
                                         command=lambda selected_action_value: self.handle_action_selection(
                                             selected_action_value, newFrame))
        action_dropdown.pack(side=tk.LEFT, padx=5)

        self.add_nav_buttons(newFrame)

        # Event binding remains the same
        newFrame.bind("<Button-1>", lambda event, frame=newFrame: self.select_frame(frame))

        # Pack and handle action selection
        newFrame.pack(pady=5, padx=5, fill="x", anchor='n')
        self.handle_action_selection(self.dropdown_options[0], newFrame)
        self.frame_order.append(newFrame)

    def add_nav_buttons(self, master_frame):
        """
        Creates a frame containing up and down arrow buttons for navigation within the master frame.
        """
        # Arrow buttons using ttk.Button with the specified style
        button_frame = ttk.Frame(master_frame, style="buttons_frame.TFrame", name="navigation_frame")
        move_up_button = ttk.Button(button_frame, text="↑", style="buttons_frame.TButton",
                                    command=lambda frame=master_frame: self.move_frame_up(frame), width=1)
        move_up_button.pack(side=tk.TOP)
        move_down_button = ttk.Button(button_frame, text="↓", style="buttons_frame.TButton",
                                      command=lambda frame=master_frame: self.move_frame_down(frame), width=1)
        move_down_button.pack(side=tk.TOP)
        button_frame.pack(side=tk.RIGHT)
        button_frame.widgetName = "nav_button_frame"

    def move_frame_up(self, frame):
        # Check if the frame is already at the top
        if frame not in self.frame_order or self.frame_order.index(frame) == 0:
            return

        # Get the index of the frame in the order list
        current_index = self.frame_order.index(frame)

        # Swap the frame with the one above it in the order list
        self.frame_order[current_index], self.frame_order[current_index - 1] = (
            self.frame_order[current_index - 1], self.frame_order[current_index],)

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
            self.frame_order[current_index + 1], self.frame_order[current_index],)

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

    def check_for_errors(self, create_call=False):
        """
        Check for errors in the script and provide appropriate user feedback.

        Parameters:
        - create_call (bool): A boolean flag indicating whether the method is called during script creation.

        Returns:
        - bool: True if no errors are found, False otherwise.

        This method checks if there are any actions in the script. If none are found, a warning is displayed,
        and the method returns False.

        It then delegates the error checking to the `processing` module, collecting any errors encountered.
        If errors are found, an error message displaying the details of each error is shown, and the method returns False.

        If no errors are found, and the method is not called during script creation (`create_call` is False),
        a confirmation dialog is presented to the user, asking if they want to proceed with script creation.
        If the user chooses to proceed, the method calls the `create_script` method.
        """
        # Check if there are scripts at all:
        values = self.scriptFrame.children.values()
        if not values:
            messagebox.showwarning("Error Check", "No actions found.")
            return False

        errors = self.processing.check_for_errors(values)
        if errors:
            error_message = "\n\n".join(errors)
            messagebox.showerror("Error Check", error_message)
            return False
        if not errors and not create_call:
            response = messagebox.askquestion("Error Check", "No errors were found. Do you want to create the script?")
            if response == "yes":
                self.create_script()
        return True

    def create_script(self, copy=False, copy_button=None):
        if self.check_for_errors(True):
            try:
                commands = []
                for action in (frame.action for frame in self.frame_order):
                    if not action.check_for_warnings():
                        return

                    command_result = action.get_command_string()
                    if isinstance(command_result, str):
                        commands.append(command_result)
                    else:  # Assuming it's a list of strings
                        commands.extend(command_result)
                if not copy:
                    save_script(commands)
                    current_path = os.path.dirname(__file__)
                    messagebox.showinfo("Create Script", f"Script successfully created in '{current_path}'")
                else:
                    self.processing.copy_to_clipboard(commands)
                    copy_button.config(text="Copied!", state="disabled", width=22)
                    self.master.after(3000, lambda: copy_button.config(text="Copy Script to Clipboard", state="normal"))

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

    @staticmethod
    def create_tooltip(string, widget, **kwargs):
        x_offset = -300
        delay = kwargs.get('delay', 0.3)
        tab_length = 4
        tooltip = textwrap.dedent(string).expandtabs(tab_length).strip()
        ToolTip(widget, msg=tooltip, delay=delay, x_offset=x_offset)

