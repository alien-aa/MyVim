from abc import ABC, abstractmethod


class IModelCursor(ABC):
    @abstractmethod
    def move_cursor(self, new_x: int, new_y: int) -> None:
        pass
