from option.base_option import BaseOption

class WalkingOption(BaseOption):
    def __init__(self, verbose: bool = False, quiet: bool = False, recursive: bool = False, jobs: int = 1, excluded: list = None, included: list = None, hidden_files: bool = False, system_files: bool = False, link_files: bool = False) -> None:
        super().__init__(verbose, quiet)
        self._recursive: bool = recursive
        self._jobs: int = jobs
        self._excluded: list = excluded
        self._included: list = included
        self._hidden_files: bool = hidden_files
        self._system_files: bool = system_files
        self._link_files: bool = link_files

    def __str__(self) -> str:
        return super().__str__() + f"\n recursive:{self.recursive}\n jobs:{self.jobs}\n excluded_patterns:{self.excluded_patterns}\n included_patterns:{self.included_patterns}\n system_files:{self.system_files}\n hidden_files:{self.hidden_files}\n link_files:{self.link_files}"

    @property
    def recursive(self) -> bool:
        return self._recursive
    @recursive.setter
    def recursive(self, val: bool):
        self._recursive = val

    @property
    def jobs(self) -> int:
        return self._jobs
    @jobs.setter
    def jobs(self, val: int):
        self._jobs = val

    @property
    def excluded_patterns(self) -> list:
        if not isinstance(self._excluded, list):
            self._excluded = []
        return self._excluded
    
    @property
    def included_patterns(self) -> list:
        if not isinstance(self._included, list):
            self._included = []
        return self._included
    
    @property
    def hidden_files(self) -> bool:
        return self._hidden_files
    @hidden_files.setter
    def hidden_files(self, val: bool) -> None:
        self._hidden_files = val
    
    @property
    def system_files(self) -> bool:
        return self._system_files
    @system_files.setter
    def system_files(self, val: bool):
        self._system_files = val
    
    @property
    def link_files(self) -> bool:
        return self._link_files
    @link_files.setter
    def link_files(self, val: bool):
        self._link_files = val