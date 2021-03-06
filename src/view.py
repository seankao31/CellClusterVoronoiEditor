import tkinter as tk

from pubsub import pub


class View(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.title('Color Voronoi')
        self.resizable(False, False)
        self.actionList()
        self.color_list_view = None

    def switchAction(self, action):
        self.action.set(action)

    def actionList(self):
        self.action = tk.IntVar()
        self.action.set(0)  # initializing the choice, i.e. Python

        choices = [
            ("Add Point"),
            ("Delete Point"),
            ("Edit Point"),
            ("Change Color")
        ]

        tk.Label(self,
                 text='Choose action:',
                 padx=0).pack()

        for val, choice in enumerate(choices):
            tk.Radiobutton(self,
                           text=choice,
                           width=20,
                           padx=0,
                           variable=self.action,
                           value=val).pack()

    def updateColorList(self, color_list):
        if self.color_list_view is not None:
            self.color_list_view.destroy()
        self.color_list_view = ColorListView(self, color_list)
        self.color_list_view.pack()


class ColorListView(tk.Frame):
    def __init__(self, root, color_list=None):
        super().__init__(root)
        self.label = tk.Label(self,
                              text='Choose color:',
                              padx=0)
        self.label.pack()

        self.new_button = tk.Button(self,
                                    text='New Color',
                                    command=self.newColor)
        self.new_button.pack()

        self.color = tk.IntVar()
        default = 0
        if list(color_list.keys()):
            default = list(color_list.keys())[0]
        self.color.set(default)
        self.canvas = tk.Canvas(self, borderwidth=0)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((10, 10), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.update(color_list)

    def newColor(self):
        pub.sendMessage('newColor')

    def update(self, color_list):
        for index, color in color_list.items():
            ColorEntry(self.frame, index, color, self.color).pack()

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),
                              width=250, height=500)


class ColorEntry(tk.Frame):
    def __init__(self, root, index, color, var):
        super().__init__(root)
        self.index = index
        self.radiobutton = tk.Radiobutton(self,
                                          text='Color {}'.format(index),
                                          indicatoron=0,
                                          width=20,
                                          padx=0,
                                          variable=var,
                                          value=index)
        self.radiobutton.pack(anchor='w')
        self.rgb = [tk.StringVar() for _ in range(3)]
        self.rgb[0].set(str(color[0]))
        self.rgb[1].set(str(color[1]))
        self.rgb[2].set(str(color[2]))

        self.entries = []
        texts = ['R:', ' G:', ' B:']
        for i, t in enumerate(texts):
            tk.Label(self, text=t).pack(side='left')
            e = tk.Entry(self, width=3, textvariable=self.rgb[i])
            e.pack(side='left')
            self.entries.append(e)
            self.rgb[i].trace('w', lambda *_, id=index, rgb=i:
                              self.changeEntry(id, rgb))

    def changeEntry(self, id, rgb):
        var = self.rgb[rgb]
        entry = self.entries[rgb]
        try:
            v = int(var.get())
            if v < 0 or v > 255:
                raise ValueError
        except ValueError:
            entry.config(fg='red')
            return
        entry.config(fg='black')
        color = tuple(int(self.rgb[i].get()) for i in range(3))
        pub.sendMessage('editColor', key=id, val=color)
