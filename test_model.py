import pytest
from unittest.mock import MagicMock
from Model.implementations.model import Model

# Заглушки для интерфейсов
class MockFile:
    def __init__(self):
        self.name = None
        self.changed = False

    def open_file(self, name):
        self.name = name

    def write_file(self, name):
        self.name = name

class MockCursor:
    def __init__(self):
        self.x_pos = 0
        self.y_pos = 0

    def move_cursor(self, x, y):
        self.x_pos = x
        self.y_pos = y

class MockText:
    def __init__(self):
        self.text = ["Hello World", "This is a test"]
        self.buffer_state = False

    def input(self, x, y, char):
        self.text[y] = self.text[y][:x] + char + self.text[y][x:]

    def search(self, input_data, direction, x, y):
        for i in range(y, len(self.text)):
            if input_data in self.text[i]:
                return self.text[i].index(input_data), i
        return -1, -1

    def delete_sym(self, x, y):
        self.text[y] = self.text[y][:x] + self.text[y][x + 1:]

    def copy_string(self, y):
        return self.text[y]

    def paste_new_string(self, y):
        self.text[y] += " Pasted text"  # Добавляем текст к существующему

    def delete_word(self, x, y):
        self.text[y] = self.text[y].replace("word", "", 1)

    def delete_str(self, y):
        del self.text[y]

    def replace_sym(self, x, y, char):
        self.text[y] = self.text[y][:x] + char + self.text[y][x + 1:]

# Тесты
@pytest.fixture
def model():
    file = MockFile()
    cursor = MockCursor()
    text = MockText()
    subject = MagicMock()  # Используем MagicMock для subject
    return Model(file, cursor, text, subject)

def test_move_cursor(model):
    model.move_cursor(1, 1, 1)  # Move cursor down by 1
    assert model.cursor.y_pos == 1
    assert model.cursor.x_pos == 0

def test_post_input(model):
    model.post_input('X', 1)  # Insert 'X' at cursor position
    assert model.text.text[0] == 'XHello World'

def test_search(model):
    model.cursor.x_pos = 0
    model.cursor.y_pos = 0
    model.search('World', 1)
    assert model.cursor.x_pos == 6
    assert model.cursor.y_pos == 0

def test_delete(model):
    model.cursor.x_pos = 0
    model.cursor.y_pos = 0
    model.delete(1)  # Delete character
    assert model.text.text[0] == 'ello World'

def test_copy(model):
    model.cursor.y_pos = 0
    model.copy(1)  # Copy string
    assert model.text.copy_string(model.cursor.y_pos) == 'Hello World'

def test_paste(model):
    model.cursor.y_pos = 0
    model.copy(1)
    model.text.buffer_state = True
    model.paste()
    assert model.text.text[0] == 'Hello World Pasted text'

def test_files_action_open(model):
    model.files_action('test.txt', 1)
    assert model.file.name == 'test.txt'

def test_change_pos(model):
    model.change_pos(1)
    model.subject.notify.assert_called_with({"action": "change_pos", "new_pos": 1})

# Запустите тесты с помощью команды:
# pytest test_model.py
