from abc import ABC, abstractmethod


class IModelFile(ABC):
    @abstractmethod
    def open_file(self, name: str) -> None:
        pass

    @abstractmethod
    def write_file(self, name: str) -> None:
        pass

