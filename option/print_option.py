from option.walking_option import WalkingOption

class PrintOption(WalkingOption):
    def __init__(self, verbose: bool = False, quiet: bool = False, recursive: bool = False, jobs: int = 1, excluded: list = None, included: list = None):
        super().__init__(verbose, quiet, recursive, jobs, excluded, included)
        self._output_file: str = None
        self._indent: int = 1
        self._header: bool = True

    def __str__(self):
        return super().__str__() + f"\n output_file:{self.output_file}\n indent:{self.indent}\n header:{self.header}"

    @property
    def output_file(self) -> str:
        return self._output_file
    @output_file.setter
    def output_file(self, value: str) -> None:
        self._output_file = value

    @property
    def indent(self) -> int:
        return self._indent
    @indent.setter
    def indent(self, value: int) -> None:
        self._indent = value

    @property
    def header(self) -> bool:
        return self._header
    @header.setter
    def header(self, value: bool) -> None:
        self._header = value