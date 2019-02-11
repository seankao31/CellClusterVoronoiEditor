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
        try:
            self.model.voronoi_diagram.addPoint(event.x, event.y)
            self.model.blendImageVoronoi()
            self.taskDisplayImage(self.model.blend_image_voronoi)
        except ValueError as e:
            print(e)
