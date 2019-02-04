class VoronoiDiagram:
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.points = set()

    def addPoint(self, r, c):
        point = (r, c)
        self.checkPointValid(point)
        self.points.add(point)

    def checkPointValid(self, point):
        if len(point) != 2:
            raise ValueError('Point length should be 2.')
        r = point[0]
        c = point[1]
        if r < 0 or r >= self.h or c < 0 or c >= self.w:
            raise ValueError('Point out of range.')
