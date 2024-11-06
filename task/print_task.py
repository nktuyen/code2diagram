"""Imports"""
#System imports
import os
#Project imports
from task.walking_task import WalkingTask
from option.print_option import PrintOption
from model.directory_model import DirectoryModel
from model.io_model import IoModel, IoType

class PrintTask(WalkingTask):
    def __init__(self, name: str = '', desc: str = '') -> None:
        super().__init__(name, desc, PrintOption())
        self._directory: DirectoryModel = None

    @property
    def option(self) -> PrintOption:
        return self._option
    
    @property
    def directory(self) -> DirectoryModel:
        return self._directory

    def _pre_run(self, args = None) -> bool:
        if not super()._pre_run(args):
            return False
        return True

    def __print_dir(self, directory: DirectoryModel, row_count: int = 0) -> int:
        row_count += 1
        print("  "*directory.depth + directory.base_name + f"({directory.size})")
        child: IoModel = None
        for child in directory.children:
            row_count += 1
            if child.kind == IoType.FILE or child.kind == IoType.LINK:
                print("  " * child.depth +  child.base_name + f"({child.size})")
            elif child.kind == IoType.DIR:
                row_count += self.__print_dir(child, row_count)
        return row_count

    def _on_run(self, args = None) -> bool:
        if not super()._on_run(args):
            return False
        row_count: int = 0
        try:
            row_count = self.__print_dir(self.directory, row_count)
        except Exception as e:
            print(f"[E]{e}")
            return False
        return True