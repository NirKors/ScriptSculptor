# main.py
import tkinter as tk

from ui_engine import UIEngine


def main():
    root = tk.Tk()
    # root.wm_attributes("-transparentcolor", 'grey')
    app = UIEngine(root)
    root.mainloop()


if __name__ == "__main__":
    main()
