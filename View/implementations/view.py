from View.abstractions.observer import Observer

from View.abstractions.idisplay import IDisplay


class View(Observer):
    def __init__(self, display: IDisplay):
        self.display = display

    def update(self, message: dict) -> None:
        if message["action"] == "move_cursor":
            self.display.update_cursor(message["new_pos"])
        elif message["action"] == "change_pos":
            self.display.change_page(message["new_pos"] == 1)
        elif message["action"] == "file":
            self.display.filename(message["filename"])
            self.display.load_text(message["text"])
        elif message["action"] == "no file":
            self.display.filename(message["no file"])
            self.display.load_text([""])
        elif message["action"] == "write":
            self.display.filename(message["filename"])
        elif message["action"] == "post":
            ch_type = 2 if message["new_string"] else 1
            self.display.update_text(line_num=message["string_num"], text=message["string_value"], changes_type=ch_type)
        elif message["action"] == "paste_new":
            self.display.update_text(line_num=message["string_num"], text=message["string_value"], changes_type=2)
        elif message["action"] == "paste_in":
            self.display.update_text(line_num=message["string_num"], text=message["string_value"], changes_type=1)
        elif message["action"] == "delete":
            self.display.update_text(line_num=message["string_num"], text=message["string_value"], changes_type=1)
        elif message["action"] == "delete_string":
            self.display.update_text(line_num=message["string_num"], text="", changes_type=3)




