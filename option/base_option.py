class BaseOption:
    def __init__(self, task = None, verbose: bool = False, quiet: bool = False) -> None:
        self._task = task
        self._verbose: bool = verbose
        self._quiet: bool = quiet

    def __str__(self) -> str:
        return f"verbose:{self.verbose}\nquiet:{self.quiet}"

    @property
    def task(self):
        return self._task

    @property
    def verbose(self) -> bool:
        return self._verbose
    @verbose.setter
    def verbose(self, val: bool):
        self._verbose = val
    
    @property
    def quiet(self) -> bool:
        return self._quiet
    @quiet.setter
    def quiet(self, val: bool):
        self._quiet = val