from typing import Protocol


class ICommand(Protocol):
    pass


class HelpCommand(ICommand):
    pass
