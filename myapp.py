# myapp.py
import tkinter as tk
from configparser import ConfigParser

from processing import Processing


class MyApp:
    def __init__(self, master):
        self.master = master
        master.title("ScriptSculptor")
        master.configure(bg="black")
        config = ConfigParser()
        config.read('settings.ini')

        self.colors = config["colors"]
        self.relief_generator = Processing()

        window_width = 800
        window_height = 600
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        master.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        buttons_frame = tk.Frame(self.master, borderwidth=2, relief="solid", background=self.colors["buttons_frame"])

        newFrameButton = tk.Button(buttons_frame, text="Add New Frame", command=self.createNewFrame)
        newFrameButton.pack(side=tk.LEFT, padx=5)

        deleteFrameButton = tk.Button(buttons_frame, text="Delete Frame", command=self.deleteFrame)
        deleteFrameButton.pack(side=tk.LEFT, padx=5)

        reliefFrameButton = tk.Button(buttons_frame, text="Change Style", command=self.changeStyle)
        reliefFrameButton.pack(side=tk.LEFT, padx=5)

        buttons_frame.pack(anchor="nw", pady=5, padx=5)

        # Use a class variable to keep track of the selected frame
        self.selected_frame = None

        scriptFrame = tk.Label(self.master, borderwidth=2, relief="solid", background=self.colors["script_frame"])
        scriptFrame.pack(expand=True, fill="both")

        self.createNewFrame()
        self.createNewFrame()

    def deleteFrame(self):

        if self.selected_frame:
            self.selected_frame.destroy()
            self.selected_frame = None
        return

    def changeStyle(self):
        relief = self.relief_generator.get_relief()

        for child in self.master.winfo_children():
            # Check if the child is a frame
            if isinstance(child, tk.Frame):
                child.configure(relief=relief)
        return

    def createNewFrame(self):
        # Method to add a new frame dynamically
        newFrame = tk.Frame(self.master, borderwidth=1, relief="solid", background=self.colors["script_frame"])
        newFrame.pack(pady=5, padx=5, fill="x")

        # Example: Add a label to the new frame
        label = tk.Label(newFrame, text="Placeholder label", padx=10)
        label.pack(side=tk.LEFT)

        # Dropdown Menu
        options = ["Option 1", "Option 2", "Option 3"]
        selected_option = tk.StringVar(newFrame)
        selected_option.set(options[0])  # Set default option
        dropdown = tk.OptionMenu(newFrame, selected_option, *options)
        dropdown.pack(side=tk.LEFT)

        newButton = tk.Button(newFrame, text="Placeholder button")
        newButton.pack(side=tk.RIGHT)

        # Bind click event to the frame
        newFrame.bind("<Button-1>", lambda event, frame=newFrame: self.selectFrame(frame))

        # Bind click event to its children
        self.bind_children_click(newFrame)

    def bind_children_click(self, widget):
        # Method to bind the click event to all children of a widget
        for child in widget.winfo_children():
            child.bind("<Button-1>", lambda event, frame=widget: self.selectFrame(frame))
            self.bind_children_click(child)

    def selectFrame(self, frame):
        # Method to select a frame and highlight it with a different colored border
        if self.selected_frame:
            self.selected_frame.configure(bg=self.colors["script_frame"])  # Reset the previously selected frame color

        self.selected_frame = frame
        frame.configure(bg=self.colors["selected_frame_highlight"])  # Highlight the selected frame
