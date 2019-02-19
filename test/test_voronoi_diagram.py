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
        assert(len(voronoi_diagram.region_color_map) == 1)

    def test_addPoint_multiple(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        assert(not voronoi_diagram.points)
        voronoi_diagram.addPoint(3, 3)
        voronoi_diagram.addPoint(4, 4)
        voronoi_diagram.addPoint(2, 9)
        assert(len(voronoi_diagram.points) == 3)
        assert(len(voronoi_diagram.region_color_map) == 3)

    def test_addPoint_duplicate(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        assert(not voronoi_diagram.points)
        voronoi_diagram.addPoint(3, 3)
        with pytest.raises(ValueError):
            voronoi_diagram.addPoint(3, 3)
        assert(len(voronoi_diagram.points) == 1)
        assert(len(voronoi_diagram.region_color_map) == 1)


class Test_addPoints:
    def test_addPoints_multiple(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        assert(not voronoi_diagram.points)
        points = [(1, 2), (2, 2), (4, 5), (7, 2), (3, 2)]
        voronoi_diagram.addPoints(points)
        assert(len(voronoi_diagram.points) == 5)
        assert(len(voronoi_diagram.region_color_map) == 5)

    def test_addPoints_duplicate(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        assert(not voronoi_diagram.points)
        points = [(1, 2), (2, 2), (4, 5), (7, 2), (3, 2), (2, 2), (1, 2)]
        with pytest.raises(ValueError):
            voronoi_diagram.addPoints(points)
        # assert(not voronoi_diagram.points)
        assert(len(voronoi_diagram.points) == 5)
        assert(len(voronoi_diagram.region_color_map) == 5)

    def test_addPoints_duplicate_early(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        assert(not voronoi_diagram.points)
        points = [(1, 2), (2, 2), (2, 2), (4, 5), (7, 2), (3, 2)]
        with pytest.raises(ValueError):
            voronoi_diagram.addPoints(points)
        assert(len(voronoi_diagram.points) == 2)
        assert(len(voronoi_diagram.region_color_map) == 2)


class Test_deletePoint:
    def test_deletePoint(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        points = [(1, 2), (2, 2), (3, 5)]
        voronoi_diagram.addPoints(points)
        assert((1, 2) in voronoi_diagram.points)
        assert(len(voronoi_diagram.region_color_map) == 3)
        voronoi_diagram.deletePoint(0)
        assert((1, 2) not in voronoi_diagram.points)
        assert(len(voronoi_diagram.region_color_map) == 2)
        with pytest.raises(IndexError):
            voronoi_diagram.deletePoint(-1)
        with pytest.raises(IndexError):
            voronoi_diagram.deletePoint(-5)
        with pytest.raises(IndexError):
            voronoi_diagram.deletePoint(2)
        assert(len(voronoi_diagram.points) == 2)
        assert(len(voronoi_diagram.region_color_map) == 2)


class Test_editPoint:
    def test_editPoint(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        points = [(1, 2), (2, 2), (3, 5)]
        voronoi_diagram.addPoints(points)
        assert((1, 2) in voronoi_diagram.points)
        assert((2, 5) not in voronoi_diagram.points)
        voronoi_diagram.editPoint(index=0, new_point=(2, 5))
        assert((1, 2) not in voronoi_diagram.points)
        assert((2, 5) in voronoi_diagram.points)
        with pytest.raises(IndexError):
            voronoi_diagram.editPoint(index=5, new_point=(3, 3))


class Test_editRegionColor:
    def test_editRegionColor(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        points = [(1, 2), (2, 2), (3, 5)]
        voronoi_diagram.addPoints(points)
        assert(all(color == -1 for color in voronoi_diagram.region_color_map))
        voronoi_diagram.editRegionColor(index=1, new_color=1)
        assert(voronoi_diagram.region_color_map[0] == -1)
        assert(voronoi_diagram.region_color_map[1] == 1)
        assert(voronoi_diagram.region_color_map[2] == -1)
        with pytest.raises(IndexError):
            voronoi_diagram.editRegionColor(index=5, new_color=2)


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


class Test_findNeareastPoint:
    def test_findNearestPoint(self):
        voronoi_diagram = VoronoiDiagram(h=30, w=30)
        points = [(1, 1), (2, 5), (7, 2), (15, 29)]
        voronoi_diagram.addPoints(points)
        voronoi_diagram.prepare()
        assert(voronoi_diagram.findNearestPoint((1, 1)) == 0)
        assert(voronoi_diagram.findNearestPoint((1, 2)) == 0)
        assert(voronoi_diagram.findNearestPoint((5, 3)) == 2)
        assert(voronoi_diagram.findNearestPoint((20, 20)) == 3)
