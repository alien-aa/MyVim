from abc import ABC, abstractmethod

from View.abstractions.observer import Observer


class IModelSubject(ABC):
    def __init__(self):
        self.observers: list[Observer] = []

    @abstractmethod
    def add_observer(self, new_one: Observer) -> None:
        pass

    @abstractmethod
    def remove_observer(self, item: Observer) -> None:
        pass

    @abstractmethod
    def notify(self, message: dict) -> None:
        pass
