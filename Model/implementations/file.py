import Model.MyString.mystring as mystring

from Model.abstractions.ifile import IModelFile

from Model.abstractions.itext import IModelText


class ModelFile(IModelFile):
    def __init__(self,
                 text: IModelText,
                 name: str | None):
        super().__init__(text, name)


    def open_file(self, name: str) -> None:
        try:
            with open(name, 'r') as f:
                self.name = name
                self.changed = False
                self.text.text.clear()
                for line in f:
                    if line[-1] == '\n' and len(line) > 1:
                        line = line[:-1]
                    elif line[-1] == '\n' and len(line) == 1:
                        line = ""
                    self.text.text.append(mystring.MyString(line))
        except FileNotFoundError:
            pass


    def write_file(self, name: str) -> None:
        try:
            with open(name, 'w') as f:
                self.name = name
                self.changed = False
                for l in self.text.text:
                    f.write(str(l) + "\n")
        except FileNotFoundError:
            pass

    def open_help(self, name: str) -> None:
        try:
            with open(name, 'r') as f:
                self.text.text.clear()
                for line in f:
                    if line[-1] == '\n' and len(line) > 1:
                        line = line[:-1]
                    elif line[-1] == '\n' and len(line) == 1:
                        line = ""
                    self.text.text.append(mystring.MyString(line))
        except FileNotFoundError:
            pass
