from View.abstractions.idisplay import IDisplay
from View.abstractions.iinteractor import IInteractor


class Adapter(IDisplay, IInteractor):
    def filename(self, message: str) -> None:
        pass

    def update_editor(self, text: list[str], cursor: list[int], new_text_flag: bool) -> None:
        pass

    def change_page(self, direction: bool) -> None:
        pass

    def read_char(self) -> str:
        pass

    def state(self, message: str) -> None:
        pass

    def read_cmd(self) -> str:
        pass

    def clear_cmd(self, new_cmd: str) -> None:
        pass
