from abc import ABC, abstractmethod


class ModelFacade(ABC):
    @abstractmethod
    def move_cursor(self, direction: int, option: int):
        pass

    @abstractmethod
    def change_pos(self, string_num: int, screen_direction: int):
        pass

    @abstractmethod
    def search(self, input_data: str, direction: bool):
        pass

    @abstractmethod
    def files_action(self, filename: str, option: int):
        pass

    @abstractmethod
    def post_input(self, char: str, option: int):
        pass

    @abstractmethod
    def copy(self, option: int):
        pass

    @abstractmethod
    def paste(self, option: int):
        pass

    @abstractmethod
    def delete(self, option: int):
        pass
