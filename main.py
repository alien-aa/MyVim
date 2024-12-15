from Controller.controller import Controller
from Model.implementations.text import ModelText
from View.implementations.adapter import Adapter
from Model.implementations.model import Model
from Model.implementations.subject import ModelSubject
from Model.implementations.cursor import ModelCursor
from Model.implementations.file import ModelFile
from View.implementations.view import View

subject = ModelSubject()
adapter = Adapter()
subject.add_observer(View(adapter))
text = ModelText()
controller = Controller(Model(ModelFile(text, "None"), ModelCursor(), text, subject),  adapter)
controller.run()
