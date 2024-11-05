import os
import re
import fnmatch
import concurrent.futures

from task.base_task import BaseTask
from option.parsing_option import ParsingOption

class ParsingTask(BaseTask):
    def __init__(self, name: str = '', desc: str = '') -> None:
        super().__init__(name, desc, ParsingOption())
        self._root_dir: str = ""
    
    @property
    def option(self) -> ParsingOption:
        return self._option
    
    @property
    def root_dir(self) -> str:
        return self._root_dir
    
    def __walk_dir(self, dir_path: str):
        path_list: list = os.listdir(dir_path)
        full_path: str = ""
        relative_path: str = ""
        ignored_flag: bool = False
        pattern: str = ""
        for child_path in path_list:
            if child_path in [".", ".."]:
                continue
            full_path = os.path.join(dir_path, child_path)
            relative_path = full_path[len(self._root_dir):]
            if relative_path.startswith(os.sep):
                relative_path = relative_path[len(os.sep):]
            ignored_flag = False #Reset filter result
            #Filter excluded
            if len(self.option.excluded_patterns) > 0:
                for pattern in self.option.excluded_patterns:
                    if fnmatch.fnmatch(relative_path, pattern):
                        if not self.option.quiet and self.option.verbose:
                            print(f"{relative_path} -> Ignored (matched {pattern})")
                        ignored_flag = True
                        break
            if ignored_flag:
                continue
            if os.path.isfile(full_path):
                #Filter included
                if len(self.option.included_patterns) > 0:
                    ignored_flag = True #Initial set ignore flag to True. set to False if child_path is matched included patterns 
                    for pattern in self.option.included_patterns:
                        if pattern == "*":
                            ignored_flag = False
                            break
                        if fnmatch.fnmatch(relative_path, pattern):
                            if not self.option.quiet and self.option.verbose:
                                print(f"{relative_path} -> Included (matched {pattern})")
                            ignored_flag = False
                            break
                if ignored_flag:
                    continue
                if not self.option.quiet and self.option.verbose:
                    print(f"{relative_path} -> To be parsed (is file)")
            elif os.path.islink(full_path):
                if not self.option.quiet and self.option.verbose:
                    print(f"{relative_path} -> Ignored (is link)")
            elif os.path.isdir(full_path):
                if self.option.recursive:
                    if not self.option.quiet and self.option.verbose:
                        print(f"{relative_path} -> To be recursively parsed (is directory and recursive option is specified)")
                    self.__walk_dir(full_path)
                else:
                    if not self.option.quiet and self.option.verbose:
                        print(f"{relative_path} -> Ignored (is directory but recursive option is not specified)")

    
    def _pre_run(self, args: list) -> bool:
        if not super()._pre_run(args):
            return False
        if len(args) <= 0:
            if not self.option.quiet:
                print("Erro:No any directory specified")
            return False
        specified_directory: str = str(args[0])
        if not os.path.isdir(specified_directory):
            if not self.option.quiet:
                print(f"Error:{specified_directory} is not a valid directory")
            return False
        self._root_dir = specified_directory
        
        return True

    def _on_run(self, args: list = None) -> bool:
        self.__walk_dir(self.root_dir)
        return True