import tkinter as tk


class DisplayOptionView(tk.Toplevel):
    def __init__(self, master, display_option):
        super().__init__(master)
        self.title('Display Option')
        self.resizable(False, False)
        display_option.view = self

        self.point_display_select = \
            self.PointDisplay(var=display_option.v_point_display)

        self.point_radius_label, self.point_radius_entry = \
            self.LabelEntry(text='Point Radius: ',
                            var=display_option.v_point_radius)
        self.point_color_label, self.point_color_entry = \
            self.RGBEntry(text='Point Color: ',
                          vars=display_option.v_point_color)

        _, self.line_width_entry = \
            self.LabelEntry(text='Line Width: ',
                            var=display_option.v_line_width)

        _, self.line_color_entry = \
            self.RGBEntry(text='Line Color: ',
                          vars=display_option.v_line_color)

        _, self.region_alpha_entry = \
            self.LabelEntry(text='Region Alpha: ',
                            var=display_option.v_region_alpha)

        _, self.scale_entry = \
            self.LabelEntry(text='Anti-alias Scale: ',
                            var=display_option.v_scale)

    def PointDisplay(self, var):
        choices = [
            ("Display Point"),
            ("Display Area"),
            ("Display Color")
        ]

        for val, choice in enumerate(choices):
            tk.Radiobutton(self,
                           text=choice,
                           width=20,
                           padx=0,
                           variable=var,
                           value=val).pack()

    def updatePointDisplay(self, choice):
        if choice == 0:
            self.point_radius_label.config(text='Point Radius: ')
            self.point_color_label.config(text='Point Color: ')
        else:
            self.point_radius_label.config(text='Text Size: ')
            self.point_color_label.config(text='Text Color: ')

    def LabelEntry(self, text, var):
        frame = tk.Frame(self)
        label = tk.Label(frame, text=text)
        label.pack(side='left')
        entry = tk.Entry(frame, width=3, textvariable=var)
        entry.pack(side='left')
        frame.pack(anchor='w')
        return label, entry

    def RGBEntry(self, text, vars):
        frame = tk.Frame(self)
        label = tk.Label(frame, text=text)
        label.pack(side='left')
        texts = ['R:', ' G:', ' B:']
        entries = []
        for i, t in enumerate(texts):
            tk.Label(frame, text=t).pack(side='left')
            e = tk.Entry(frame, width=3, textvariable=vars[i])
            e.pack(side='left')
            entries.append(e)
        frame.pack(anchor='w')
        return label, entries
