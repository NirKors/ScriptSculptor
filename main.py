# main.py
import tkinter as tk

from ui_engine import UIEngine


def main():
    root = tk.Tk()
    app = UIEngine(root)
    root.mainloop()


if __name__ == "__main__":
    main()
