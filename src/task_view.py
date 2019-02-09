import tkinter as tk


class TaskView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('Task')
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side='left')

    def displayImage(self, image):
        self.image = image
        self.canvas.config(width=image.width(), height=image.height())
        self.canvas.create_image((0, 0), image=image, anchor="nw")

    def displayVoronoi(self, voronoi):
        pass
