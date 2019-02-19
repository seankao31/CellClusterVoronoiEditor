from pubsub import pub

from src.model import Model
from src.task_view import TaskView
from src.view import View


class Controller:
    def __init__(self, root):
        self.model = Model()
        self.main_view = View(root)
        self.task_view = TaskView(self.main_view)
        pub.subscribe(self.taskEventHandler, 'taskViewClick')
        pub.subscribe(self.model.color_list.new, 'newColor')
        pub.subscribe(self.updateTaskView, 'updateVoronoi')
        pub.subscribe(self.model.color_list.__setitem__, 'editColor')
        pub.subscribe(self.updateTaskView, 'updateColorList')
        pub.subscribe(self.updateMainView, 'updateColorList.newColor')
        pub.subscribe(self.chooseNewColor, 'updateColorList.newColor')

    def taskLoadImage(self, image_file_name):
        self.model.setupTask(image_file_name)
        self.taskDisplayImage(self.model.back_image)

    def taskDisplayImage(self, image):
        self.task_view.displayImage(image)

    def taskEventHandler(self, event):
        if self.main_view.action.get() == 0:
            try:
                color = self.main_view.color_list_view.color.get()
                self.model.voronoi_diagram.addPoint(event.x, event.y, color)
            except ValueError as e:
                print(e)
        elif self.main_view.action.get() == 1:
            nearest = self.model.voronoi_diagram.findNearestPoint(
                (event.x, event.y))
            self.model.voronoi_diagram.deletePoint(nearest)
        elif self.main_view.action.get() == 2:
            nearest = self.model.voronoi_diagram.findNearestPoint(
                (event.x, event.y))
            color = self.main_view.color_list_view.color.get()
            self.model.voronoi_diagram.editRegionColor(nearest, color)

    def updateTaskView(self):
        self.model.blendImageVoronoi()
        self.taskDisplayImage(self.model.blend_image_voronoi)

    def updateMainView(self):
        self.main_view.updateColorList(self.model.color_list)

    def chooseNewColor(self):
        self.main_view.color_list_view.color.set(
            list(self.model.color_list.keys())[-1])
