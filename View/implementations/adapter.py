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
        """
        # TODO: начинаю разрабатывать приём апдейтов, чтобы не загружать сразу всё
        # TODO: добавить загрузку из файла (отдельную), где просто будет загружаться весь текст
        # TODO: проверить ресайз и сделать где-то там (мб в другом методе, но рядом) сдвиг по курсору нормальный

        pass

    def update_cursor(self, new_pos: list[int]) -> None:
        pass

    def load_text(self, text: list[str]):
        pass

    def change_page(self, direction: bool) -> None:
        pass

    def read_char(self) -> str:
        pass

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

    def update_handler(self) -> None:
        self.status_bar.strings[0] = str(self.editor.cursor_pos[1] + 1)
        self.status_bar.strings[1] = str(len(self.editor.curr_text))
        not_overflow = self.resize_statusbar()
        self.resize_editor()
        self.window.screen.refresh()
        if not_overflow:
            self.update_statusbar()
        self.update_editor()
        self.window.editor_panel.window().move(self.editor.cursor_on_screen[1], self.editor.cursor_on_screen[0])

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

    def resize_editor(self):
        self.window.editor_panel.window().clear()
        height, width = self.window.screen.getmaxyx()
        height -= self.status_bar.height
        self.window.editor_panel.window().resize(height, width)
        self.window.editor_panel.show()
        self.window.editor_panel.window().refresh()

    def update_statusbar(self):
        height, width = self.window.status_bar_panel.window().getmaxyx()
        str_1 = f"| MODE: {self.status_bar.mode} | FILE: {self.status_bar.file} | {self.status_bar.command}"
        str_2 = f" | {self.status_bar.strings[0]}/{self.status_bar.strings[1]} |"
        addition = height * width - (len(str_1) + len(str_2))
        string = str_1 + (" " * addition) + str_2
        for i in range(self.status_bar.height):
            self.window.status_bar_panel.window().addstr(i, 0, string[(width*i):(width*(i+1)-1)])
        self.window.status_bar_panel.show()
        self.window.status_bar_panel.window().refresh()

    def update_editor(self):
        height, width = self.window.editor_panel.window().getmaxyx()
        y = 0
        for i in range(self.editor.screen_borders_yx[0][0], self.editor.screen_borders_yx[1][0] + 1):
            part_start = self.editor.screen_borders_yx[0][1] \
                if i == self.editor.screen_borders_yx[0][0] else 0
            line = self.editor.curr_text[i]
            part_end = self.editor.screen_borders_yx[1][1] \
                if i == self.editor.screen_borders_yx[1][0] else len(line) // width
            for j in range(part_start, part_end + 1):
                out_line = line[j * width:(j + 1) * width]
                self.window.editor_panel.window().addstr(y, 0, out_line)
                y += 1
        self.window.editor_panel.show()
        self.window.editor_panel.window().refresh()


class Window:
    def __init__(self):
        self.screen = curses.initscr()
        self.editor_panel = None
        self.status_bar_panel = None
        self.init_screen()

    def __del__(self):
        curses.endwin()

    def init_screen(self):
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
        self.editor_panel.window().move(1, 0)


class Editor:
    def __init__(self):
        self.curr_text = [""]
        self.cursor_pos = [0, 0]
        self.screen_borders_yx = [[0, 0], [0, 0]]
        self.cursor_on_screen = [0, 0]


class StatusBar:
    def __init__(self):
        self.mode = "Navigation&Edit"
        self.file = "no file"
        self.command = ""
        self.strings = ["1", "0"]
        self.height = 3
