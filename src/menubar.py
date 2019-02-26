from tkinter import filedialog
import tkinter as tk

from pubsub import pub


class Menubar:
    def __init__(self, root):
        self.menubar = tk.Menu(root)
        self.fileMenu(root)
        self.save_file_name = None

    def fileMenu(self, root):
        self.image_file_types = [
            ('jpeg files', '*.jpg'),
            ('tiff files', '*.tiff'),
            ('tif files', '*.tif'),
            ('png files', '*.png')
        ]
        self.file_menu = tk.Menu(self.menubar)
        self.file_menu.add_command(
            labe='Open', command=self.file_open)
        self.file_menu.add_command(
            label="Load image", command=self.file_load_image)
        self.file_menu.add_command(
            label="Save", command=self.file_save)
        self.file_menu.add_command(
            label="Save as...", command=self.file_save_as)
        self.file_menu.add_command(
            label="Export", command=self.file_export)

        self.file_menu.add_separator()

        self.file_menu.add_command(label="Exit", command=root.destroy)

        self.menubar.add_cascade(label="File", menu=self.file_menu)

    def file_open(self):
        name = filedialog.askopenfilename(
            filetypes=[('cvdata files', '*.cvdata')])
        self.save_file_name = name
        pub.sendMessage('openFile', open_file_name=name)

    def file_load_image(self):
        name = filedialog.askopenfilename(
            filetypes=self.image_file_types)
        pub.sendMessage('loadImageFile', image_file_name=name)

    def file_save(self):
        if self.save_file_name is None:
            self.file_save_as()
        else:
            pub.sendMessage('saveFile', save_file_name=self.save_file_name)

    def file_save_as(self):
        name = filedialog.asksaveasfilename(
            defaultextension='.cvdata',
            filetypes=[('cvdata files', '*.cvdata')])
        self.save_file_name = name
        pub.sendMessage('saveFile', save_file_name=name)

    def file_export(self):
        name = filedialog.asksaveasfilename(
            defaultextension='.tiff', filetypes=self.image_file_types)
        pub.sendMessage('exportImage', export_file_name=name)
