import tkinter as tk


class ScriptSculptorApp:
    def __init__(self, master):
        self.master = master
        master.title("ScriptSculptor")

        window_width = 800
        window_height = 600
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        master.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Create a canvas for scrolling
        self.canvas = tk.Canvas(master, borderwidth=0, background="black")
        self.frame = tk.Frame(self.canvas, background="white")
        self.scrollbar = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", self.on_frame_configure)

        # Creating the frames and buttons:
        self.buttonsFrame = tk.Frame(self.frame, borderwidth=2, relief="solid")

        newFrameButton = tk.Button(self.buttonsFrame, text="Add New Frame", command=self.createNewFrame)
        newFrameButton.pack(side=tk.LEFT, padx=5)

        deleteFrameButton = tk.Button(self.buttonsFrame, text="Delete Frame", command=self.deleteFrame)
        deleteFrameButton.pack(side=tk.LEFT, padx=5)

        self.buttonsFrame.pack(anchor="nw", pady=5, padx=5)

        self.actionsFrame = tk.Frame(self.frame, borderwidth=2, relief="solid")
        _ = tk.Button(self.actionsFrame, text="test1", command=self.createNewFrame)
        _.pack()
        _ = tk.Button(self.actionsFrame, text="test2", command=self.createNewFrame)
        _.pack()
        self.actionsFrame.pack(fill="both", expand=True, padx=5, pady=5)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def deleteFrame(self):
        return

    def createButton(self, text, command):
        # Method to create a button dynamically
        button = tk.Button(self.frame, text=text, command=command)
        button.pack()

    def createNewFrame(self):
        # Method to add a new frame dynamically
        new_frame = tk.Frame(self.frame, borderwidth=2, relief="solid")
        new_frame.pack(pady=10, fill="y")

        # Example: Add a label to the new frame
        label = tk.Label(new_frame, text="This is a new frame!")
        label.pack()

        # Configure the canvas to update its scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


def main():
    root = tk.Tk()
    app = ScriptSculptorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
