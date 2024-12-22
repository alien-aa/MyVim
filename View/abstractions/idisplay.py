from abc import ABC, abstractmethod

class IDisplay(ABC):
    @abstractmethod
    def filename(self, message: str) -> None:
        pass

    @abstractmethod
    def update_text(self, line_num: int, text: str, changes_type: int) -> None:
        pass

    @abstractmethod
    def update_cursor(self, new_pos: list[int]) -> None:
        pass

    @abstractmethod
    def load_text(self, text: list[str]) -> None:
        pass

    @abstractmethod
    def change_page(self, direction: bool) -> None:
        pass
