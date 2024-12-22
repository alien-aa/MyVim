import Model.MyString.mystring as mystring

from Model.abstractions.itext import IModelText


class ModelText(IModelText):
    def __init__(self):
        super().__init__()


    def search(self, input_data: str, direction: int, start_x: int, start_y: int) -> list[int]:
        try:
            x, y = start_x, start_y
            if start_y >= len(self.text) or start_x >= self.text[start_y].size():
                return [x, y]
            if direction > 0:
                index = self.text[start_y].find(input_data, start_x)
                if index < 0:
                    for i in range(start_y + 1, len(self.text)):
                        if self.text[i].size() == 0:
                            continue
                        index = self.text[i].find(input_data)
                        if index >= 0:
                            x = index
                            y = i
                            break
            elif direction < 0:
                index = self.text[start_y].find(input_data)
                index = -1 if index >= start_x else index
                if index < 0:
                    for i in range(start_y, -1, -1):
                        if self.text[i].size() == 0:
                            continue
                        index = self.text[i].find(input_data)
                        if index >= 0:
                            x = index
                            y = i
                            break
            return [x, y]
        except RuntimeError:
            return [start_x, start_y]
        except IndexError:
            return [start_x, start_y]

    def copy_string(self, line_num: int) -> bool:
        try:
            self.buffer.clear()
            self.buffer = mystring.MyString(self.text[line_num])
            self.buffer_state = True
            return True
        except IndexError:
            return False

    def copy_word(self, sym_num: int, line_num: int) -> bool:
        try:
            if self.text[line_num] == "":
                return False
            begin_index = sym_num
            end_index = sym_num
            if self.text[line_num][begin_index] == ' ':
                self.buffer.clear()
                self.buffer = mystring.MyString(" ")
                return True
            while begin_index != 0 and self.text[line_num][begin_index] != ' ':
                begin_index -= 1
            if self.text[line_num][begin_index] == ' ':
                begin_index += 1
            while end_index < self.text[line_num].size() and self.text[line_num][end_index] != ' ':
                end_index += 1
            self.buffer.clear()
            for i in range(begin_index, end_index):
                self.buffer += self.text[line_num][i]
            self.buffer_state = False
            return True
        except IndexError:
            return False

    def paste_new_string(self, line_num: int) -> bool:
        try:
            self.text.insert(line_num + 1, mystring.MyString(self.buffer))
            return True
        except IndexError:
            return False

    def paste_in_string(self, sym_num: int, line_num: int) -> bool:
        try:
            self.text[line_num].insert(sym_num, str(self.buffer))
            return True
        except IndexError:
            return False

    def delete_sym(self, sym_num: int, line_num: int) -> bool:
        try:
            if self.text[line_num].size() > sym_num >= 0:
                self.text[line_num].erase(sym_num, 1)
            return True
        except IndexError:
            return False

    def delete_word(self, sym_num: int, line_num: int) -> bool:
        try:
            if self.text[line_num] == "":
                return False
            begin_index = sym_num
            end_index = sym_num
            if self.text[line_num][begin_index] == ' ':
                self.text[line_num].erase(begin_index, 1)
                return True
            while begin_index != 0 and self.text[line_num][begin_index] != ' ':
                begin_index -= 1
            if self.text[line_num][begin_index] == ' ':
                begin_index += 1
            while end_index < self.text[line_num].size() and self.text[line_num][end_index] != ' ':
                end_index += 1
            if end_index < self.text[line_num].size() and self.text[line_num][end_index] == ' ':
                end_index += 1
            self.text[line_num].erase(begin_index, end_index - begin_index)
            return True
        except IndexError:
            return False

    def delete_str(self, line_num: int) -> bool:
        try:
            self.text.pop(line_num)
            return True
        except IndexError:
            return False

    def input(self, sym_num: int, line_num: int, input_data: str) -> bool:
        try:
            self.text[line_num].insert(sym_num, input_data[0])
            return True
        except IndexError:
            return False

    def new_string(self, sym_num: int, line_num: int) -> bool:
        try:
            self.text.insert(line_num + 1, mystring.MyString(""))
            for i in range(sym_num, self.text[line_num].size()):
                self.text[line_num + 1].append(str(self.text[line_num][i]))
            self.text[line_num].erase(sym_num, self.text[line_num].size() - sym_num)
            return True
        except IndexError:
            return False

    def replace_sym(self, sym_num: int, line_num: int, input_data: str) -> bool:
        try:
            self.text[line_num].erase(sym_num, 1)
            self.text[line_num].insert(sym_num, input_data[0])
            return True
        except IndexError:
            return False

    def go_to_previous(self, line_num: int) -> bool:
        try:
            for i in range(self.text[line_num].size()):
                self.text[line_num - 1].append(str(self.text[line_num][i]))
            return True
        except IndexError:
            return False
