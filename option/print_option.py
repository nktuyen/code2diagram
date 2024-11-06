from option.walking_option import WalkingOption

class PrintOption(WalkingOption):
    def __init__(self, verbose: bool = False, quiet: bool = False, recursive: bool = False, jobs: int = 1, excluded: list = None, included: list = None, output_file: str = None):
        super().__init__(verbose, quiet, recursive, jobs, excluded, included)
        self._output_file: str = output_file


    def __str__(self):
        return super().__str__() + f"\n output_file:{self.output_file}"

    @property
    def output_file(self) -> str:
        return self._output_file
    @output_file.setter
    def output_file(self, value: str) -> None:
        self._output_file = value