from collections import OrderedDict

import numpy as np
from pubsub import pub


class ColorList:
    def __init__(self):
        self.colors = OrderedDict()
        self.id = 0

    def __getattr__(self, name):
        # avoid recursion
        return super().__getattribute__('colors').__getattribute__(name)

    def __getitem__(self, key):
        return self.colors[key]

    def __setitem__(self, key, val):
        self.colors[key] = val
        pub.sendMessage('updateColorList')

    def __delitem__(self, key):
        del self.colors[key]
        pub.sendMessage('updateColorList')

    def new(self):
        self.colors[self.id] = tuple(np.random.choice(range(256), size=3))
        self.id += 1
        pub.sendMessage('updateColorList.newColor')
