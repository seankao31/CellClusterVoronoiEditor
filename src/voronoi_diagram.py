from pubsub import pub
from scipy.spatial import Voronoi, cKDTree
from scipy.spatial.qhull import QhullError


class VoronoiDiagram:
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.points = []
        self.region_color_map = []
        self.is_prepared = False

    @property
    def voronoi(self):
        if not self.is_prepared:
            self.prepare()
        return self._voronoi

    @voronoi.setter
    def voronoi(self, value):
        self._voronoi = value

    def prepare(self):
        if self.is_prepared:
            return
        self.is_prepared = True
        self.finalPoints()
        self.generateVoronoi()

    def addPoint(self, r, c, color=-1):
        point = (r, c)
        self.checkPointValid(point)
        if point in self.points:
            raise ValueError('Cannot add duplicate point.')
        self.points.append(point)
        self.region_color_map.append(color)
        self.is_prepared = False
        pub.sendMessage('updateVoronoi')

    def addPoints(self, points):
        for r, c in points:
            self.addPoint(r, c)

    def deletePoint(self, index):
        # Explicitly disallow -1 ~ -len
        if index < 0:
            raise IndexError()
        del self.points[index]
        del self.region_color_map[index]
        self.is_prepared = False
        pub.sendMessage('updateVoronoi')

    def editPoint(self, index, new_point):
        # Explicitly disallow -1 ~ -len
        if index < 0:
            raise IndexError()
        self.checkPointValid(new_point)
        self.points[index] = new_point
        self.is_prepared = False
        pub.sendMessage('updateVoronoi')

    def editRegionColor(self, index, new_color):
        # Explicitly disallow -1 ~ -len
        if index < 0:
            raise IndexError()
        self.region_color_map[index] = new_color
        pub.sendMessage('updateVoronoi')

    def checkPointValid(self, point):
        if len(point) != 2:
            raise ValueError('Point length should be 2.')
        r = point[0]
        c = point[1]
        if r < 0 or r >= self.h or c < 0 or c >= self.w:
            raise ValueError('Point out of range.')

    def finalPoints(self):
        self.points_kdtree = cKDTree(self.points)

    def generateVoronoi(self):
        try:
            self.voronoi = Voronoi(self.points)
        except QhullError as e:
            self.voronoi = None
            print(e.__class__.__name__)

    def findNearestPoint(self, query_point):
        dist, index = self.points_kdtree.query(query_point)
        return index
