from model.io_model import IoModel, IoType
from model.code_model import CodeModel
from model.directory_model import DirectoryModel

class FileModel(IoModel):
    def __init__(self, name: str = '', parent: IoModel = None):
        super().__init__(IoType.FILE, name, parent)
        self._code_model: CodeModel = None

    @property
    def parent(self) -> DirectoryModel:
        return self._parent
    @parent.setter
    def parent(self, value: DirectoryModel):
        self._parent = value