from model.io_model import IoType, IoModel
from model.directory_model import DirectoryModel

class SymLinkModel(IoModel):
    def __init__(self, name: str = '', parent: IoModel = None):
        super().__init__(IoType.LINK, name, parent)

    
    @property
    def parent(self) -> DirectoryModel:
        return self._parent
    @parent.setter
    def parent(self, value: DirectoryModel):
        self._parent = value