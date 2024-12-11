from abc import ABC, abstractmethod
import Model.MyString.mystring as mystring


class  IModelText(ABC):
    def __init__(self):
        self.text: list[mystring.MyString] = [mystring.MyString("")]
        self.buffer: mystring.MyString = mystring.MyString("")

    @abstractmethod
    def search(self, input_data: str, direction: bool, start_x: int, start_y: int) -> list[int]:
        pass

    @abstractmethod
    def copy_string(self, line_num: int) -> bool:
        pass

    @abstractmethod
    def copy_word(self, sym_num: int, line_num: int) -> bool:
        pass

    @abstractmethod
    def paste_new_string(self, line_num: int) -> bool:
        pass

    @abstractmethod
    def paste_in_string(self, sym_num: int, line_num: int) -> bool:
        pass

    @abstractmethod
    def delete_sym(self, sym_num: int, line_num: int) -> bool:
        pass

    @abstractmethod
    def delete_word(self, sym_num: int, line_num: int) -> bool:
        pass

    @abstractmethod
    def delete_str(self, line_num: int) -> bool:
        pass

    @abstractmethod
    def input(self, sym_num: int, line_num: int, input_data: str) -> bool:
        pass

    @abstractmethod
    def replace_sym(self, sym_num: int, line_num: int, input_data: str) -> bool:
        pass
