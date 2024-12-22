from Controller.state import ControllerState, NavigationMode, SearchMode, CommandMode, InputMode
from Model.abstractions.facade import ModelFacade
from View.abstractions.iinteractor import IInteractor


class Controller:
    def __init__(self,
                 model: ModelFacade,
                 interactor: IInteractor,
                 last_search: dict):
        self.state: ControllerState = NavigationMode(model, interactor, last_search)
        self.curr_command: str = ""


    def change_mode(self, new_mode: ControllerState) -> None:
        self.state = new_mode

    def state_handle(self) -> dict:
        in_value = self.state.handle_input()
        ret_value = {"state": "current",
                     "exit": False,
                     "clear_cmd": False}

        if in_value == "ENTER":
            self.curr_command += '\n'
            ret_value = self.state.handle_action(self.curr_command)
        elif in_value == "BACKSPACE" and len(self.curr_command) >= 1:
            self.curr_command = self.curr_command[:-1]
        elif in_value == "KEY_A3":
            self.state.model.change_pos(-1)
            x, y = self.state.input_adapter.get_cursor()
            self.state.model.move_cursor(x, 6, y)
        elif in_value == "KEY_C3":
            self.state.model.change_pos(1)
            x, y = self.state.input_adapter.get_cursor()
            self.state.model.move_cursor(x, 6, y)
        elif in_value == "KEY_DOWN":
            self.state.model.move_cursor(1, 1, 1)
        elif in_value == "KEY_UP":
            self.state.model.move_cursor(-1, 1, 1)
        elif in_value == "KEY_RIGHT":
            self.state.model.move_cursor(2, 1, 1)
        elif in_value == "KEY_LEFT":
            self.state.model.move_cursor(0, 1, 1)
        elif in_value == "ESCAPE":
            self.change_mode(NavigationMode(self.state.model, self.state.input_adapter, self.state.last_search))
            self.curr_command = ""
            self.state.show_state()
        elif len(in_value) == 1:
            self.curr_command += in_value
        elif in_value == "BACKSPACE" and self.state.curr_state() == "input":
            self.curr_command = "BACKSPACE"
        return ret_value

    def run(self):
        while True:
            self.state.show_state()
            result = self.state_handle()
            if result["exit"]:
                break
            if result["clear_cmd"]:
                self.state.clear_cmd()
                self.curr_command = "" if result["state"] != "cmd" else ":"
            if result["state"] == "cmd":
                self.change_mode(CommandMode(self.state.model, self.state.input_adapter, self.state.last_search))
            elif result["state"] == "search":
                self.change_mode(SearchMode(self.state.model, self.state.input_adapter, self.state.last_search))
            elif result["state"] == "input":
                self.change_mode(InputMode(self.state.model, self.state.input_adapter, self.state.last_search, result["mode_flags"][0]))
                self.curr_command = ""
            elif result["state"] == "navigation":
                self.change_mode(NavigationMode(self.state.model, self.state.input_adapter, self.state.last_search))
            result = self.state.handle_action(self.curr_command)
            if result["exit"]:
                break
            if result["clear_cmd"]:
                self.state.clear_cmd()
                self.curr_command = "" if result["state"] != "cmd" else ":"
            if result["state"] == "cmd":
                self.change_mode(CommandMode(self.state.model, self.state.input_adapter, self.state.last_search))
            elif result["state"] == "search":
                self.change_mode(SearchMode(self.state.model, self.state.input_adapter, self.state.last_search))
            elif result["state"] == "input":
                self.change_mode(InputMode(self.state.model, self.state.input_adapter, self.state.last_search, result["mode_flags"][0]))
                self.curr_command = ""
            elif result["state"] == "navigation":
                self.change_mode(NavigationMode(self.state.model, self.state.input_adapter, self.state.last_search))
