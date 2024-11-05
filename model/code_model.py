#Systen imports
from enum import IntEnum
#Project imports
from model.base_model import BaseModel

class ProgrammingLanguageType(IntEnum):
    UNKNOWN = 0
    C = 1
    CPP = 2
    CS = 3
    JAVA = 4
    PYTHON = 5
    VB = 6


class CodeModel(BaseModel):
    def __init__(self,language: ProgrammingLanguageType, name: str = '', parent: BaseModel = None):
        super().__init__(name, parent)
        self._language: ProgrammingLanguageType = language


    @property
    def language(self):
        return self._language