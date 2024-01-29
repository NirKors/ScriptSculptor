import tkinter as tk


class ScriptSculptorApp:
    def __init__(self, master):
        self.master = master
        master.title("ScriptSculptor")
        master.configure(bg="black")

        window_width = 800
        window_height = 600
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        master.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        buttons_frame = tk.Frame(self.master, borderwidth=2, relief="solid", background="red")

        newFrameButton = tk.Button(buttons_frame, text="Add New Frame", command=self.createNewFrame)
        newFrameButton.pack(side=tk.LEFT, padx=5)

        deleteFrameButton = tk.Button(buttons_frame, text="Delete Frame", command=self.deleteFrame)
        deleteFrameButton.pack(side=tk.LEFT, padx=5)

        buttons_frame.pack(anchor="nw", pady=5, padx=5)

        # Use a class variable to keep track of the selected frame
        self.selected_frame = None

        scriptFrame = tk.Label(self.master, borderwidth=2, relief="solid", background="blue")
        scriptFrame.pack(expand=True, fill="both")

        self.createNewFrame()
        self.createNewFrame()

    def deleteFrame(self):
        return

    def createNewFrame(self):
        # Method to add a new frame dynamically
        newFrame = tk.Label(self.master, borderwidth=1, relief="solid", background="red")
        newFrame.pack(pady=5, padx=5, fill="x")

        newButton = tk.Button(newFrame, text="test button")
        newButton.pack()

        # Example: Add a label to the new frame
        label = tk.Label(newFrame, text="I want to", padx=10)
        label.pack(side=tk.LEFT)

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
            self.selected_frame.configure(bg="red")  # Reset the previously selected frame color

        self.selected_frame = frame
        frame.configure(bg="green")  # Highlight the selected frame


def main():
    root = tk.Tk()
    app = ScriptSculptorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
