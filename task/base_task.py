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
    
    def _pre_run(self, args: list) -> bool:
        if not self.option.quiet and self.option.verbose:
            print(f"{self.name} begin")
        return True

    def _post_run(self) -> None:
        if not self.option.quiet and self.option.verbose:
            print(f"{self.name} end")

    def _on_run(self, args: list = None) -> bool:
        return False

    def run(self, args: list = None):
        if not self._pre_run(args):
            self._status = False
            return
        self._status = self._on_run(args)
        self._post_run()
        return