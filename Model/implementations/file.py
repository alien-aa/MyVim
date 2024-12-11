import Model.MyString.mystring as mystring

from Model.abstractions.ifile import IModelFile

from Model.abstractions.itext import IModelText


class ModelFile(IModelFile):
    def __init__(self,
                 text: IModelText,
                 name: str):
        self.text = text
        self.name = name
        self.changed: bool = False


    def open_file(self, name: str) -> None:
        with open(name, 'r') as f:
            self.name = name
            self.changed = False
            self.text.text.clear()
            for line in f:
                self.text.text.append(mystring.MyString(line))


    def write_file(self, name: str) -> None:
        with open(name, 'w') as f:
            self.name = name
            self.changed = False
            f.writelines([str(line) for line in self.text.text])
