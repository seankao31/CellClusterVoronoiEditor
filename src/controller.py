from src.model import Model
from src.task_view import TaskView
from src.view import View


class Controller:
    def __init__(self, root):
        self.model = Model()
        self.main_view = View(root)
        self.task_view = TaskView(self.main_view)
        self.task_view.bind('<Button-1>', self.taskEventHandler)

    def taskLoadImage(self, image_file_name):
        self.model.setupTask(image_file_name)
        self.taskDisplayImage(self.model.back_image)

    # use callback function instead
    def addPoint(self, r, c):
        self.model.voronoi_diagram.addPoint(r, c)

    def taskDisplayImage(self, image):
        self.task_view.displayImage(image)

    def taskEventHandler(self, event):
        if self.main_view.action.get() == 0:
            try:
                self.model.voronoi_diagram.addPoint(event.x, event.y)
                self.model.blendImageVoronoi()
                self.taskDisplayImage(self.model.blend_image_voronoi)
            except ValueError as e:
                print(e)
        elif self.main_view.action.get() == 1:
            nearest = self.model.voronoi_diagram.findNearestPoint(
                (event.x, event.y))
            self.model.voronoi_diagram.deletePoint(nearest)
            self.model.blendImageVoronoi()
            self.taskDisplayImage(self.model.blend_image_voronoi)
        elif self.main_view.action.get() == 2:
            nearest = self.model.voronoi_diagram.findNearestPoint(
                (event.x, event.y))
            color = self.main_view.color_list_view.color.get()
            self.model.voronoi_diagram.editRegionColor(nearest, color)
            self.model.blendImageVoronoi()
            self.taskDisplayImage(self.model.blend_image_voronoi)
