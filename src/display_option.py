import tkinter as tk

from pubsub import pub


class DisplayOption:
    def __init__(self):
        self.point_radius = 2
        self.point_color = (255, 0, 0)
        self.line_width = 4
        self.line_color = (255, 0, 0)

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
