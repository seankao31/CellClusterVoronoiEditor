import numpy as np

from PIL import Image, ImageDraw

from src.color_list import ColorList
from src.voronoi_diagram import VoronoiDiagram
from src.plot_utils import voronoiFinitePolygons, voronoiSegments


class Model:
    def __init__(self):
        self.color_list = ColorList()
        self.image_refs = []

    @property
    def color_list(self):
        return self._color_list

    @color_list.setter
    def color_list(self, val):
        self._color_list = val

    @property
    def voronoi_diagram(self):
        return self._voronoi_diagram

    @voronoi_diagram.setter
    def voronoi_diagram(self, val):
        self._voronoi_diagram = val

    def setupTask(self, image_file_name):
        self.back_image = image = self.createImage(image_file_name)
        width, height = image.size
        self.voronoi_diagram = VoronoiDiagram(h=height, w=width)

    def createImage(self, file_name):
        return Image.open(file_name)

    def blendImageVoronoi(self):
        width, height = self.back_image.size
        draw_voronoi = Image.new(
                "RGB", (width, height), 'black')
        draw = ImageDraw.Draw(draw_voronoi)
        voronoi = self.voronoi_diagram.voronoi

        regions, vertices = voronoiFinitePolygons(voronoi)
        for region in regions:
            polygon = vertices[region]
            flattened = [i for sub in polygon for i in sub]
            color = tuple(np.random.choice(range(256), size=3))
            draw.polygon(flattened, fill=color, outline=None)

        finite_segments, infinite_segments = voronoiSegments(voronoi)
        line_width = 0
        for s in finite_segments:
            draw.line([s[0][0], s[0][1], s[1][0], s[1][1]],
                      fill='red', width=line_width)
        for s in infinite_segments:
            draw.line([s[0][0], s[0][1], s[1][0], s[1][1]],
                      fill='red', width=line_width)

        for p in voronoi.points:
            draw.arc([p[0]-5, p[1]-5, p[0]+5, p[1]+5], 0, 360, 'red')

        self.blend_image_voronoi = Image.blend(
                self.back_image.convert('RGB'), draw_voronoi, 0.5)
