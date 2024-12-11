from abc import ABC, abstractmethod

from Model.abstractions.facade import ModelFacade

from View.abstractions.iinteractor import IInteractor


class ControllerState(ABC):
    def __init__(self,
                 model: ModelFacade,
                 interactor: IInteractor):
        self.model = model
        self.input_adapter = interactor

    @abstractmethod
    def handle_input(self) -> str:
        pass

    @abstractmethod
    def handle_action(self, curr_smd: str) -> dict:
        pass

    @abstractmethod
    def show_state(self) -> None:
        pass

    @abstractmethod
    def clear_cmd(self):
        pass

class NavigationMode(ControllerState):
    def __init__(self,
                 model: ModelFacade,
                 interactor: IInteractor):
        super().__init__(model, interactor)

    def handle_input(self) -> str:
        return self.input_adapter.read_cmd()

    def handle_action(self, curr_smd: str) -> dict:
        pass

    def show_state(self) -> None:
        self.input_adapter.state("Navigation&Edit")

    def clear_cmd(self):
        self.input_adapter.clear_cmd("")



class SearchMode(ControllerState):
    def __init__(self,
                 model: ModelFacade,
                 interactor: IInteractor):
        super().__init__(model, interactor)

    def handle_input(self) -> str:
        return self.input_adapter.read_cmd()

    def handle_action(self, curr_smd: str) -> dict:
        pass

    def show_state(self) -> None:
        self.input_adapter.state("Search")

    def clear_cmd(self):
        self.input_adapter.clear_cmd("")


class InputMode(ControllerState):
    def __init__(self,
                 model: ModelFacade,
                 interactor: IInteractor):
        super().__init__(model, interactor)

    def handle_input(self) -> str:
        return self.input_adapter.read_cmd()

    def handle_action(self, curr_smd: str) -> dict:
        pass

    def show_state(self) -> None:
        self.input_adapter.state("Input")

    def clear_cmd(self):
        self.input_adapter.clear_cmd("")


class CommandMode(ControllerState):
    def __init__(self,
                 model: ModelFacade,
                 interactor: IInteractor):
        super().__init__(model, interactor)

    def handle_input(self) -> str:
        return self.input_adapter.read_cmd()

    def handle_action(self, curr_smd: str) -> dict:
        pass

    def show_state(self) -> None:
        self.input_adapter.state("Command")

    def clear_cmd(self):
        self.input_adapter.clear_cmd(":")
