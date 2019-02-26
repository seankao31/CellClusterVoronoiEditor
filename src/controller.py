from functools import partial
import pickle

from pubsub import pub

from src.display_option_view import DisplayOptionView
from src.menubar import Menubar
from src.model import Model
from src.task_view import TaskView
from src.undo_redo import Action, UndoRedo
from src.view import View


class Controller:
    def __init__(self, root):
        root.config(menu=Menubar(root).menubar)
        self.model = Model()
        self.undo_redo = UndoRedo()
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
        pub.subscribe(self.undo_redo.undo, 'undo')
        pub.subscribe(self.undo_redo.redo, 'redo')
        pub.subscribe(self.main_view.switchAction, 'switchAction')

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
        try:
            self.model.voronoi_diagram.checkPointValid((event.x, event.y))
        except ValueError:
            return
        if self.main_view.action.get() == 0:
            self.addPoint(event)
        elif self.main_view.action.get() == 1:
            self.deletePoint(event)
        elif self.main_view.action.get() == 2:
            self.changeColor(event)

    def addPoint(self, event):
        try:
            color = self.main_view.color_list_view.color.get()
            self.model.voronoi_diagram.addPoint(event.x, event.y, color)
        except ValueError as e:
            print(e)
            return
        action = Action(undo=partial(self.executeDeletePoint, event=event),
                        redo=partial(self.model.voronoi_diagram.addPoint,
                                     r=event.x,
                                     c=event.y,
                                     color=color))
        self.undo_redo.newAction(action)

    def executeDeletePoint(self, event):
        nearest = self.model.voronoi_diagram.findNearestPoint(
            (event.x, event.y))
        self.model.voronoi_diagram.deletePoint(nearest)

    def deletePoint(self, event):
        nearest = self.model.voronoi_diagram.findNearestPoint(
            (event.x, event.y))
        color = self.model.voronoi_diagram.region_color_map[nearest]
        point = self.model.voronoi_diagram.points[nearest]
        # event.x = point[0]
        # event.y = point[1]
        action = Action(undo=partial(self.model.voronoi_diagram.addPoint,
                                     r=point[0],
                                     c=point[1],
                                     color=color),
                        redo=partial(self.executeDeletePoint,
                                     event=event))
        self.undo_redo.newAction(action)
        self.model.voronoi_diagram.deletePoint(nearest)

    def executeChangeColor(self, event, color):
        nearest = self.model.voronoi_diagram.findNearestPoint(
            (event.x, event.y))
        self.model.voronoi_diagram.editRegionColor(nearest, color)

    def changeColor(self, event):
        nearest = self.model.voronoi_diagram.findNearestPoint(
            (event.x, event.y))
        color = self.main_view.color_list_view.color.get()
        old_color = self.model.voronoi_diagram.region_color_map[nearest]
        # point = self.model.voronoi_diagram.points[nearest]
        # event.x = point[0]
        # event.y = point[1]
        action = Action(undo=partial(self.executeChangeColor,
                                     event=event,
                                     color=old_color),
                        redo=partial(self.executeChangeColor,
                                     event=event,
                                     color=color))
        self.undo_redo.newAction(action)
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
