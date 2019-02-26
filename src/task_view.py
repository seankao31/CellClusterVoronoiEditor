import tkinter as tk

from PIL import ImageTk
from pubsub import pub


class TaskView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('Task')
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side='left')
        self.resizable(False, False)
        self.bind('<Button-1>', self.clickEvent)
        self.bind('<Command-z>', lambda *_: pub.sendMessage('undo'))
        self.bind('<Command-Z>', lambda *_: pub.sendMessage('redo'))
        self.bind('<Command-a>', lambda *_: pub.sendMessage('switchAction',
                                                            action=0))
        self.bind('<Command-d>', lambda *_: pub.sendMessage('switchAction',
                                                            action=1))
        self.bind('<Command-c>', lambda *_: pub.sendMessage('switchAction',
                                                            action=2))
        self.bind('<Command-n>', lambda *_: pub.sendMessage('newColor'))

    def displayImage(self, image):
        self.photo_image = photo_image = ImageTk.PhotoImage(image)
        self.width, self.height = width, height = image.size
        self.canvas.config(width=width, height=height)
        self.canvas.create_image((0, 0), image=photo_image, anchor='nw')

    def clickEvent(self, event):
        pub.sendMessage('taskViewClick', event=event)
