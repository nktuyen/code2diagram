from model.file_model import FileModel
from model.directory_model import DirectoryModel
from model.code_model import CodeModel

class CodeFileModel(FileModel):
    def __init__(self, name: str = '', parent: DirectoryModel = None):
        super().__init__(name, parent)
        self._code_model: CodeModel = None

    
    @property
    def code_model(self) -> CodeModel:
        return self._code_model
    @code_model.setter
    def code_model(self, value: CodeModel):
        self._code_model = value