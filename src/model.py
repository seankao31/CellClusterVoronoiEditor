import numpy as np

from PIL import Image

from src.color_list import ColorList
from src.draw import Draw
from src.voronoi_analysis import VoronoiAnalysis
from src.voronoi_diagram import VoronoiDiagram


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
        draw_voronoi = Image.new('RGB', (width, height), 'black')
        draw = Draw(draw_voronoi)
        voronoi = self.voronoi_diagram.voronoi
        voronoi_analysis = VoronoiAnalysis(voronoi)

        bbox = [(0, 0), (width, height)]
        regions, vertices, finite_segments, infinite_segments = \
            voronoi_analysis.finitePolygons(bbox)
        for p, region in enumerate(regions):
            polygon = vertices[region]
            flattened = [i for sub in polygon for i in sub]
            color = self.voronoi_diagram.region_color_map[p]
            if color == -1:
                color = tuple(np.random.choice(range(256), size=3))
            else:
                color = self.color_list[color]
            draw.polygon(flattened, fill=color, outline=None)

        finite_segments = [[(a, b) for a, b in s] for s in finite_segments]
        infinite_segments = [[(a, b) for a, b in s] for s in infinite_segments]

        line_width = 4
        for s in finite_segments:
            draw.line(s, fill='red', width=line_width)
        for s in infinite_segments:
            draw.line(s, fill='red', width=line_width)

        for p in voronoi.points:
            draw.circle(p, radius=2, fill='red')

        self.blend_image_voronoi = Image.blend(
                self.back_image.convert('RGB'), draw_voronoi, 0.5)
