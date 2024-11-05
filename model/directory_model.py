from model.io_model import IoType, IoModel

class DirectoryModel(IoModel):
    def __init__(self, name: str = '', parent: IoModel = None):
        super().__init__(IoType.DIR, name, parent)


    @property
    def parent(self) -> IoModel:
        return self._parent
    @parent.setter
    def parent(self, value: IoModel):
        self._parent = value

    @property
    def size(self) -> int:
        return self._size
    @size.setter
    def size(self, value: int):
        self._size = value