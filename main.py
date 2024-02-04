# main.py
import tkinter as tk

from myapp import MyApp


def main():
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
