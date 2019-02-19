import tkinter as tk

from src.app import App


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = App(root)
    root.mainloop()
