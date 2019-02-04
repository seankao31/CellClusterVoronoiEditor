import pytest

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

    def test_addPoint_no_duplicate(self):
        voronoi_diagram = VoronoiDiagram(h=10, w=20)
        assert(not voronoi_diagram.points)
        voronoi_diagram.addPoint(3, 3)
        voronoi_diagram.addPoint(3, 3)
        assert(len(voronoi_diagram.points) == 1)
