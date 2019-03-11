import tkinter as tk

from pubsub import pub


class DisplayOption:
    def __init__(self):
        self.point_display = 0
        self.point_radius = 2
        self.point_color = (255, 0, 0)
        self.line_width = 4
        self.line_color = (255, 0, 0)
        self.region_alpha = 0.5
        self.scale = 2

        self.v_point_display = tk.IntVar()
        self.v_point_display.set(self.point_display)
        self.v_point_display.trace('w', lambda *_: self.setPointDisplay())

        self.v_point_radius = tk.StringVar()
        self.v_point_radius.set(str(self.point_radius))
        self.v_point_radius.trace('w', lambda *_: self.setPointRadius())

        self.v_point_color = [tk.StringVar() for _ in range(3)]
        for i in range(3):
            self.v_point_color[i].set(str(self.point_color[i]))
            self.v_point_color[i].trace('w', lambda *_: self.setPointColor())

        self.v_line_width = tk.StringVar()
        self.v_line_width.set(str(self.line_width))
        self.v_line_width.trace('w', lambda *_: self.setLineWidth())

        self.v_line_color = [tk.StringVar() for _ in range(3)]
        for i in range(3):
            self.v_line_color[i].set(str(self.line_color[i]))
            self.v_line_color[i].trace('w', lambda *_: self.setLineColor())

        self.v_region_alpha = tk.StringVar()
        self.v_region_alpha.set(str(self.region_alpha))
        self.v_region_alpha.trace('w', lambda *_: self.setRegionAlpha())

        self.v_scale = tk.StringVar()
        self.v_scale.set(str(self.scale))
        self.v_scale.trace('w', lambda *_: self.setScale())

    def setVariables(self):
        self.v_point_display.set(self.point_display)
        self.v_point_radius.set(str(self.point_radius))
        self.v_line_width.set(str(self.line_width))
        self.v_region_alpha.set(str(self.region_alpha))
        point_color = self.point_color
        line_color = self.line_color
        for i in range(3):
            self.v_point_color[i].set(str(point_color[i]))
            self.v_line_color[i].set(str(line_color[i]))

    def setPointDisplay(self):
        self.point_display = self.v_point_display.get()
        pub.sendMessage('updateDisplayOption.pointDisplay')

    def setPointRadius(self):
        v = 0
        try:
            v = int(self.v_point_radius.get())
            if v < 0:
                raise ValueError
        except ValueError:
            self.view.point_radius_entry.config(fg='red')
            return
        self.view.point_radius_entry.config(fg='black')
        self.point_radius = v
        pub.sendMessage('updateDisplayOption')

    def setPointColor(self):
        for var, entry in zip(self.v_point_color, self.view.point_color_entry):
            try:
                v = int(var.get())
                if v < 0 or v > 255:
                    raise ValueError
            except ValueError:
                entry.config(fg='red')
                return
            entry.config(fg='black')
        self.point_color = \
            tuple(int(self.v_point_color[i].get()) for i in range(3))
        pub.sendMessage('updateDisplayOption')

    def setLineWidth(self):
        v = 0
        try:
            v = int(self.v_line_width.get())
            if v < 0:
                raise ValueError
        except ValueError:
            self.view.line_width_entry.config(fg='red')
            return
        self.view.line_width_entry.config(fg='black')
        self.line_width = v
        pub.sendMessage('updateDisplayOption')

    def setLineColor(self):
        for var, entry in zip(self.v_line_color, self.view.line_color_entry):
            try:
                v = int(var.get())
                if v < 0 or v > 255:
                    raise ValueError
            except ValueError:
                entry.config(fg='red')
                return
            entry.config(fg='black')
        self.line_color = \
            tuple(int(self.v_line_color[i].get()) for i in range(3))
        pub.sendMessage('updateDisplayOption')

    def setRegionAlpha(self):
        v = 0
        try:
            v = float(self.v_region_alpha.get())
            if v < 0 or v > 1:
                raise ValueError
        except ValueError:
            self.view.region_alpha_entry.config(fg='red')
            return
        self.view.region_alpha_entry.config(fg='black')
        self.region_alpha = v
        pub.sendMessage('updateDisplayOption')

    def setScale(self):
        v = 0
        try:
            v = int(self.v_scale.get())
            if v <= 0:
                raise ValueError
        except ValueError:
            self.view.scale_entry.config(fg='red')
            return
        self.view.scale_entry.config(fg='black')
        self.scale = v
        pub.sendMessage('updateDisplayOption')
