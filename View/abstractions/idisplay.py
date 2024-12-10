from abc import ABC, abstractmethod

class IDisplay(ABC):
    @abstractmethod
    def filename(self, message: str) -> None:
        pass

    @abstractmethod
    def update_editor(self, text: list[str], cursor: list[int], new_text_flag: bool) -> None:
        pass

    @abstractmethod
    def change_page(self, direction: bool) -> None:
        pass
