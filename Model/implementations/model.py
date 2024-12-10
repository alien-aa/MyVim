from Model.abstractions.facade import ModelFacade

from Model.abstractions.ifile import IModelFile
from Model.abstractions.icursor import IModelCursor
from Model.abstractions.itext import IModelText
from Model.abstractions.isubject import IModelSubject


class Model(ModelFacade):
    def __init__(self,
                 file: IModelFile,
                 cursor: IModelCursor,
                 text: IModelText,
                 subject: IModelSubject):
        self.file = file
        self.cursor = cursor
        self.text = text
        self.subject = subject


    def move_cursor(self, direction: int, option: int):
        # TODO: implement method
        pass

    def change_pos(self, string_num: int, screen_direction: int):
        # TODO: implement method
        pass

    def search(self, input_data: str, direction: bool):
        # TODO: implement method
        pass

    def files_action(self, filename: str, option: int):
        # TODO: implement method
        pass

    def post_input(self, char: str, option: int):
        # TODO: implement method
        pass

    def copy(self, option: int):
        # TODO: implement method
        pass

    def paste(self, option: int):
        # TODO: implement method
        pass

    def delete(self, option: int):
        # TODO: implement method
        pass
