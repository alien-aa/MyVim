from Controller.controller import Controller
from Model.implementations.text import ModelText
from View.implementations.adapter import Adapter
from Model.implementations.model import Model
from Model.implementations.subject import ModelSubject
from Model.implementations.cursor import ModelCursor
from Model.implementations.file import ModelFile
from View.implementations.view import View

help_filename = "C:\\Users\\alien_aa\\PycharmProjects\\MyVim\\help.txt"

subject = ModelSubject()
adapter = Adapter()
subject.add_observer(View(adapter))
text = ModelText()
help_text = ModelText()
help_file = ModelFile(help_text, "help")
controller = Controller(Model(ModelFile(text, ""),
                              ModelCursor(),
                              text,
                              subject,
                              help_file,
                              ModelCursor(),
                              help_text),
                        adapter,
                        {"dir": 1, "data": ""})
controller.run(help_filename)
