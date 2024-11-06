#System imports
import os
import optparse
#Project imports
from option.base_option import BaseOption

class BaseTask:
    def __init__(self, name: str = '', desc: str = '', option: BaseOption = None) -> None:
        self._name: str = name
        self._desc: str = desc
        self._option: BaseOption = option
        self._status: bool = False

    def __str__(self) -> str:
        return self._name

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._desc

    @property
    def option(self) -> BaseOption:
        if self._option is None:
            self._option = BaseOption()
        return self._option
    @option.setter
    def option(self, val: BaseOption):
        self._option = val

    @property
    def status(self) -> bool:
        return self._status
    
    def _pre_run(self, args = None) -> bool:
        if not self.option.quiet and self.option.verbose:
            print(f"{self.name.capitalize()} begin")
            print("OPTIONS:")
            print(self.option)
        return True

    def _post_run(self) -> None:
        if not self.option.quiet and self.option.verbose:
            print(f"{self.name.capitalize()} end")

    def _on_run(self, args = None) -> bool:
        return False
    
    def _pre_parse_args(self, parser: optparse.OptionParser) -> None:
        parser.add_option("-v", "--verbose", action="store_false")
        parser.add_option("-q", "--quiet", action="store_false")

    def _post_parse_args(self, opts, args) -> bool:
        if opts is not None:
            if opts.verbose is not None:
                self.option.verbose = True
            if opts.quiet is not None:
                self.option.quiet = True
        return True
    
    def parse_args(self, args) -> bool:
        parser: optparse.OptionParser = optparse.OptionParser(f"%prog {self.name} [options] DIRECTORY")

        self._pre_parse_args(parser)
        try:
            opts, args = parser.parse_args(args)
        except optparse.OptionError as ex:
            print(f"[E]{ex}")
            parser.print_help()
            return False
        return self._post_parse_args(opts, args)

    def run(self, args = None):
        if not self._pre_run(args):
            self._status = False
            return
        self._status = self._on_run(args)
        self._post_run()