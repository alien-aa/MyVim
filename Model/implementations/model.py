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


    def move_cursor(self, direction: int | None, option: int, value: int | None) -> None:
        """
        directions:
        None no direction (for some options)
        -1 UP
        0 LEFT
        1 DOWN
        2 RIGHT
        options:
        1 move for value of positions (ULDR)
        2 move to border of string (RL, value = None)
        3 move for 1 word (RL, value = None)
        4 move to border of file (UD, value = None)
        5 move for value string (direction = None)
        """
        match option:
            case 1:
                new_y = -value if direction == -1 else 0
                new_y = value if direction == 1 else new_y
                new_x = -value if direction == 0 else 0
                new_x = value if direction == 2 else new_x
                new_x += self.cursor.x_pos
                new_y += self.cursor.y_pos
                if direction % 2 == 0:
                    if new_x < 0:
                        if new_y > 0:
                            new_y -= 1
                            new_x = self.text.text[new_y].size() - 1
                        else:
                            new_x = 0
                    elif new_x >= self.text.text[new_y].size() > 0:
                        if new_y < len(self.text.text) - 1:
                            new_x = 0
                            new_y += 1
                        else:
                            new_x = self.text.text[new_y].size() - 1
                else:
                    if new_y < 0:
                        new_y = 0
                    elif new_y >= len(self.text.text) > 0:
                        new_y = len(self.text.text) - 1
                    if new_x >= self.text.text[new_y].size() > 0:
                        new_x = self.text.text[new_y].size() - 1
                self.cursor.move_cursor(new_x, new_y)
                self.subject.notify({}) #TODO дописать сообщение
                return
            case 2:
                new_x = 0
                new_y = self.cursor.y_pos
                new_x = self.text.text[new_y].size() - 1 if direction == 2 else new_x
                self.cursor.move_cursor(new_x, new_y)
                self.subject.notify({}) #TODO дописать сообщение
                return
            case 3:
                if direction == 2:
                    new_x = self.cursor.x_pos
                    new_x = new_x + 1 if (self.text.text[self.cursor.y_pos][new_x] == ' '
                                          and new_x != self.text.text[self.cursor.y_pos].size() - 1) else new_x
                    while (self.text.text[self.cursor.y_pos][new_x] != ' '
                           and new_x != self.text.text[self.cursor.y_pos].size() - 1):
                        new_x += 1
                    self.cursor.move_cursor(new_x, self.cursor.y_pos)
                    self.subject.notify({}) #TODO дописать сообщение
                elif direction == 0:
                    new_x = self.cursor.x_pos
                    new_x = new_x - 1 if self.text.text[self.cursor.y_pos][new_x] == ' ' and new_x != 0 else new_x
                    while self.text.text[self.cursor.y_pos][new_x] != ' ' and new_x != 0:
                        new_x -= 1
                    self.cursor.move_cursor(new_x, self.cursor.y_pos)
                    self.subject.notify({}) #TODO дописать сообщение
                return
            case 4:
                if direction == -1:
                    self.cursor.move_cursor(0, 0)
                elif direction == 1:
                    new_y = len(self.text.text) - 1
                    new_x = self.text.text[new_y].size() - 1
                    self.cursor.move_cursor(new_x, new_y)
                self.subject.notify({}) #TODO дописать сообщение
                return
            case 5:
                value = len(self.text.text) - 1 if value >= len(self.text.text) else value
                self.cursor.move_cursor(0, value)
                self.subject.notify({}) #TODO дописать сообщение
                return
            case _:
                return

    def change_pos(self, string_num: int, screen_direction: int, num_on_screen: int) -> None:
        """
        direction:
        -1 UP
        1 DOWN
        """
        self.move_cursor(screen_direction, 1, num_on_screen)
        self.subject.notify({}) #TODO дописать сообщение
        return

    def search(self, input_data: str, direction: bool) -> None:
        """
        direction:
        -1 UP
        1 DOWN
        """
        new_x, new_y = self.text.search(input_data, direction, self.cursor.x_pos, self.cursor.y_pos)
        self.cursor.move_cursor(new_x, new_y)
        self.subject.notify({}) #TODO дописать сообщение
        return

    def files_action(self, name: str, option: int) -> None:
        """
        option:
        1 open (read)
        2 write
        3 no file (without saving)
        4 no file (saving)
        """
        # TODO: implement method
        match option:
            case 1:
                self.file.open_file(name)
                self.subject.notify({}) #TODO дописать сообщение
                return
            case 2:
                self.file.write_file(name)
                self.subject.notify({}) #TODO дописать сообщение
                return
            case 3:
                self.file.name = None
                self.file.changed = False
                self.subject.notify({}) #TODO дописать сообщение
                return
            case 4:
                self.file.write_file(name)
                self.file.name = None
                self.file.changed = False
                self.subject.notify({}) #TODO дописать сообщение
                return
            case _:
                return

    def post_input(self, char: str, option: int) -> None:
        """
        option:
        1 before cursor
        2 from beginning of string
        3 from ending of string
        4 erase string & write
        5 replace char
        """
        # TODO: implement method
        match option:
            case 1:
                self.text.input(self.cursor.x_pos, self.cursor.y_pos, char)
                self.subject.notify({}) #TODO дописать сообщение
                return
            case 2:
                self.cursor.move_cursor(0, self.cursor.y_pos)
                self.text.input(self.cursor.x_pos, self.cursor.y_pos, char)
                self.subject.notify({}) #TODO дописать сообщение
                return
            case 3:
                self.cursor.move_cursor(self.text.text[self.cursor.y_pos].size() - 1, self.cursor.y_pos)
                self.text.input(self.cursor.x_pos, self.cursor.y_pos, char)
                self.subject.notify({}) #TODO дописать сообщение
                return
            case 4:
                self.cursor.move_cursor(0, self.cursor.y_pos)
                self.text.text[self.cursor.y_pos].clear()
                self.text.input(self.cursor.x_pos, self.cursor.y_pos, char)
                self.subject.notify({}) #TODO дописать сообщение
                return
            case 5:
                self.text.delete_sym(self.cursor.x_pos, self.cursor.y_pos)
                self.text.input(self.cursor.x_pos, self.cursor.y_pos, char)
                self.subject.notify({}) #TODO дописать сообщение
                return
            case _:
                return

    def copy(self, option: int) -> None:
        """
        option:
        1 string
        2 word
        """
        match option:
            case 1:
                self.text.copy_string(self.cursor.y_pos)
                self.subject.notify({}) #TODO дописать сообщение
                return
            case 2:
                self.text.copy_word(self.cursor.x_pos, self.cursor.y_pos)
                self.subject.notify({}) #TODO дописать сообщение
                return
            case _:
                return

    def paste(self) -> None:
        if self.text.buffer_state:
            self.text.paste_new_string(self.cursor.y_pos)
            self.subject.notify({}) #TODO дописать сообщение
            return
        else:
            self.text.paste_in_string(self.cursor.x_pos, self.cursor.y_pos)
            self.subject.notify({}) #TODO дописать сообщение
            return

    def delete(self, option: int) -> None:
        """
        option:
        1 char
        2 word
        3 string
        """
        match option:
            case 1:
                self.text.replace_sym(self.cursor.x_pos, self.cursor.y_pos, '')
                self.subject.notify({}) #TODO дописать сообщение
                return
            case 2:
                self.text.delete_word(self.cursor.x_pos, self.cursor.y_pos)
                self.subject.notify({}) #TODO дописать сообщение
                return
            case 3:
                self.text.delete_str(self.cursor.y_pos)
                self.subject.notify({}) #TODO дописать сообщение
                return
            case _:
                return
