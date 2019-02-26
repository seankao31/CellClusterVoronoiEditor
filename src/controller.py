import pickle

from pubsub import pub

from src.display_option_view import DisplayOptionView
from src.menubar import Menubar
from src.model import Model
from src.task_view import TaskView
from src.view import View


class Controller:
    def __init__(self, root):
        root.config(menu=Menubar(root).menubar)
        self.model = Model()
        self.main_view = View(root)
        self.display_option_view = DisplayOptionView(
            self.main_view, self.model.display_option)
        self.task_view = TaskView(self.main_view)
        self.task_loaded = False
        pub.subscribe(self.openFile, 'openFile')
        pub.subscribe(self.taskLoadImage, 'loadImageFile')
        pub.subscribe(self.taskExportImage, 'exportImage')
        pub.subscribe(self.taskSaveFile, 'saveFile')
        pub.subscribe(self.taskEventHandler, 'taskViewClick')
        pub.subscribe(self.model.color_list.new, 'newColor')
        pub.subscribe(self.updateTaskView, 'updateVoronoi')
        pub.subscribe(self.updateTaskView, 'updateDisplayOption')
        pub.subscribe(self.model.color_list.__setitem__, 'editColor')
        pub.subscribe(self.updateTaskView, 'updateColorList')
        pub.subscribe(self.updateMainView, 'updateColorList.newColor')
        pub.subscribe(self.chooseNewColor, 'updateColorList.newColor')

    def openFile(self, open_file_name):
        self.task_loaded, \
            self.model.color_list, \
            self.model.voronoi_diagram, \
            back_image_file_name, \
            self.model.display_option.point_radius, \
            self.model.display_option.point_color, \
            self.model.display_option.line_width, \
            self.model.display_option.line_color, \
            self.model.display_option.region_alpha = \
            pickle.load(open(open_file_name, 'rb'))
        pub.subscribe(self.model.color_list.new, 'newColor')
        pub.subscribe(self.model.color_list.__setitem__, 'editColor')
        self.model.loadImage(back_image_file_name)
        self.model.display_option.setVariables()
        self.updateTaskView()
        self.updateMainView()

    def taskLoadImage(self, image_file_name):
        self.task_loaded = True
        self.model.setupTask(image_file_name)
        self.taskDisplayImage(self.model.back_image)

    def taskExportImage(self, export_file_name):
        if not self.task_loaded:
            return
        self.model.blend_image_voronoi.save(export_file_name)

    def taskSaveFile(self, save_file_name):
        with open(save_file_name, 'wb') as f:
            pickle.dump([self.task_loaded,
                         self.model.color_list,
                         self.model.voronoi_diagram,
                         self.model.back_image_file_name,
                         self.model.display_option.point_radius,
                         self.model.display_option.point_color,
                         self.model.display_option.line_width,
                         self.model.display_option.line_color,
                         self.model.display_option.region_alpha], f)

    def taskDisplayImage(self, image):
        self.task_view.displayImage(image)

    def taskEventHandler(self, event):
        if not self.task_loaded:
            return
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
        if not self.task_loaded:
            return
        self.model.blendImageVoronoi()
        self.taskDisplayImage(self.model.blend_image_voronoi)

    def updateMainView(self):
        self.main_view.updateColorList(self.model.color_list)

    def chooseNewColor(self):
        self.main_view.color_list_view.color.set(
            list(self.model.color_list.keys())[-1])
