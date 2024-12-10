from View.abstractions.observer import Observer

from View.abstractions.idisplay import IDisplay

#TODO: реализация
class View(Observer):
    def __init__(self, display: IDisplay):
        self.display = display

    def update(self, message: dict) -> None:
        pass
