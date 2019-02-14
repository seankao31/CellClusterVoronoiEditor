from collections import OrderedDict


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
        self.colors[self.id] = (0, 0, 0)
        self.id += 1
