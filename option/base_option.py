class BaseOption:
    def __init__(self, verbose: bool = False, quiet: bool = False) -> None:
        self._verbose: bool = verbose
        self._quiet: bool = quiet
        self._debug: bool = True

    def __str__(self) -> str:
        return f"verbose:{self.verbose}\nquiet:{self.quiet}\ndebug:{self.debug}"

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

    @property
    def debug(self) -> bool:
        return bool(self._debug)
    @debug.setter
    def debug(self, val: bool):
        self._debug = val