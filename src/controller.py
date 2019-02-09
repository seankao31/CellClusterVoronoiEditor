from src.model import Model
from src.view import View
from src.task_view import TaskView


class Controller:
    def __init__(self, root):
        self.model = Model()
        self.main_view = View(root)
        self.task_view = TaskView(self.main_view)
        self.task_view.bind('<Button-1>', self.taskEventHandler)

    def taskLoadImage(self, image_file_name):
        self.model.setupTask(image_file_name)
        self.task_view.displayImage(self.model.image)

    # use callback function instead
    def addPoint(self, r, c):
        self.model.voronoi_diagram.addPoint(r, c)

    def taskDisplayVoronoi(self):
        self.task_view.displayVoronoi(
                self.model.voronoi_diagram.voronoi,
                self.model.voronoi_diagram.points)

    def taskEventHandler(self, event):
        try:
            self.model.voronoi_diagram.addPoint(event.x, event.y)
            self.taskDisplayVoronoi()
        except ValueError as e:
            print(e)
