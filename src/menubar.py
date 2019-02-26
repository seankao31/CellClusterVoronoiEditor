from tkinter import filedialog
import tkinter as tk

from pubsub import pub


class Menubar:
    def __init__(self, root):
        self.menubar = tk.Menu(root)
        self.fileMenu(root)
        self.editMenu()
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
            label='Open', command=self.file_open)
        self.file_menu.add_command(
            label='Load image', command=self.file_load_image)
        self.file_menu.add_command(
            label='Save', command=self.file_save)
        self.file_menu.add_command(
            label='Save as...', command=self.file_save_as)
        self.file_menu.add_command(
            label='Export Image', command=self.file_export_image)
        self.file_menu.add_command(
            label='Export Points', command=self.file_export_points)

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

    def file_export_image(self):
        name = filedialog.asksaveasfilename(
            defaultextension='.tiff', filetypes=self.image_file_types)
        pub.sendMessage('exportImage', export_file_name=name)

    def file_export_points(self):
        name = filedialog.asksaveasfilename(
            defaultextension='.json', filetypes=[('json files', '*.json')])
        pub.sendMessage('exportPoints', export_file_name=name)

    def editMenu(self):
        self.edit_menu = tk.Menu(self.menubar)
        self.edit_menu.add_command(
            labe='Undo', command=self.edit_undo)
        self.edit_menu.add_command(
            label="Redo", command=self.edit_redo)

        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)

    def edit_undo(self):
        pub.sendMessage('undo')

    def edit_redo(self):
        pub.sendMessage('redo')
