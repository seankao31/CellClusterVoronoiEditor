from PIL import Image

from src.color_list import ColorList
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
        self.image = image = self.createImage(image_file_name)
        width, height = image.size
        self.voronoi_diagram = VoronoiDiagram(h=height, w=width)

    def createImage(self, file_name):
        return Image.open(file_name)
