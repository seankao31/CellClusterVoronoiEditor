from src.controller import Controller


class App:
    def __init__(self, root):
        self.app = Controller(root)
        self.app.model.color_list.new()
        self.app.model.color_list[0] = (0, 0, 0)
        self.app.updateMainView()
