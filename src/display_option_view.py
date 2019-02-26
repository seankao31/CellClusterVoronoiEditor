import tkinter as tk


class DisplayOptionView(tk.Toplevel):
    def __init__(self, master, display_option):
        super().__init__(master)
        self.title('Display Option')
        self.resizable(False, False)
        display_option.view = self

        self.point_radius_entry = \
            self.LabelEntry(text='Point Radius: ',
                            var=display_option.v_point_radius)
        self.point_color_entry = \
            self.RGBEntry(text='Point Color: ',
                          vars=display_option.v_point_color)

        self.line_width_entry = \
            self.LabelEntry(text='Line Width: ',
                            var=display_option.v_line_width)

        self.line_color_entry = \
            self.RGBEntry(text='Line Color: ',
                          vars=display_option.v_line_color)

        self.region_alpha_entry = \
            self.LabelEntry(text='Region Alpha: ',
                            var=display_option.v_region_alpha)

    def LabelEntry(self, text, var):
        frame = tk.Frame(self)
        label = tk.Label(frame, text=text)
        label.pack(side='left')
        entry = tk.Entry(frame, width=3, textvariable=var)
        entry.pack(side='left')
        frame.pack(anchor='w')
        return entry

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
        return entries
