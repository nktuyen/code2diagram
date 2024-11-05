from model.code_model import CodeModel, ProgrammingLanguageType

class CppCodeModel(CodeModel):
    def __init__(self, name = '', parent: CodeModel = None):
        super().__init__(ProgrammingLanguageType.CPP, name, parent)
    

    @property
    def parent(self) -> CodeModel:
        return self._parent
    @parent.setter
    def parent(self, value: CodeModel):
        self._parent = value