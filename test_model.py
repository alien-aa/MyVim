import pytest
from unittest.mock import MagicMock

from Model.implementations.model import Model
from Model.implementations.text import ModelText
from Model.implementations.subject import ModelSubject
from Model.implementations.cursor import ModelCursor
from Model.implementations.file import ModelFile
from Model.abstractions.observer import Observer
import Model.MyString.mystring as mystring


class MockView(Observer):
    def __init__(self):
        self.update = MagicMock()

    def update(self, message: dict) -> None:
        pass

@pytest.fixture
def setup_model():
    subject = ModelSubject()
    mock_view = MockView()
    subject.add_observer(mock_view)


    text = ModelText()
    text.text = [mystring.MyString('abc'), mystring.MyString('def'), mystring.MyString('ghi')]
    help_text = ModelText()  # Пустой текст помощи
    help_file = ModelFile(help_text, "help")

    model = Model(
        ModelFile(text, ""),
        ModelCursor(),
        text,
        subject,
        help_file,
        ModelCursor(),
        help_text
    )

    return model, subject, mock_view

def test_move_cursor(setup_model):
    model, subject, mock_view = setup_model

    model.move_cursor(1, 1, 2)

    assert mock_view.update.called
    assert mock_view.update.call_args[0][0] == {"action": "move_cursor", "new_pos": [0, 2]}

def test_change_pos(setup_model):
    model, subject, mock_view = setup_model

    model.change_pos(-1)

    assert mock_view.update.called
    assert mock_view.update.call_args[0][0] == {"action": "change_pos", "new_pos": -1}

def test_search(setup_model):
    model, subject, mock_view = setup_model

    model.search("g", 1)

    assert mock_view.update.called
    assert mock_view.update.call_args[0][0] == {"action": "move_cursor", "new_pos": [0, 2]}

def test_files_action_open(setup_model):
    model, subject, mock_view = setup_model

    model.files_action('test.txt', 1)

    assert mock_view.update.called
    assert mock_view.update.call_args[0][0] == {"action": "file",
                                                "filename": 'test.txt',
                                                "text": ['abc', 'def', 'ghi']}

def test_files_action_write(setup_model):
    model, subject, mock_view = setup_model

    model.files_action('test.txt', 2)

    assert mock_view.update.called
    assert mock_view.update.call_args[0][0] == {"action": "write", "filename": 'test.txt'}

def test_post_input(setup_model):
    model, subject, mock_view = setup_model

    model.post_input('a', 1)

    assert mock_view.update.call_count == 2

    assert mock_view.update.call_args_list[0][0][0] == {"action": "post",
                                                        "string_num": 0,
                                                        "string_value": 'aabc',
                                                        "new_string": False}
    assert mock_view.update.call_args_list[1][0][0] == {"action": "move_cursor", "new_pos": [1, 0]}


def test_delete_character(setup_model):
    model, subject, mock_view = setup_model
    model.cursor.x_pos = 1

    model.delete(1)

    assert mock_view.update.call_count == 2

    assert mock_view.update.call_args_list[0][0][0] == {"action": "delete",
                                                   "string_num": 0,
                                                   "string_value": 'ac'}
    assert mock_view.update.call_args_list[1][0][0] == {"action": "move_cursor",
                                                        "new_pos": [1, 0]}

def test_help_state(setup_model):
    model, subject, mock_view = setup_model

    assert model.help_state() is False
