import numpy as np
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

from src.plot_utils import voronoiSegments, voronoiFinitePolygons


class TaskView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('Task')
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side='left')

    def displayImage(self, image):
        self.back_image = image
        self.photo_image = photo_image = ImageTk.PhotoImage(image)
        self.width, self.height = width, height = image.size
        self.canvas.config(width=width, height=height)
        self.canvas.create_image((0, 0), image=photo_image, anchor="nw")

    def displayVoronoi(self, voronoi):
        self.draw_voronoi = Image.new(
                "RGB", (self.width, self.height), 'white')
        self.draw = ImageDraw.Draw(self.draw_voronoi)

        regions, vertices = voronoiFinitePolygons(voronoi)
        for region in regions:
            polygon = vertices[region]
            flattened = [i for sub in polygon for i in sub]
            self.draw.polygon(
                    flattened, tuple(np.random.choice(range(256), size=3)))

        finite_segments, infinite_segments = voronoiSegments(voronoi)
        for s in finite_segments:
            self.draw.line([s[0][0], s[0][1], s[1][0], s[1][1]], 'red')
        for s in infinite_segments:
            self.draw.line([s[0][0], s[0][1], s[1][0], s[1][1]], 'red')

        blend = Image.blend(
                self.back_image.convert('RGB'), self.draw_voronoi, 0.5)
        self.photo_blend = ImageTk.PhotoImage(blend)

        self.canvas.create_image((0, 0), image=self.photo_blend, anchor="nw")
