from Controller.state import ControllerState, NavigationMode
from Model.abstractions.facade import ModelFacade
from View.abstractions.iinteractor import IInteractor


class Controller:
    def __init__(self,
                 model: ModelFacade,
                 interactor: IInteractor):
        self.state: ControllerState = NavigationMode(model, interactor)
        self.curr_command: str = ""

        #TODO: методы, реализация