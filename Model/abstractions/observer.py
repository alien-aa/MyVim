from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, message: dict) -> None:
        pass
