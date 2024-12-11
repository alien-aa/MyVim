from abc import ABC, abstractmethod


class IModelCursor(ABC):
    def __init__(self):
        self.x_pos: int = 0
        self.y_pos: int = 0

    @abstractmethod
    def move_cursor(self, new_x: int, new_y: int) -> None:
        pass
