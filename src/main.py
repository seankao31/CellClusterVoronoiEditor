import sys
import tkinter as tk

from app import App


if __name__ == '__main__':
    sys.tracebacklimit = 0
    root = tk.Tk()
    root.withdraw()
    app = App(root)
    root.mainloop()
