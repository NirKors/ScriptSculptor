import tkinter as tk
import os
from ui_engine import UIEngine


def main():
    root = tk.Tk()

    script_path = os.path.dirname(__file__)
    script_dir, _ = os.path.split(script_path)
    config_dir = os.path.join(script_dir, "config")

    image = tk.PhotoImage(file=f"{script_path}\\assets\\icon.png")
    root.iconphoto(False, image)

    UIEngine(root, config_dir)
    root.mainloop()


if __name__ == "__main__":
    main()
