from abc import ABC, abstractmethod


class IInteractor(ABC):
    @abstractmethod
    def read_char(self) -> str:
        pass

    @abstractmethod
    def state(self, message: str) -> None:
        pass

    @abstractmethod
    def read_cmd(self) -> str:
        pass

    @abstractmethod
    def clear_cmd(self, new_cmd: str) -> None:
        pass

    @abstractmethod
    def get_cursor(self) -> list[int]:
        pass
