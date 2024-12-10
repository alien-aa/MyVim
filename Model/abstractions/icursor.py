from abc import ABC, abstractmethod

#TODO: возвращаемые значения методов - подписать типы
class IModelCursor(ABC):
    @abstractmethod
    def move_cursor(self, direction: int, option: int):
        pass

    @abstractmethod
    def change_pos(self, string_num: int, screen_direction: int):
        pass
