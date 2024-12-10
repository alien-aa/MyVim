from abc import ABC, abstractmethod

from Model.abstractions.facade import ModelFacade

from View.abstractions.iinteractor import IInteractor


class ControllerState(ABC):
    def __init__(self,
                 model: ModelFacade,
                 interactor: IInteractor):
        self.model = model
        self.input_adapter = interactor

    #TODO: определить и написать необходимые методы


class NavigationMode(ControllerState):
    def __init__(self,
                 model: ModelFacade,
                 interactor: IInteractor):
        super().__init__(model, interactor)
    #TODO: определить и написать необходимые методы


class SearchMode(ControllerState):
    def __init__(self,
                 model: ModelFacade,
                 interactor: IInteractor):
        super().__init__(model, interactor)
    #TODO: определить и написать необходимые методы


class InputMode(ControllerState):
    def __init__(self,
                 model: ModelFacade,
                 interactor: IInteractor):
        super().__init__(model, interactor)
    #TODO: определить и написать необходимые методы


class CommandMode(ControllerState):
    def __init__(self,
                 model: ModelFacade,
                 interactor: IInteractor):
        super().__init__(model, interactor)
    #TODO: определить и написать необходимые методы
