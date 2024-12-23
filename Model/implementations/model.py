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
                 subject: IModelSubject,

                 file_buffer: IModelFile,
                 cursor_buffer: IModelCursor,
                 text_buffer: IModelText):
        self.file = file
        self.cursor = cursor
        self.text = text
        self.subject = subject

        self.help_status = False
        self.cursor_buffer = cursor_buffer
        self.text_buffer = text_buffer
        self.file_buffer = file_buffer


    def move_cursor(self, direction: int, option: int, value: int) -> None:
        """
        directions:
        None no direction (for some options)
        -1 UP
        0 LEFT
        1 DOWN
        2 RIGHT
        options:
        1 move for value of positions (ULDR)
        2 move to border of string (RL)
        3 move for 1 word (RL)
        4 move to border of file (UD)
        5 move for value string
        6 move to (direction, value) as (x, y)
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
                            new_x = self.text.text[new_y].size()
                        else:
                            new_x = 0
                    elif new_x > self.text.text[new_y].size() >= 0:
                        if new_y < len(self.text.text) - 1:
                            new_x = 0
                            new_y += 1
                        else:
                            new_x = self.text.text[new_y].size()
                else:
                    if new_y < 0:
                        new_y = 0
                    elif new_y >= len(self.text.text) > 0:
                        new_y = len(self.text.text) - 1
                    if new_x > self.text.text[new_y].size() >= 0:
                        new_x = self.text.text[new_y].size()
                self.cursor.move_cursor(new_x, new_y)
                self.subject.notify({"action": "move_cursor",
                                     "new_pos": [new_x, new_y]})
                return
            case 2:
                new_x = 0
                new_y = self.cursor.y_pos
                new_x = self.text.text[new_y].size() if direction == 2 else new_x
                self.cursor.move_cursor(new_x, new_y)
                self.subject.notify({"action": "move_cursor",
                                     "new_pos": [new_x, new_y]})
                return
            case 3:
                if direction == 2:
                    new_x = self.cursor.x_pos
                    if new_x == self.text.text[self.cursor.y_pos].size():
                        if self.cursor.y_pos + 1 < len(self.text.text):
                            self.cursor.y_pos += 1
                            new_x = 0
                        else:
                            new_x = self.text.text[self.cursor.y_pos].size()
                    while (new_x < self.text.text[self.cursor.y_pos].size()
                           and self.text.text[self.cursor.y_pos][new_x] == ' '):
                        new_x += 1
                    while (new_x < self.text.text[self.cursor.y_pos].size()
                           and self.text.text[self.cursor.y_pos][new_x] != ' '):
                        new_x += 1
                    self.cursor.move_cursor(new_x, self.cursor.y_pos)
                    self.subject.notify({"action": "move_cursor",
                                         "new_pos": [new_x, self.cursor.y_pos]})

                elif direction == 0:
                    new_x = self.cursor.x_pos
                    if self.cursor.y_pos < len(self.text.text):
                        if new_x == 0 and self.cursor.y_pos > 0:
                            self.cursor.y_pos -= 1
                            new_x = len(
                                self.text.text[self.cursor.y_pos])
                        while new_x > 0 and self.text.text[self.cursor.y_pos][new_x - 1] == ' ':
                            new_x -= 1
                        while new_x > 0 and self.text.text[self.cursor.y_pos][new_x - 1] != ' ':
                            new_x -= 1
                    self.cursor.move_cursor(new_x, self.cursor.y_pos)
                    self.subject.notify({"action": "move_cursor", "new_pos": [new_x, self.cursor.y_pos]})
                return
            case 4:
                if direction == -1:
                    self.cursor.move_cursor(0, 0)
                    self.subject.notify({"action": "move_cursor",
                                         "new_pos": [0, 0]})
                elif direction == 1:
                    new_y = len(self.text.text) - 1
                    new_x = self.text.text[new_y].size()
                    self.cursor.move_cursor(new_x, new_y)
                    self.subject.notify({"action": "move_cursor",
                                         "new_pos": [new_x, new_y]})
                return
            case 5:
                value = len(self.text.text) - 1 if value >= len(self.text.text) else value
                self.cursor.move_cursor(0, value)
                self.subject.notify({"action": "move_cursor",
                                     "new_pos": [0, value]})
                return
            case 6:
                self.cursor.move_cursor(direction, value)
                self.subject.notify({"action": "move_cursor",
                                     "new_pos": [direction, value]})
            case _:
                return

    def change_pos(self, screen_direction: int) -> None:
        """
        direction:
        -1 UP
        1 DOWN
        """
        self.subject.notify({"action": "change_pos",
                             "new_pos": screen_direction})
        return

    def search(self, input_data: str, direction: int) -> None:
        """
        direction:
        -1 UP
        1 DOWN
        """
        new_x, new_y = self.text.search(input_data, direction, self.cursor.x_pos, self.cursor.y_pos)
        self.cursor.move_cursor(new_x, new_y)
        self.subject.notify({"action": "move_cursor",
                             "new_pos": [new_x, new_y]})
        return

    def files_action(self, name: str, option: int) -> None:
        """
        option:
        1 open (read)
        2 write name
        3 write curr
        4 no file
        """
        match option:
            case 1:
                self.file.open_file(name)
                self.subject.notify({"action": "file",
                                     "filename": name,
                                     "text": [str(item) for item in self.text.text]})
                return
            case 2:
                self.file.write_file(name)
                self.file.changed = False
                self.subject.notify({"action": "write",
                                     "filename": name})
                return
            case 3:
                if self.file.name != "":
                    self.file.write_file(self.file.name)
                    self.subject.notify({"action": "write",
                                         "filename": self.file.name})
                return
            case 4:
                self.file.name = ""
                self.file.changed = False
                self.subject.notify({"action": "no file",
                                     "filename": name})
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
        6 after cursor
        7 \n sym
        8 backspace
        """
        self.file.changed = True
        match option:
            case 1:
                self.text.input(self.cursor.x_pos, self.cursor.y_pos, char)
                self.cursor.x_pos += 1
                self.subject.notify({"action": "post",
                                     "string_num": self.cursor.y_pos,
                                     "string_value": str(self.text.text[self.cursor.y_pos]),
                                     "new_string": False})
                self.subject.notify({"action": "move_cursor",
                                     "new_pos": [self.cursor.x_pos, self.cursor.y_pos]})
                return
            case 2:
                self.cursor.move_cursor(0, self.cursor.y_pos)
                self.text.input(self.cursor.x_pos, self.cursor.y_pos, char)
                self.subject.notify({"action": "post",
                                     "string_num": self.cursor.y_pos,
                                     "string_value": str(self.text.text[self.cursor.y_pos]),
                                     "new_string": False})
                self.subject.notify({"action": "move_cursor",
                                     "new_pos": [self.cursor.x_pos, self.cursor.y_pos]})
                return
            case 3:
                self.cursor.move_cursor(self.text.text[self.cursor.y_pos].size(), self.cursor.y_pos)
                self.text.input(self.cursor.x_pos, self.cursor.y_pos, char)
                self.subject.notify({"action": "post",
                                     "string_num": self.cursor.y_pos,
                                     "string_value": str(self.text.text[self.cursor.y_pos]),
                                     "new_string": False})
                self.subject.notify({"action": "move_cursor",
                                     "new_pos": [self.cursor.x_pos, self.cursor.y_pos]})
                return
            case 4:
                self.cursor.move_cursor(0, self.cursor.y_pos)
                self.text.text[self.cursor.y_pos].clear()
                self.text.input(self.cursor.x_pos, self.cursor.y_pos, char)
                self.subject.notify({"action": "post",
                                     "string_num": self.cursor.y_pos,
                                     "string_value": str(self.text.text[self.cursor.y_pos]),
                                     "new_string": False})
                self.subject.notify({"action": "move_cursor",
                                     "new_pos": [self.cursor.x_pos, self.cursor.y_pos]})
                return
            case 5:
                self.text.delete_sym(self.cursor.x_pos, self.cursor.y_pos)
                self.text.input(self.cursor.x_pos, self.cursor.y_pos, char)
                self.subject.notify({"action": "post",
                                     "string_num": self.cursor.y_pos,
                                     "string_value": str(self.text.text[self.cursor.y_pos]),
                                     "new_string": False})
                self.subject.notify({"action": "move_cursor",
                                     "new_pos": [self.cursor.x_pos, self.cursor.y_pos]})
                return
            case 6:
                self.text.input(self.cursor.x_pos + 1, self.cursor.y_pos, char)
                self.subject.notify({"action": "post",
                                     "string_num": self.cursor.y_pos,
                                     "string_value": str(self.text.text[self.cursor.y_pos]),
                                     "new_string": False})
                self.subject.notify({"action": "move_cursor",
                                     "new_pos": [self.cursor.x_pos, self.cursor.y_pos]})
                return
            case 7:
                self.text.new_string(self.cursor.x_pos, self.cursor.y_pos)
                self.cursor.y_pos += 1
                self.cursor.x_pos = 0
                self.cursor.move_cursor(self.cursor.x_pos, self.cursor.y_pos)
                self.subject.notify({"action": "post",
                                     "string_num": self.cursor.y_pos - 1,
                                     "string_value": str(self.text.text[self.cursor.y_pos - 1]),
                                     "new_string": False})
                self.subject.notify({"action": "post",
                                     "string_num": self.cursor.y_pos,
                                     "string_value": str(self.text.text[self.cursor.y_pos]),
                                     "new_string": True})
                self.subject.notify({"action": "move_cursor",
                                     "new_pos": [self.cursor.x_pos, self.cursor.y_pos]})
                return
            case 8:
                line_num = self.cursor.y_pos
                sym_num = self.cursor.x_pos
                if line_num < len(self.text.text) and sym_num > 0:
                    self.cursor.x_pos -= 1
                    self.delete(1)
                    self.subject.notify({"action": "move_cursor",
                                         "new_pos": [self.cursor.x_pos, self.cursor.y_pos]})
                    return
                elif line_num > 0 and sym_num == 0:
                    prev_line = line_num - 1
                    if prev_line >= 0:
                        self.cursor.x_pos = self.text.text[prev_line].size()
                        self.text.go_to_previous(line_num)
                        self.delete(3)
                        self.cursor.y_pos -= 1
                        self.subject.notify({"action": "post",
                                             "string_num": self.cursor.y_pos,
                                             "string_value": str(self.text.text[self.cursor.y_pos]),
                                             "new_string": False})
                        self.subject.notify({"action": "move_cursor",
                                             "new_pos": [self.cursor.x_pos, prev_line]})
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
                return
            case 2:
                self.text.copy_word(self.cursor.x_pos, self.cursor.y_pos)
                return
            case _:
                return

    def paste(self) -> None:
        self.file.changed = True
        if self.text.buffer_state:
            self.text.paste_new_string(self.cursor.y_pos)
            self.subject.notify({"action": "paste_new",
                                 "string_num": self.cursor.y_pos + 1,
                                 "string_value": str(self.text.text[self.cursor.y_pos + 1])})
            return
        else:
            self.text.paste_in_string(self.cursor.x_pos, self.cursor.y_pos)
            self.subject.notify({"action": "paste_in",
                                 "string_num": self.cursor.y_pos,
                                 "string_value": str(self.text.text[self.cursor.y_pos])})
            return

    def delete(self, option: int) -> None:
        """
        option:
        1 char
        2 word
        3 string
        """
        self.file.changed = True
        match option:
            case 1:
                if self.text.text[self.cursor.y_pos].size() == self.cursor.x_pos and self.cursor.y_pos < len(self.text.text) - 1:
                    self.cursor.x_pos = self.text.text[self.cursor.y_pos]
                    self.text.go_to_previous(self.cursor.y_pos + 1)
                    self.subject.notify({"action": "post",
                                         "string_num": self.cursor.y_pos,
                                         "string_value": str(self.text.text[self.cursor.y_pos]),
                                         "new_string": False})
                    self.text.delete_str(self.cursor.y_pos + 1)
                    self.subject.notify({"action": "delete_string",
                                         "string_num": self.cursor.y_pos + 1})
                    self.subject.notify({"action": "move_cursor",
                                         "new_pos": [self.cursor.x_pos, self.cursor.y_pos]})
                    return
                if self.text.text[self.cursor.y_pos].size() > self.cursor.x_pos >= 0:
                    self.text.delete_sym(self.cursor.x_pos, self.cursor.y_pos)
                    self.subject.notify({"action": "delete",
                                         "string_num": self.cursor.y_pos,
                                         "string_value": str(self.text.text[self.cursor.y_pos])})
                    self.cursor.x_pos = min(self.cursor.x_pos, self.text.text[self.cursor.y_pos].size())
                    self.subject.notify({"action": "move_cursor",
                                         "new_pos": [self.cursor.x_pos, self.cursor.y_pos]})
                    return
            case 2:
                self.text.delete_word(self.cursor.x_pos, self.cursor.y_pos)
                self.subject.notify({"action": "delete",
                                     "string_num": self.cursor.y_pos,
                                     "string_value": str(self.text.text[self.cursor.y_pos])})
                self.cursor.x_pos = min(self.cursor.x_pos, self.text.text[self.cursor.y_pos].size())
                self.subject.notify({"action": "move_cursor",
                                     "new_pos": [self.cursor.x_pos, self.cursor.y_pos]})
                return
            case 3:
                self.text.delete_str(self.cursor.y_pos)
                self.subject.notify({"action": "delete_string",
                                     "string_num": self.cursor.y_pos})
                self.cursor.x_pos = min(self.cursor.x_pos, self.text.text[self.cursor.y_pos].size())
                self.subject.notify({"action": "move_cursor",
                                     "new_pos": [self.cursor.x_pos, self.cursor.y_pos]})
                return
            case _:
                return

    def file_status(self) -> bool:
        return self.file.changed

    def help(self, status: bool) -> None:
        if status != self.help_status:
            self.help_status = status
            self.text, self.text_buffer = self.text_buffer, self.text
            self.cursor, self.cursor_buffer = self.cursor_buffer, self.cursor
            self.file, self.file_buffer = self.file_buffer, self.file
            self.subject.notify({"action": "file",
                                 "filename": self.file.name if self.file.name != "" else "no file",
                                 "text": [str(item) for item in self.text.text]})
            self.subject.notify({"action": "move_cursor",
                                 "new_pos": [self.cursor.x_pos, self.cursor.y_pos]})

    def help_state(self) -> bool:
        return self.help_status

    def init_help(self, name: str) -> None:
        self.file_buffer.open_help(name)

