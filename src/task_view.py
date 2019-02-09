import tkinter as tk
from PIL import ImageTk


class TaskView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('Task')
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side='left')

    def displayImage(self, image):
        self.image = image
        self.photo_image = photo_image = ImageTk.PhotoImage(image)
        width, height = image.size
        self.canvas.config(width=width, height=height)
        self.canvas.create_image((0, 0), image=photo_image, anchor="nw")

    def displayVoronoi(self, voronoi):
        pass
