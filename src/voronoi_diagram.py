from scipy.spatial import Voronoi


class VoronoiDiagram:
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.points = []
        self.is_prepared = False

    def addPoint(self, r, c):
        point = (r, c)
        self.checkPointValid(point)
        if point not in self.points:
            self.points.append(point)
            self.is_prepared = False

    def addPoints(self, points):
        for point in points:
            if point not in self.points:
                self.points.append(point)
                self.is_prepared = False

    def checkPointValid(self, point):
        if len(point) != 2:
            raise ValueError('Point length should be 2.')
        r = point[0]
        c = point[1]
        if r < 0 or r >= self.h or c < 0 or c >= self.w:
            raise ValueError('Point out of range.')

    def generateVoronoi(self):
        points = np.array([list(point) for point in self.points])
        self.voronoi = Voronoi(points)
