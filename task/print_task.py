"""Imports"""
#System imports
import os
#Project imports
from task.base_task import BaseTask
from option.print_option import PrintOption
from model.directory_model import DirectoryModel
from model.io_model import IoModel, IoType

class PrintTask(BaseTask):
    def __init__(self, name: str = '', desc: str = '') -> None:
        super().__init__(name, desc, PrintOption())
        self._directory: DirectoryModel = None

    @property
    def option(self) -> PrintOption:
        return self._option
    
    @property
    def directory(self) -> DirectoryModel:
        return self._directory

    def _pre_run(self, args: list) -> bool:
        if not super()._pre_run(args):
            return False
        if len(args) <= 0:
            if not self.option.quiet:
                print("[ERROR]No any directory specified")
            return False
        self._directory = args[0]
        if not os.path.isdir(self.directory.name):
            if not self.option.quiet:
                print(f"[ERROR]{self.directory} is not a valid directory")
            return False
        return True


    def __print_dir(self, directory: DirectoryModel):
        print("  "*directory.depth + directory.base_name + f"({directory.size})")
        child: IoModel = None
        for child in directory.children:
            if child.kind == IoType.FILE or child.kind == IoType.LINK:
                print("  " * child.depth +  child.base_name + f"({child.size})")
            elif child.kind == IoType.DIR:
                self.__print_dir(child)

    def _on_run(self, args: list = None) -> bool:
        self.__print_dir(self.directory)
        return True