from tkinter import ttk
from configparser import ConfigParser
import sv_ttk


class Style:
    def __init__(self, config_path):
        config = ConfigParser()
        config.read(f'{config_path}\\settings.ini')
        self.colors = config["colors"]
        self.style = ttk.Style()
        sv_ttk.set_theme("dark")

        self.style.configure("TFrame")
        self.style.configure("Highlight.TFrame", background="blue")  # TODO: Change color

    def toggle_highlight(self, widget, highlight: bool):  # TODO: Make recursive


        if isinstance(widget, ttk.Frame):
            highlight = "Highlight.TFrame" if highlight else ""
            widget.configure(style=highlight)
        else:
            print("else")
            widget.configure(style="")
