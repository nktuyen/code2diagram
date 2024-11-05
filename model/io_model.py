#System imports
import os
from enum import IntEnum
#Project imports
from model.base_model import BaseModel

class IoType(IntEnum):
    UNKNOWN = 0
    FILE = 1
    LINK = 2
    DIR = 3

class IoModel(BaseModel):
    def __init__(self, kind: IoType, name: str = '', parent = None, stat = None):
        super().__init__(name, parent)
        self._kind: IoType = kind
        self._size: int = 0
        self._depth: int = 0
        self._stat = stat
        self._base_name: str = ""
        self._relative_name: str = ""

    @property
    def base_name(self) -> str:
        return os.path.basename(self.name)

    @property
    def relative_name(self) -> str:
        return self._relative_name
    @relative_name.setter
    def relative_name(self, value: str):
        self._relative_name = value
    
    @property
    def kind(self):
        return self._kind
    
    @property
    def parent(self) -> BaseModel:
        return self._parent
    @parent.setter
    def parent(self, value: BaseModel):
        self._parent = value
    
    @property
    def size(self) -> int:
        return self.stat.st_size
    
    @property
    def depth(self) -> int:
        return self._depth
    @depth.setter
    def depth(self, value: int):
        self._depth = value

    @property
    def stat(self) -> int:
        if self._stat is None:
            self._stat = os.stat(self.name)
        return self._stat