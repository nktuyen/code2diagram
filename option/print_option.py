from option.walking_option import WalkingOption

class PrintOption(WalkingOption):
    def __init__(self, verbose: bool = False, quiet: bool = False, recursive: bool = False, jobs: int = 1, excluded: list = None, included: list = None, print_to_file: str = None):
        super().__init__(verbose, quiet, recursive, jobs, excluded, included)
        self._print_to_file: str = print_to_file


    def __str__(self):
        return super().__str__() + f"\nprint_to_file:{self.print_to_file}"

    @property
    def print_to_file(self) -> str:
        return self._print_to_file
    @print_to_file.setter
    def print_to_file(self, value: str) -> None:
        self._print_to_file = value