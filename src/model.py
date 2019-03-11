import numpy as np

from PIL import Image, ImageFont

from color_list import ColorList
from display_option import DisplayOption
from draw import Draw
from voronoi_analysis import VoronoiAnalysis
from voronoi_diagram import VoronoiDiagram


class Model:
    def __init__(self):
        self.color_list = ColorList()
        self.display_option = DisplayOption()
        self.voronoi_diagram = None
        self.back_image_file_name = None

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

    def loadImage(self, image_file_name):
        self.back_image_file_name = image_file_name
        self.back_image = self.createImage(image_file_name)

    def setupTask(self, image_file_name):
        self.back_image_file_name = image_file_name
        self.back_image = image = self.createImage(image_file_name)
        width, height = image.size
        self.voronoi_diagram = VoronoiDiagram(h=height, w=width)

    def createImage(self, file_name):
        return Image.open(file_name)

    def blendImageVoronoi(self):
        width, height = self.back_image.size
        draw_voronoi = Image.new('RGB', (width, height), 'black')
        draw = Draw(draw_voronoi)

        point_radius = self.display_option.point_radius
        point_color = self.display_option.point_color
        line_width = self.display_option.line_width
        line_color = self.display_option.line_color
        region_alpha = self.display_option.region_alpha
        areas = []
        finite_segments = []
        infinite_segments = []
        self.blend_image_voronoi = self.back_image.convert('RGB')

        try:
            voronoi = self.voronoi_diagram.voronoi
            voronoi_analysis = VoronoiAnalysis(voronoi)

            bbox = [(0, 0), (width, height)]
            regions, vertices, areas, finite_segments, infinite_segments = \
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

            finite_segments = [[(a, b) for a, b in s]
                               for s in finite_segments]
            infinite_segments = [[(a, b) for a, b in s]
                                 for s in infinite_segments]

            self.blend_image_voronoi = Image.blend(
                self.back_image.convert('RGB'),
                draw_voronoi,
                region_alpha)

        except (AttributeError, ValueError):
            print('This error raises possibly due to too few points.')

        scale = self.display_option.scale  # for anti-aliasing

        self.blend_image_voronoi = \
            self.blend_image_voronoi.resize((width*scale, height*scale))

        draw = Draw(self.blend_image_voronoi)

        for s in finite_segments:
            ss = [tuple(e * scale for e in p) for p in s]
            draw.line(ss, fill=line_color, width=line_width*scale)
        for s in infinite_segments:
            ss = [tuple(e * scale for e in p) for p in s]
            draw.line(ss, fill=line_color, width=line_width*scale)

        self.blend_image_voronoi = \
            self.blend_image_voronoi.resize((width, height),
                                            resample=Image.LANCZOS)

        draw = Draw(self.blend_image_voronoi)

        # font = ImageFont.truetype('Arial.ttf', point_radius + 10)

        for i, p in enumerate(self.voronoi_diagram.points):
            if self.display_option.point_display == 0:
                draw.circle(p, radius=point_radius, fill=point_color)
            elif self.display_option.point_display == 1:
                area = -1
                if areas:
                    area = round(areas[i], 2)
                # draw.text(p, str(area), font=font, fill=point_color)
                draw.text(p, str(area), fill=point_color)
            else:
                color = self.voronoi_diagram.region_color_map[i]
                # draw.text(p, str(color), font=font, fill=point_color)
                draw.text(p, str(color), fill=point_color)
