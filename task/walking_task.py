#System imports
import os
import re
import fnmatch
import concurrent.futures
#Project import
from model.directory_model import DirectoryModel
from model.file_model import FileModel
from model.symlink_model import SymLinkModel
from task.base_task import BaseTask
from option.walking_option import WalkingOption

S_comma: str = ","
S_semicolon: str = ";"

class WalkingTask(BaseTask):
    def __init__(self, name: str = '', desc: str = '', option: WalkingOption = WalkingOption()) -> None:
        super().__init__(name, desc, option)
        self._directory: DirectoryModel = None
    
    @property
    def option(self) -> WalkingOption:
        return self._option
    
    @property
    def directory(self) -> DirectoryModel:
        return self._directory
    
    def __walk_dir(self, directory: DirectoryModel) -> DirectoryModel:
        path_list: list = os.listdir(directory.name)
        full_path: str = ""
        relative_path: str = ""
        ignored_flag: bool = False
        pattern: str = ""
        for child_path in path_list:
            if child_path in [".", ".."]:
                continue
            full_path = os.path.join(directory.name, child_path)
            relative_path = full_path[len(self.directory.name):]
            if relative_path.startswith(os.sep):
                relative_path = relative_path[len(os.sep):]
            ignored_flag = False #Reset filter result
            #Filter excluded
            if len(self.option.excluded_patterns) > 0:
                for pattern in self.option.excluded_patterns:
                    if fnmatch.fnmatch(relative_path, pattern):
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
                            ignored_flag = False
                            break
                if ignored_flag:
                    continue
                file_model: FileModel =  FileModel(full_path, directory)
                file_model.relative_name = relative_path
                file_model.parent = directory
                file_model.depth = directory.depth + 1
                file_model.parent.size += file_model.size
                file_model = self._on_file(file_model)
                if file_model is not None:
                    directory.children.append(file_model)
            elif os.path.islink(full_path) and self.option.link_files:
                link_model: SymLinkModel = SymLinkModel(full_path, directory)
                link_model.relative_name = relative_path
                link_model.parent = directory
                link_model.depth = directory.depth + 1
                link_model = self._on_symlink(link_model)
                if link_model is not None:
                    directory.children.append(link_model)
            elif os.path.isdir(full_path):
                dir_model: DirectoryModel = DirectoryModel(full_path, directory)
                dir_model.relative_name = relative_path
                dir_model.parent = directory
                dir_model.depth = directory.depth + 1
                dir_model = self._on_directory(dir_model)
                if dir_model is not None:
                    if self.option.recursive:
                        dir_model = self.__walk_dir(dir_model)
                        dir_model.parent.size += dir_model.size
                        directory.children.append(dir_model)
                    else:
                        directory.children.append(dir_model)
        return directory
    
    def _on_directory(self, dir_model: DirectoryModel) -> DirectoryModel:
        return dir_model

    def _on_file(self, file_model: FileModel) -> FileModel:
        return file_model
    
    def _on_symlink(self, link_model: SymLinkModel) -> SymLinkModel:
        return link_model
    
    def _pre_parse_args(self, parser):
        super()._pre_parse_args(parser)
        parser.add_option("-r", "--recursive", action="store_false")
        parser.add_option("-j", "--jobs", default=1)
        parser.add_option("-x", "--exclude", default=None)
        parser.add_option("-i", "--include", default="*")
        parser.add_option("", "--system-files", action="store_false", help="Include system files or not. System files are ignored if not specified")
        parser.add_option("", "--hidden-files", action="store_false", help="Include hidden files or not. Hidden files are ignored if not specified")
        parser.add_option("", "--link-files", action="store_false", help="Include symbol links or not. Symbol links are ignored if not specified")

    def _post_parse_args(self, opts, args) -> bool:
        super()._post_parse_args(opts, args)
        if opts is not None:
            if opts.recursive is not None:
                self.option.recursive = True
            if isinstance(opts.jobs, int):
                self.option.jobs = int(opts.jobs)
            if opts.exclude is not None:
                for string in opts.exclude.split(S_comma):
                    string_list: list = string.split(S_semicolon)
                    for pattern in string_list:
                        self.option.excluded_patterns.append(pattern.strip())
            if opts.include is not None:
                for string in opts.include.split(S_comma):
                    string_list: list = string.split(S_semicolon)
                    for pattern in string_list:
                        self.option.included_patterns.append(pattern.strip())
            if opts.system_files is not None:
                self.option.system_files = True
            if opts.hidden_files is not None:
                self.option.hidden_files = True
            if opts.link_files is not None:
                self.option.link_files = True
        if args is None or len(args) == 0:
            print("[E]No any directory specified")
            return False
        directory: str = str(args[0])
        if not os.path.isdir(directory):
            if not os.path.isdir(os.path.abspath(directory)):
                print(f"[E]{directory} is not a valid directory")
                return False
        self._directory = DirectoryModel(os.path.abspath(directory))
        return True

    def _pre_run(self, args = None) -> bool:
        if not super()._pre_run(args):
            return False
        return True

    def _on_run(self, args = None) -> bool:
        try:
            self._directory = self.__walk_dir(self._directory)
        except Exception as e:
            print(f"[E]{e}")
            return False
        return True