from Model.abstractions.icursor import IModelCursor


class ModelCursor(IModelCursor):
    def __init__(self):
        super().__init__()

    def move_cursor(self, new_x: int, new_y: int) -> None:
        self.x_pos = new_x if new_x >= 0 else self.x_pos
        self.y_pos = new_y if new_y >= 0 else self.y_pos
