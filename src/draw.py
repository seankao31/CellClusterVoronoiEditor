from PIL import ImageDraw


class Draw:
    def __init__(self, image):
        self.draw = ImageDraw.Draw(image)

    def __getattr__(self, name):
        return self.draw.__getattribute__(name)

    def circle(self, center, radius=2, **kwargs):
        if len(center) != 2:
            raise ValueError('Point length should be 2.')
        x, y = center
        bbox = [(x-radius, y-radius), (x+radius, y+radius)]
        self.draw.ellipse(bbox, **kwargs)
