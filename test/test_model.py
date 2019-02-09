from tkinter import Tk

from src.model import Model


class Test_createImage:
    def test_tiff(self):
        Tk()
        model = Model()
        model.createImage('image/test.tiff')

    def test_png(self):
        Tk()
        model = Model()
        model.createImage('image/test.png')

    def test_jpg(self):
        Tk()
        model = Model()
        model.createImage('image/test.jpg')


class Test_setupTask:
    def test_setupTask(self):
        Tk()
        model = Model()
        model.setupTask('image/test.tiff')
        assert(model.voronoi_diagram is not None)
