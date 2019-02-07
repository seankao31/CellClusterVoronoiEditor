from tkinter import Tk

from src.model import Model


class Test_createImage:
    def test_tiff(self):
        Tk()
        model = Model()
        model.createImage('image/test.tiff')
        assert(len(model.image_refs) == 1)

    def test_png(self):
        Tk()
        model = Model()
        model.createImage('image/test.png')
        assert(len(model.image_refs) == 1)

    def test_jpg(self):
        Tk()
        model = Model()
        model.createImage('image/test.jpg')
        assert(len(model.image_refs) == 1)


class Test_setupTask:
    def test_setupTask(self):
        Tk()
        model = Model()
        model.setupTask('image/test.tiff')
        assert(model.voronoi_diagram is not None)
