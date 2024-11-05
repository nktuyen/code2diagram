from model.code_file_model import CodeFileModel
from model.cpp.cpp_code_model import CppCodeModel
from model.directory_model import DirectoryModel

class CppCodeFileModel(CodeFileModel):
    def __init__(self, name = '', parent: DirectoryModel = None):
        super().__init__(name, parent)

    
    @property
    def code_model(self) -> CppCodeModel:
        return self._code_model
    @code_model.setter
    def code_model(self, value: CppCodeModel):
        self._code_model = value