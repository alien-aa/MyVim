from abc import ABC, abstractmethod


class ModelFacade(ABC):
    @abstractmethod
    def move_cursor(self, direction: int, option: int, value: int) -> None:
        pass

    @abstractmethod
    def change_pos(self, screen_direction: int) -> None:
        pass

    @abstractmethod
    def search(self, input_data: str, direction: int) -> None:
        pass

    @abstractmethod
    def files_action(self, name: str, option: int) -> None:
        pass

    @abstractmethod
    def post_input(self, char: str, option: int) -> None:
        pass

    @abstractmethod
    def copy(self, option: int) -> None:
        pass

    @abstractmethod
    def paste(self) -> None:
        pass

    @abstractmethod
    def delete(self, option: int) -> None:
        pass
