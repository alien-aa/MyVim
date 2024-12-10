from View.abstractions.observer import Observer

#TODO: реализация
class View(Observer):
    def __init__(self, display: IDisplay):
        self.display = display

    def update(self, message: dict) -> None:
        pass
