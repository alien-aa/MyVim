from Model.abstractions.isubject import IModelSubject
from Model.abstractions.observer import Observer


class ModelSubject(IModelSubject):
    def __init__(self):
        super().__init__()

    def add_observer(self, new_one: Observer) -> None:
        self.observers.append(new_one)

    def remove_observer(self, item: Observer) -> None:
        self.observers.remove(item)

    def notify(self, message: dict) -> None:
        for item in self.observers:
            item.update(message)
