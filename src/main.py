import tkinter as tk
from configparser import ConfigParser
from tkinter import ttk

from ui_engine import UIEngine


def main():
    config_path = "C:\\Users\\nirko\\PycharmProjects\\ScriptSculptor\\config"
    config_path = "C:\\Users\\Nir\\PycharmProjects\\ScriptSculptor\\config"

    root = tk.Tk()
    config = ConfigParser()
    config.read(f'{config_path}\\settings.ini')
    colors = config["colors"]
    style = ttk.Style()
    style.theme_use("default")

    style.configure("buttons_frame.TFrame", padding=6, background=colors["buttons_frame"])
    style.configure("background.TFrame", padding=6, background=colors["background"])
    style.configure("script_frame.TFrame", padding=6, background=colors["script_frame"])
    style.configure("selected_frame_highlight.TFrame", padding=6, background=colors["selected_frame_highlight"])
    style.configure("TLabel", background=colors["labels"])

    style.map("TButton",
              background=[("active", "white"), ("!active", "black")],
              foreground=[("active", "black"), ("!active", "white")])

    app = UIEngine(root, config_path)
    root.mainloop()


if __name__ == "__main__":
    main()
