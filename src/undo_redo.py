class UndoRedo:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def newAction(self, action):
        self.undo_stack.append(action)
        self.redo_stack = []

    def undo(self):
        if not self.undo_stack:
            return
        action = self.undo_stack.pop()
        action.undo()
        self.redo_stack.append(action)

    def redo(self):
        if not self.redo_stack:
            return
        action = self.redo_stack.pop()
        action.redo()
        self.undo_stack.append(action)


class Action:
    def __init__(self, undo, redo):
        self.undo = undo
        self.redo = redo
