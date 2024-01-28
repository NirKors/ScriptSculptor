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

        scriptFrame = tk.Frame(self.master, borderwidth=2, relief="solid", background="blue")
        scriptFrame.pack(expand=True, fill="both")

    def deleteFrame(self):
        return

    def createNewFrame(self):
        # Method to add a new frame dynamically
        new_frame = tk.Frame(self.master, borderwidth=1, relief="solid", background="red")
        new_frame.pack(pady=5, padx=5, fill="x")

        # Example: Add a label to the new frame
        label = tk.Label(new_frame, text="I want to", padx=10)
        label.pack(side=tk.LEFT)


def main():
    root = tk.Tk()
    app = ScriptSculptorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
