from Controller.state import ControllerState, NavigationMode, SearchMode, CommandMode, InputMode
from Model.abstractions.facade import ModelFacade
from View.abstractions.iinteractor import IInteractor


class Controller:
    def __init__(self,
                 model: ModelFacade,
                 interactor: IInteractor):
        self.state: ControllerState = NavigationMode(model, interactor)
        self.curr_command: str = ""

        #TODO: пересмотреть методы, реализация

    def change_mode(self, new_mode: ControllerState) -> None:
        self.state = new_mode

    def state_handle(self) -> bool:
        in_value = self.state.handle_input()
        action = False
        if in_value == "BACKSPACE" and len(self.curr_command) >= 1:
            self.curr_command = self.curr_command[:-1]
        elif in_value == "KEY_DOWN":
            # self.state.model.move_cursor(1, 1, 1)
            action = True
        elif in_value == "KEY_UP":
            # self.state.model.move_cursor(2, 1, 1)
            action = True
        elif in_value == "KEY_RIGHT":
            # self.state.model.move_cursor(3, 1, 1)
            action = True
        elif in_value == "KEY_LEFT":
            # self.state.model.move_cursor(4, 1, 1)
            action = True
        elif in_value == "ESCAPE":
            if isinstance(self.state, NavigationMode):
                print("QUIT HELP")
            self.change_mode(NavigationMode(self.state.model, self.state.input_adapter))
            self.curr_command = ""
            self.state.show_state()
        elif len(in_value) == 1:
            self.curr_command += in_value
        return action

    def run(self):
        while True:
            self.state.show_state()
            result = self.state_handle()
            print(f"RESULT: {result}")
