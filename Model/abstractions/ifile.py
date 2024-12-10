from abc import ABC, abstractmethod

#TODO: возвращаемые значения методов - подписать типы
class IModelFile(ABC):
    @abstractmethod
    def open_file(self, filename: str):
        pass

    @abstractmethod
    def write_file(self, filename: str):
        pass

    @abstractmethod
    def close_file(self, save_flag: bool):
        pass
