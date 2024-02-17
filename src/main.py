# main.py
import tkinter as tk

from ui_engine import UIEngine


def main():
    root = tk.Tk()
    # root.wm_attributes("-transparentcolor", 'grey')
    config_path = "C:\\Users\\nirko\\PycharmProjects\\ScriptSculptor\\config"
    app = UIEngine(root, config_path)
    root.mainloop()


if __name__ == "__main__":
    main()
