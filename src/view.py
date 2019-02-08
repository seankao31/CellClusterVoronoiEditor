import tkinter as tk


class View(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.title('Color Voronoi')
