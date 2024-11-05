from option.base_option import BaseOption

class ParsingOption(BaseOption):
    def __init__(self, task = None, verbose: bool = False, quiet: bool = False, recursive: bool = False, jobs: int = 1, excluded: list = None, included: list = None) -> None:
        super().__init__(task, verbose, quiet)
        self._recursive: bool = recursive
        self._jobs: int = jobs
        self._excluded: list = excluded
        self._included: list = included

    def __str__(self) -> str:
        return super().__str__() + f"\nrecursive:{self.recursive}\njobs:{self.jobs}\nexcluded_patterns:{self.excluded_patterns}\nincluded_patterns:{self.included_patterns}"

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