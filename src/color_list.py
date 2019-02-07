from collections import OrderedDict
from colour import Color


class ColorList:
    def __init__(self):
        self.colors = OrderedDict()
        self.id = 0

    def __getitem__(self, key):
        return self.colors[key]

    def __setitem__(self, key, val):
        self.colors[key] = val

    def __delitem__(self, key):
        del self.colors[key]

    def new(self):
        self.colors[self.id] = Color()
        self.id += 1
