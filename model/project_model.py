from model.directory_model import DirectoryModel

class ProjectModel(DirectoryModel):
    def __init__(self, name: str = ''):
        super().__init__(name)