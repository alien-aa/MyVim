from abc import ABC, abstractmethod

#TODO: возвращаемые значения методов - подписать типы
class  IModelText(ABC):
    @abstractmethod
    def search(self, input_data: str, direction: bool):
        pass

    @abstractmethod
    def copy_string(self, sym_num: int, line_num: int):
        pass

    @abstractmethod
    def copy_word(self, sym_num: int, line_num: int):
        pass

    @abstractmethod
    def paste(self, sym_num: int, line_num: int):
        pass

    @abstractmethod
    def delete_sym(self, sym_num: int, line_num: int):
        pass

    @abstractmethod
    def delete_word(self, sym_num: int, line_num: int):
        pass

    @abstractmethod
    def delete_str(self, line_num: int):
        pass

    @abstractmethod
    def input(self, sym_num: int, line_num: int):
        pass

    @abstractmethod
    def replace_word(self, sym_num: int, line_num: int):
        pass

    @abstractmethod
    def replace_sym(self, sym_num: int, line_num: int):
        pass
