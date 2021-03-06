from functools import partial
import json
import numpy as np
import pickle

from pubsub import pub

from display_option_view import DisplayOptionView
from menubar import Menubar
from model import Model
from task_view import TaskView
from undo_redo import Action, UndoRedo
from view import View


class Controller:
    def __init__(self, root):
        root.config(menu=Menubar(root).menubar)
        self.model = Model()
        self.undo_redo = UndoRedo()
        self.main_view = View(root)
        self.display_option_view = DisplayOptionView(
            self.main_view, self.model.display_option)
        self.taskViewInit()
        pub.subscribe(self.openFile, 'openFile')
        pub.subscribe(self.taskLoadImage, 'loadImageFile')
        pub.subscribe(self.taskExportImage, 'exportImage')
        pub.subscribe(self.taskExportData, 'exportData')
        pub.subscribe(self.taskSaveFile, 'saveFile')
        pub.subscribe(self.model.color_list.new, 'newColor')
        pub.subscribe(self.updateTaskView, 'updateVoronoi')
        pub.subscribe(self.updateTaskView, 'updateDisplayOption')
        pub.subscribe(self.updatePointDisplay,
                      'updateDisplayOption.pointDisplay')
        pub.subscribe(self.model.color_list.__setitem__, 'editColor')
        pub.subscribe(self.updateTaskView, 'updateColorList')
        pub.subscribe(self.updateMainView, 'updateColorList.newColor')
        pub.subscribe(self.chooseNewColor, 'updateColorList.newColor')
        pub.subscribe(self.undo_redo.undo, 'undo')
        pub.subscribe(self.undo_redo.redo, 'redo')
        # self.task_view.bind('<Button-1>', self.taskEventHandler)

    def openFile(self, open_file_name):
        if self.task_view.window_deleted:
            self.taskViewInit()
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

    def taskViewInit(self):
        self.task_view = TaskView(self.main_view)
        self.task_loaded = False
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

    def taskLoadImage(self, image_file_name):
        if self.task_view.window_deleted:
            self.taskViewInit()
        self.task_loaded = True
        self.model.setupTask(image_file_name)
        self.taskDisplayImage(self.model.back_image)

    def taskExportImage(self, export_file_name):
        if not self.task_loaded:
            return
        self.model.blend_image_voronoi.save(export_file_name)

    def taskExportData(self, export_file_name):
        if not self.task_loaded:
            return
        with open(export_file_name, 'w') as outfile:
            data = {}

            # points
            data['points'] = []
            for i in range(len(self.model.voronoi_diagram.points)):
                point_data = {}
                point_data['point_id'] = i
                point_data['position'] = self.model.voronoi_diagram.points[i]
                point_data['region_color'] = \
                    self.model.voronoi_diagram.region_color_map[i]
                area = -1
                if self.model.voronoi_diagram.areas:
                    area = self.model.voronoi_diagram.areas[i]
                point_data['region_area'] = area
                data['points'].append(point_data)

            # color list
            data['colors'] = []
            for key, val in self.model.color_list.colors.items():
                color_data = {}
                color_data['color_id'] = key
                if isinstance(val[0], np.generic):
                    color_data['rgb'] = tuple(v.item() for v in val)
                else:
                    color_data['rgb'] = val
                data['colors'].append(color_data)

            json.dump(data, outfile, indent=4)

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
                                     x=event.x,
                                     y=event.y,
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
                                     x=point[0],
                                     y=point[1],
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

    def updatePointDisplay(self):
        self.display_option_view.updatePointDisplay(
            self.model.display_option.point_display)

    def updateMainView(self):
        self.main_view.updateColorList(self.model.color_list)

    def chooseNewColor(self):
        self.main_view.color_list_view.color.set(
            list(self.model.color_list.keys())[-1])
