from functools import partial
import json
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
        pub.subscribe(self.taskExportPoints, 'exportPoints')
        pub.subscribe(self.taskSaveFile, 'saveFile')
        pub.subscribe(self.model.color_list.new, 'newColor')
        pub.subscribe(self.updateTaskView, 'updateVoronoi')
        pub.subscribe(self.updateTaskView, 'updateDisplayOption')
        pub.subscribe(self.model.color_list.__setitem__, 'editColor')
        pub.subscribe(self.updateTaskView, 'updateColorList')
        pub.subscribe(self.updateMainView, 'updateColorList.newColor')
        pub.subscribe(self.chooseNewColor, 'updateColorList.newColor')
        # self.task_view.bind('<Button-1>', self.taskEventHandler)
        self.task_view.bind("<ButtonPress-1>", self.taskEventHandler)
        self.task_view.bind("<B1-Motion>", self.dragOnDrag)
        self.task_view.bind('<Command-z>', lambda *_:
                            self.undo_redo.undo())
        self.task_view.bind('<Command-Z>', lambda *_:
                            self.undo_redo.redo())
        self.task_view.bind('<Command-a>', lambda *_:
                            self.main_view.switchAction(0))
        self.task_view.bind('<Command-d>', lambda *_:
                            self.main_view.switchAction(1))
        self.task_view.bind('<Command-e>', lambda *_:
                            self.main_view.switchAction(2))
        self.task_view.bind('<Command-c>', lambda *_:
                            self.main_view.switchAction(3))
        self.task_view.bind('<Command-n>', lambda *_:
                            self.model.color_list.new())

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

    def taskExportPoints(self, export_file_name):
        if not self.task_loaded:
            return
        with open(export_file_name, 'w') as outfile:
            json.dump(self.model.voronoi_diagram.points, outfile)

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
            self.dragOnStart(event)
        elif self.main_view.action.get() == 3:
            self.changeColor(event)

    def dragOnStart(self, event):
        if not self.task_loaded:
            return
        try:
            self.model.voronoi_diagram.checkPointValid((event.x, event.y))
        except ValueError:
            return
        if self.main_view.action.get() != 2:
            return
        self._drag_start = (event.x, event.y)
        self._drag_nearest = self.model.voronoi_diagram.findNearestPoint(
            self._drag_start)
        self._drag_origin = \
            self.model.voronoi_diagram.points[self._drag_nearest]

    def dragOnDrag(self, event):
        if self.main_view.action.get() != 2:
            return
        delta = (event.x - self._drag_start[0],
                 event.y - self._drag_start[1])
        new_point = (self._drag_origin[0] + delta[0],
                     self._drag_origin[1] + delta[1])
        self.model.voronoi_diagram.editPoint(self._drag_nearest, new_point)

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
