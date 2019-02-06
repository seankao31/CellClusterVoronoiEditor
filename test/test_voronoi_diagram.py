import pytest
from scipy.spatial.qhull import QhullError

from src.voronoi_diagram import VoronoiDiagram


class Test_checkPointValid:
    def test_checkPointValid_valid_0(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        voronoi_diagram.checkPointValid((5, 10))

    def test_checkPointValid_valid_1(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        voronoi_diagram.checkPointValid((0, 10))

    def test_checkPointValid_valid_2(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        voronoi_diagram.checkPointValid((9, 10))

    def test_checkPointValid_valid_3(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        voronoi_diagram.checkPointValid((5, 0))

    def test_checkPointValid_valid_4(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        voronoi_diagram.checkPointValid((5, 19))

    def test_checkPointValid_invalid_0(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        with pytest.raises(ValueError):
            voronoi_diagram.checkPointValid((-1, 10))

    def test_checkPointValid_invalid_1(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        with pytest.raises(ValueError):
            voronoi_diagram.checkPointValid((10, 10))

    def test_checkPointValid_invalid_2(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        with pytest.raises(ValueError):
            voronoi_diagram.checkPointValid((5, -1))

    def test_checkPointValid_invalid_3(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        with pytest.raises(ValueError):
            voronoi_diagram.checkPointValid((5, 20))

    def test_checkPointValid_invalid_4(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        with pytest.raises(ValueError):
            voronoi_diagram.checkPointValid(())

    def test_checkPointValid_invalid_5(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        with pytest.raises(ValueError):
            voronoi_diagram.checkPointValid((4,))

    def test_checkPointValid_invalid_6(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        with pytest.raises(ValueError):
            voronoi_diagram.checkPointValid((4, 4, 4))


class Test_addPoint:
    def test_addPoint_invalid(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        with pytest.raises(ValueError):
            voronoi_diagram.addPoint(-1, -1)

    def test_addPoint_single(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        assert(not voronoi_diagram.points)
        voronoi_diagram.addPoint(3, 3)
        assert(len(voronoi_diagram.points) == 1)

    def test_addPoint_multiple(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        assert(not voronoi_diagram.points)
        voronoi_diagram.addPoint(3, 3)
        voronoi_diagram.addPoint(4, 4)
        voronoi_diagram.addPoint(2, 9)
        assert(len(voronoi_diagram.points) == 3)

    def test_addPoint_duplicate(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        assert(not voronoi_diagram.points)
        voronoi_diagram.addPoint(3, 3)
        voronoi_diagram.addPoint(3, 3)
        assert(len(voronoi_diagram.points) == 1)


class Test_addPoints:
    def test_addPoints_multiple(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        assert(not voronoi_diagram.points)
        points = [(1, 2), (2, 2), (4, 5), (15, 2), (3, 2), (2, 2), (1, 2)]
        voronoi_diagram.addPoints(points)
        assert(len(voronoi_diagram.points) == 5)


class Test_generateVoronoi:
    def test_generateVoronoi_invalid_one_point(self):
        voronoi_diagram = VoronoiDiagram(h=30, w=30)
        voronoi_diagram.addPoint(4, 15)
        with pytest.raises(QhullError):
            voronoi_diagram.generateVoronoi()

    def test_generateVoronoi_invalid_two_points(self):
        voronoi_diagram = VoronoiDiagram(h=30, w=30)
        voronoi_diagram.addPoint(4, 15)
        voronoi_diagram.addPoint(7, 6)
        with pytest.raises(QhullError):
            voronoi_diagram.generateVoronoi()

    def test_generateVoronoi_valid_three_points(self):
        voronoi_diagram = VoronoiDiagram(h=30, w=30)
        voronoi_diagram.addPoint(4, 15)
        voronoi_diagram.addPoint(7, 6)
        voronoi_diagram.addPoint(8, 8)
        voronoi_diagram.generateVoronoi()
        assert(voronoi_diagram.voronoi is not None)

    def test_generateVoronoi_valid_four_points(self):
        voronoi_diagram = VoronoiDiagram(h=30, w=30)
        voronoi_diagram.addPoint(4, 15)
        voronoi_diagram.addPoint(7, 6)
        voronoi_diagram.addPoint(8, 8)
        voronoi_diagram.addPoint(23, 19)
        voronoi_diagram.generateVoronoi()
        assert(voronoi_diagram.voronoi is not None)

    def test_generateVoronoi_invalid_coplanar(self):
        voronoi_diagram = VoronoiDiagram(h=30, w=30)
        points = [(1+2*r, 2+3*r) for r in range(8)]
        voronoi_diagram.addPoints(points)
        assert(len(voronoi_diagram.points) == 8)
        with pytest.raises(QhullError):
            voronoi_diagram.generateVoronoi()
