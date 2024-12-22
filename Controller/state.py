from abc import ABC, abstractmethod

from Model.abstractions.facade import ModelFacade

from View.abstractions.iinteractor import IInteractor


class ControllerState(ABC):
    def __init__(self,
                 model: ModelFacade,
                 interactor: IInteractor,
                 last_search: dict):
        self.model = model
        self.input_adapter = interactor
        self.last_search = last_search

    @abstractmethod
    def handle_input(self) -> str:
        pass

    @abstractmethod
    def handle_action(self, curr_cmd: str) -> dict:
        pass

    @abstractmethod
    def show_state(self) -> None:
        pass

    @abstractmethod
    def clear_cmd(self):
        pass

    @abstractmethod
    def curr_state(self) -> str:
        pass

class NavigationMode(ControllerState):
    def __init__(self,
                 model: ModelFacade,
                 interactor: IInteractor,
                 last_search: dict):
        super().__init__(model, interactor, last_search)
        self.input_adapter.clear_cmd("")

    def handle_input(self) -> str:
        return self.input_adapter.read_cmd()

    def handle_action(self, curr_cmd: str) -> dict:
        ret_value = {"state": "current",
                     "exit": False,
                     "clear_cmd": False,
                     "mode_flags": []}

        if curr_cmd == ":":
            ret_value["state"] = "cmd"
        elif curr_cmd == "/":
            ret_value["state"] = "search"
        elif curr_cmd == "?":
            ret_value["state"] = "search"
        elif curr_cmd == "i":
            ret_value["state"] = "input"
            ret_value["mode_flags"].append(1)
        elif curr_cmd == "I":
            ret_value["state"] = "input"
            ret_value["mode_flags"].append(2)
        elif curr_cmd == "A":
            ret_value["state"] = "input"
            ret_value["mode_flags"].append(3)
        elif curr_cmd == "S":
            ret_value["state"] = "input"
            ret_value["mode_flags"].append(4)
        elif curr_cmd == "r":
            ret_value["state"] = "input"
            ret_value["mode_flags"].append(5)
        elif curr_cmd == "o":
            ret_value["state"] = "input"
            ret_value["mode_flags"].append(6)
        elif curr_cmd == "^" or curr_cmd == "0":
            self.model.move_cursor(direction=0, option=2, value=0)
            ret_value["clear_cmd"] = True
        elif curr_cmd == "$":
            self.model.move_cursor(direction=2, option=2, value=0)
            ret_value["clear_cmd"] = True
        elif curr_cmd == "w":
            self.model.move_cursor(direction=2, option=3, value=0)
            ret_value["clear_cmd"] = True
        elif curr_cmd == "b":
            self.model.move_cursor(direction=0, option=3, value=0)
            ret_value["clear_cmd"] = True
        elif curr_cmd == "gg":
            self.model.move_cursor(direction=-1, option=4, value=0)
            ret_value["clear_cmd"] = True
        elif curr_cmd == "G":
            self.model.move_cursor(direction=1, option=4, value=0)
            ret_value["clear_cmd"] = True
        elif len(curr_cmd) >= 2 and curr_cmd[-1] == "G" and curr_cmd[:-1].isdigit():
            self.model.move_cursor(direction=-1, option=5, value=int(curr_cmd[:-1]) - 1)
            ret_value["clear_cmd"] = True
        elif curr_cmd == "x":
            self.model.delete(option=1)
            ret_value["clear_cmd"] = True
        elif curr_cmd == "diw":
            self.model.delete(option=2)
            ret_value["clear_cmd"] = True
        elif curr_cmd == "dd":
            self.model.delete(option=3)
            ret_value["clear_cmd"] = True
        elif curr_cmd == "yy":
            self.model.copy(option=1)
            ret_value["clear_cmd"] = True
        elif curr_cmd == "yw":
            self.model.copy(option=2)
            ret_value["clear_cmd"] = True
        elif curr_cmd == "p":
            self.model.paste()
            ret_value["clear_cmd"] = True
        return ret_value

    def show_state(self) -> None:
        self.input_adapter.state("Navigation&Edit")

    def clear_cmd(self):
        self.input_adapter.clear_cmd("")

    def curr_state(self) -> str:
        return "navigation"

class SearchMode(ControllerState):
    def __init__(self,
                 model: ModelFacade,
                 interactor: IInteractor,
                 last_search: dict):
        super().__init__(model, interactor, last_search)


    def handle_input(self) -> str:
        return self.input_adapter.read_cmd()

    def handle_action(self, curr_cmd: str) -> dict:
        ret_value = {"state": "current",
                     "exit": False,
                     "clear_cmd": False}
        if curr_cmd == "n":
            self.model.search(input_data=self.last_search["data"], direction=self.last_search["dir"])
            ret_value["clear_cmd"] = True
        elif curr_cmd == "N":
            new_dir = self.last_search["dir"] * (-1)
            self.model.search(input_data=self.last_search["data"], direction=new_dir)
            ret_value["clear_cmd"] = True
        elif len(curr_cmd) >= 5 and curr_cmd[0] == "/" and curr_cmd[-4:] == "<CR>":
            self.last_search["dir"] = -1
            self.last_search["data"] = curr_cmd[1:-4]
            self.model.search(input_data=curr_cmd[1:-4], direction=-1)
            ret_value["clear_cmd"] = True
        elif len(curr_cmd) >= 5 and curr_cmd[0] == "?" and curr_cmd[-4:] == "<CR>":
            self.last_search["dir"] = 1
            self.last_search["data"] = curr_cmd[1:-4]
            self.model.search(input_data=curr_cmd[1:-4], direction=1)
            ret_value["clear_cmd"] = True

        return ret_value

    def show_state(self) -> None:
        self.input_adapter.state("Search")

    def clear_cmd(self):
        self.input_adapter.clear_cmd("")

    def curr_state(self) -> str:
        return "search"

class InputMode(ControllerState):
    def __init__(self,
                 model: ModelFacade,
                 interactor: IInteractor,
                 last_search: dict,
                 start_flag: int):
        super().__init__(model, interactor, last_search)
        self.start_flag = start_flag
        self.input_adapter.clear_cmd("")

    def handle_input(self) -> str:
        return self.input_adapter.read_char()

    def handle_action(self, curr_cmd: str) -> dict:
        ret_value = {"state": "current",
                     "exit": False,
                     "clear_cmd": False}

        if curr_cmd == "\n":
            self.model.post_input("", 7)
            ret_value["clear_cmd"] = True
        elif curr_cmd == "BACKSPACE":
            self.model.post_input("", 8)
            ret_value["clear_cmd"] = True
        elif len(curr_cmd) == 1:
            self.model.post_input(curr_cmd[0], self.start_flag)
            ret_value["clear_cmd"] = True
        self.start_flag = 6 if self.start_flag == 6 else 1
        return ret_value

    def show_state(self) -> None:
        self.input_adapter.state("Input")

    def clear_cmd(self):
        self.input_adapter.clear_cmd("")

    def curr_state(self) -> str:
        return "input"

class CommandMode(ControllerState):
    def __init__(self,
                 model: ModelFacade,
                 interactor: IInteractor,
                 last_search: dict):
        super().__init__(model, interactor, last_search)
        self.input_adapter.clear_cmd(":")

    def handle_input(self) -> str:
        return self.input_adapter.read_cmd()

    def handle_action(self, curr_cmd: str) -> dict:
        ret_value = {"state": "current",
                     "exit": False,
                     "clear_cmd": False}
        if curr_cmd == ":q\n":
            if not self.model.file_status():
                ret_value["exit"] = True
            else:
                ret_value["state"] = "cmd"
                ret_value["clear_cmd"] = True
        elif curr_cmd == ":q!\n":
            ret_value["exit"] = True
        elif curr_cmd[:3] == ":o " and curr_cmd[-1] == '\n' and len(curr_cmd) > 5:
            self.model.files_action(curr_cmd[3:-1], 1)
            ret_value["state"] = "navigation"
            ret_value["clear_cmd"] = True
        elif curr_cmd== ":w\n":
            self.model.files_action("", 3)
            ret_value["state"] = "cmd"
            ret_value["clear_cmd"] = True
        elif curr_cmd == ":x\n":
            self.model.files_action("", 3)
            ret_value["exit"] = True
        elif curr_cmd[:3] == ":w " and curr_cmd[-1] == '\n' and len(curr_cmd) > 5:
            self.model.files_action(curr_cmd[3:-1], 2)
            ret_value["exit"] = True
        elif curr_cmd[:4] == ":wq!\n":
            self.model.files_action("", 2)
            ret_value["exit"] = True
        elif len(curr_cmd) > 2 and curr_cmd[1:-1].isdigit() and curr_cmd[-1] == '\n':
            self.model.move_cursor(direction=-1, option=5, value=int(curr_cmd[1:-1]) - 1)
            ret_value["state"] = "cmd"
            ret_value["clear_cmd"] = True
        return ret_value

    def show_state(self) -> None:
        self.input_adapter.state("Command")

    def clear_cmd(self):
        self.input_adapter.clear_cmd(":")

    def curr_state(self) -> str:
        return "cmd"