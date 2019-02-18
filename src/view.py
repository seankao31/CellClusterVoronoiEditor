import tkinter as tk


class View(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.title('Color Voronoi')
        self.actionList()
        self.color_list_view = None

    def actionList(self):
        self.action = tk.IntVar()
        self.action.set(0)  # initializing the choice, i.e. Python

        choices = [
            ("addPoint"),
            ("deletePoint"),
            ("changeColor")
        ]

        tk.Label(self,
                 text="""Choose action:""",
                 justify='left',
                 padx=0).pack()

        for val, choice in enumerate(choices):
            tk.Radiobutton(self,
                           text=choice,
                           indicatoron=0,
                           width=20,
                           padx=20,
                           variable=self.action,
                           value=val).pack(anchor='w')

    def colorList(self, color_list):
        if self.color_list_view is not None:
            self.color_list_view.destroy()
        self.color_list_view = ColorListView(self, color_list)
        self.color_list_view.pack()


class ColorListView(tk.Frame):
    def __init__(self, root, color_list=None):
        super().__init__(root)
        self.label = tk.Label(self,
                              text="""Choose color:""",
                              justify='left',
                              padx=0)
        self.label.pack()
        self.color = tk.IntVar()
        default = 0
        if list(color_list.keys()):
            default = list(color_list.keys())[0]
        self.color.set(default)
        self.update(color_list)

    def update(self, color_list):
        for index, color in color_list.items():
            tk.Radiobutton(self,
                           text=color,
                           indicatoron=0,
                           width=20,
                           padx=20,
                           variable=self.color,
                           value=index).pack(anchor='w')
