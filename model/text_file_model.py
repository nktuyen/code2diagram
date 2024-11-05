from model.file_model import FileModel
from model.directory_model import DirectoryModel

class TextFileModel(FileModel):
    def __init__(self, name: str = '', parent: DirectoryModel = None):
        super().__init__(name, parent)
        self._content: str = ""

    
    @property
    def content(self) -> str:
        return self._content
    @content.setter
    def content(self, value: str):
        self._content = value