from zzz.controllers.controller import Controller
from zzz.curses_adapter.adapter import Adapter
from zzz.models.model import Model
from zzz.models.subject import ModelSubject
from zzz.models.cursor import ModelCursor
from zzz.models.file import ModelFile
from zzz.views.view import View

subject = ModelSubject()
adapter = Adapter()
subject.add_observer(View(adapter))
controller = Controller(Model(ModelFile(),ModelCursor(), subject),  adapter)
controller.run()
