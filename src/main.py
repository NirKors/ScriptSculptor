import tkinter as tk
from configparser import ConfigParser
from tkinter import ttk

from ui_engine import UIEngine


def main():

    root = tk.Tk()

    config_path = "C:\\Users\\nirko\\PycharmProjects\\ScriptSculptor\\config"
    config_path = "C:\\Users\\Nir\\PycharmProjects\\ScriptSculptor\\config"

    app = UIEngine(root, config_path)

    root.mainloop()




if __name__ == "__main__":
    main()
