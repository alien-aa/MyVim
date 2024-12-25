import curses
import curses.panel

from View.abstractions.idisplay import IDisplay
from View.abstractions.iinteractor import IInteractor


class Adapter(IDisplay, IInteractor):
    def __init__(self):
        self.window = Window()
        self.status_bar = StatusBar()
        self.editor = Editor()

    def filename(self, message: str) -> None:
        self.status_bar.file = message
        self.update_handler()

    def update_text(self, line_num: int, text: str, changes_type: int) -> None:
        """
        changes type:
        1 - replace old_text[line_num] -> text
        2 - insert text to line_num position
        3 - delete old_text[line_num]
        """
        match changes_type:
            case 1:
                self.editor.curr_text[line_num] = text
                self.editor.screen_borders[0] = 0
                self.editor.screen_borders[1] = len(self.editor.curr_text)
                self.update_handler()
            case 2:
                self.editor.curr_text.insert(line_num, text)
                self.editor.screen_borders[1] = len(self.editor.curr_text)
                self.update_handler()
            case 3:
                self.editor.curr_text.pop(line_num)
                self.editor.screen_borders[1] = len(self.editor.curr_text)
                self.update_handler()
            case _:
                return

    def update_cursor(self, new_pos: list[int]) -> None:
        self.editor.cursor_pos = new_pos
        self.update_handler()

    def load_text(self, text: list[str]) -> None:
        self.editor.curr_text = text
        self.editor.cursor_pos = [0, 0]
        self.editor.screen_borders = [0, 0]
        self.editor.cursor_on_screen = [0, 0]
        self.update_handler()

    def change_page(self, direction: bool) -> None:
        """
        direction:
        False UP
        True DOWN
        """
        height, width = self.window.screen.getmaxyx()
        if direction:
            self.editor.screen_borders[0] = min(len(self.editor.curr_text) - 1, self.editor.screen_borders[0] + height)
            self.editor.screen_borders[1] = min(len(self.editor.curr_text), self.editor.screen_borders[1] + height)
            self.editor.cursor_pos[1] = self.editor.screen_borders[0]
            self.editor.cursor_pos[0] = min(self.editor.cursor_pos[0], len(self.editor.curr_text[self.editor.cursor_pos[1]]))
            self.update_handler()
        else:
            self.editor.screen_borders[0] = max(0, self.editor.screen_borders[0] - height)
            self.editor.screen_borders[1] = max(1, self.editor.screen_borders[1] - height)
            self.editor.cursor_pos[1] = self.editor.screen_borders[0]
            self.editor.cursor_pos[0] = min(self.editor.cursor_pos[0], len(self.editor.curr_text[self.editor.cursor_pos[1]]))
            self.update_handler()

    def read_char(self) -> str:
        char_code = self.window.editor_panel.window().getkey()
        if char_code == "\b":
            char_code = "BACKSPACE"
        elif char_code == "\x1b":
            return "ESCAPE"
        elif char_code == "\n":
            return "ENTER"
        self.update_handler()
        return char_code

    def state(self, message: str) -> None:
        self.status_bar.mode = message
        self.update_handler()

    def read_cmd(self) -> str:
        char_code = self.window.status_bar_panel.window().getkey()
        if char_code == "\b" and len(self.status_bar.command) > 1:
            self.status_bar.command = self.status_bar.command[:-1]
            char_code = "BACKSPACE"
        elif char_code == "\b" and len(self.status_bar.command) <= 1 and self.status_bar.mode != "Command":
            self.status_bar.command = self.status_bar.command[:-1]
            char_code = "BACKSPACE"
        elif char_code == "\b" and len(self.status_bar.command) <= 1 and self.status_bar.mode == "Command":
            char_code = ""
        elif char_code == "\x1b":
            self.status_bar.command = ""
            return "ESCAPE"
        elif any(char_code == item for item in ("KEY_DOWN", "KEY_UP", "KEY_RIGHT", "KEY_LEFT", "KEY_A3", "KEY_C3")):
            return char_code
        elif char_code == "\n":
            return "ENTER"
        elif len(char_code) == 1 and char_code != "\b":
            self.status_bar.command += char_code
        self.update_handler()
        return char_code

    def clear_cmd(self, new_cmd: str) -> None:
        self.status_bar.command = new_cmd
        self.update_handler()

    def get_cursor(self) -> list[int]:
        return self.editor.cursor_pos

    def update_handler(self) -> None:
        self.status_bar.strings[0] = str(self.editor.cursor_pos[1] + 1)
        self.status_bar.strings[1] = str(len(self.editor.curr_text))
        not_overflow = self.resize_statusbar()
        self.resize_editor()
        self.window.screen.refresh()
        if not_overflow:
            self.update_statusbar()
        self.update_editor()

    def resize_statusbar(self) -> bool:
        self.window.status_bar_panel.window().clear()
        height, width = self.window.screen.getmaxyx()
        str_1 = f"| MODE: {self.status_bar.mode} | FILE: {self.status_bar.file} | {self.status_bar.command} "
        str_2 = f"| {self.status_bar.strings[0]}/{self.status_bar.strings[1]} |"
        total_length = len(str_1) + len(str_2)
        if total_length >= width * (height - 1):
            self.window.status_bar_panel.replace(curses.newwin(height - 1, width, 1, 0))
            self.window.status_bar_panel.window().bkgd(' ', curses.color_pair(2))
            self.window.status_bar_panel.window().keypad(True)
            self.window.status_bar_panel.window().leaveok(True)
            curses.curs_set(1)
            self.window.status_bar_panel.show()
            self.window.status_bar_panel.window().refresh()
            return False
        else:
            self.status_bar.height = (total_length // width) + 1
            self.window.status_bar_panel.replace(curses.newwin(self.status_bar.height, width, height - self.status_bar.height, 0))
            self.window.status_bar_panel.window().bkgd(' ', curses.color_pair(2))
            self.window.status_bar_panel.window().keypad(True)
            self.window.status_bar_panel.window().leaveok(True)
            curses.curs_set(1)
            self.window.status_bar_panel.show()
            self.window.status_bar_panel.window().refresh()
            return True

    def resize_editor(self) -> None:
        self.window.editor_panel.window().clear()
        height, width = self.window.screen.getmaxyx()
        height -= self.status_bar.height
        self.window.editor_panel.window().resize(height, width)
        self.window.editor_panel.show()
        self.window.editor_panel.window().refresh()

    def update_statusbar(self) -> None:
        height, width = self.window.status_bar_panel.window().getmaxyx()
        str_1 = f"| MODE: {self.status_bar.mode} | FILE: {self.status_bar.file} | {self.status_bar.command}"
        str_2 = f" | {self.status_bar.strings[0]}/{self.status_bar.strings[1]} |"
        addition = height * width - (len(str_1) + len(str_2))
        string = str_1 + (" " * addition) + str_2
        for i in range(self.status_bar.height):
            self.window.status_bar_panel.window().addstr(i, 0, string[(width*i):(width*(i+1)-1)])
        self.window.status_bar_panel.show()
        self.window.status_bar_panel.window().refresh()

    def update_editor(self) -> None:
        height, width = self.window.screen.getmaxyx()
        height -= self.status_bar.height
        on_screen = []
        self.editor.cursor_on_screen = [0, 0]
        cursor_flag = False
        self.editor.screen_borders[0] = min(self.editor.screen_borders[0], self.editor.cursor_pos[1]) # чтобы двигалось вверх при перемещении курсора вверх
        self.editor.screen_borders[1] = max(self.editor.screen_borders[1], self.editor.cursor_pos[1] + 1)
        if self.editor.screen_borders[1] - self.editor.screen_borders[0] >= height:
            if self.editor.screen_borders[1] - self.editor.cursor_pos[1] < height:
                self.editor.screen_borders[0] = self.editor.screen_borders[1] - height
            elif self.editor.cursor_pos[1] - self.editor.screen_borders[0] < height:
                self.editor.screen_borders[1] = self.editor.screen_borders[0] + height

        for i in range(self.editor.screen_borders[0], self.editor.screen_borders[1]):
            if len(on_screen) > height and cursor_flag:
                self.editor.screen_borders[1] = i
                break
            elif len(on_screen) > height:
                if self.editor.cursor_on_screen[1] <= len(on_screen) - height:
                    while len(on_screen) >= height:
                        on_screen.pop(-1)
                else:
                    while len(on_screen) >= height:
                        on_screen.pop(0)
                        self.editor.cursor_on_screen[1] -= 1

            line = self.editor.curr_text[i]
            max_parts = len(line) // (width - 1) + 1
            for j in range(max_parts):
                part = line[j * (width - 1):(j + 1) * (width - 1)]
                on_screen.append(part)
                if i < self.editor.cursor_pos[1]:
                    self.editor.cursor_on_screen[1] += 1
                elif i == self.editor.cursor_pos[1] and (j * (width - 1) <= self.editor.cursor_pos[0] < (j + 1) * (width - 1)):
                    self.editor.cursor_on_screen[0] = self.editor.cursor_pos[0] % (width - 1)
                    cursor_flag = True

        if len(on_screen) < height:
            for i in range(self.editor.screen_borders[1], len(self.editor.curr_text)):
                if len(on_screen) >= height and cursor_flag:
                    self.editor.screen_borders[1] = i + 1
                    break
                elif len(on_screen) >= height:
                    if self.editor.cursor_on_screen[1] <= len(on_screen) - height:
                        while len(on_screen) >= height:
                            on_screen.pop(-1)
                    else:
                        while len(on_screen) >= height:
                            on_screen.pop(0)
                            self.editor.cursor_on_screen[1] -= 1

                line = self.editor.curr_text[i]
                max_parts = len(line) // (width - 1) + 1
                for j in range(max_parts):
                    part = line[j * (width - 1):(j + 1) * (width - 1)]
                    on_screen.append(part)
                    if i < self.editor.cursor_pos[1]:
                        self.editor.cursor_on_screen[1] += 1
                    elif i == self.editor.cursor_pos[1] and (
                            j * (width - 1) <= self.editor.cursor_pos[0] < (j + 1) * (width - 1)):
                        self.editor.cursor_on_screen[0] = self.editor.cursor_pos[0] % (width - 1)
                        cursor_flag = True

        while len(on_screen) > height:
            if self.editor.cursor_on_screen[1] <= len(on_screen) - height:
                on_screen.pop(-1)
            else:
                on_screen.pop(0)
                self.editor.cursor_on_screen[1] -= 1
        y = 0
        for item in on_screen:
            self.window.editor_panel.window().addstr(y, 0, item)
            y += 1
        self.window.editor_panel.show()
        self.window.editor_panel.window().refresh()
        self.window.editor_panel.window().leaveok(True)
        self.window.status_bar_panel.window().leaveok(True)
        self.window.screen.leaveok(True)
        curses.curs_set(1)
        curses.setsyx(self.editor.cursor_on_screen[1], self.editor.cursor_on_screen[0])


class Window:
    def __init__(self):
        self.screen = curses.initscr()
        self.editor_panel = None
        self.status_bar_panel = None
        self.init_screen()

    def __del__(self):
        curses.endwin()

    def init_screen(self) -> None:
        curses.noecho()
        curses.start_color()
        self.screen.leaveok(True)
        curses.curs_set(1)

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        height, width = self.screen.getmaxyx()

        editor_win = curses.newwin(height - 1, width, 0, 0)
        editor_win.bkgd(' ', curses.color_pair(1))
        editor_win.keypad(True)
        editor_win.leaveok(True)
        curses.curs_set(1)

        status_bar_win = curses.newwin(1, width, height - 1, 0)
        status_bar_win.bkgd(' ', curses.color_pair(2))
        status_bar_win.keypad(True)
        status_bar_win.leaveok(True)
        curses.curs_set(1)

        self.editor_panel = curses.panel.new_panel(editor_win)
        self.status_bar_panel = curses.panel.new_panel(status_bar_win)

        self.screen.refresh()
        self.editor_panel.show()
        self.editor_panel.window().refresh()
        self.status_bar_panel.show()
        self.status_bar_panel.window().refresh()
        curses.setsyx(0, 0)


class Editor:
    def __init__(self):
        self.curr_text = [""]
        self.cursor_pos = [0, 0]
        self.screen_borders = [0, 0]
        self.cursor_on_screen = [0, 0]


class StatusBar:
    def __init__(self):
        self.mode = "Navigation&Edit"
        self.file = "no file"
        self.command = ""
        self.strings = ["1", "0"]
        self.height = 1
