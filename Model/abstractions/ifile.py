from abc import ABC, abstractmethod

from Model.abstractions.itext import IModelText

class IModelFile(ABC):
    def __init__(self,
                 text: IModelText,
                 name: str | None):
        self.text = text
        self.name = name
        self.changed: bool = False

    @abstractmethod
    def open_file(self, name: str) -> None:
        pass

    @abstractmethod
    def write_file(self, name: str) -> None:
        pass

