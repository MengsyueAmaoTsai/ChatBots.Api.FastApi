from .abstractions import ICommand, ICommandSender


class CommandSender(ICommandSender):
    def __init__(self) -> None: ...

    async def handle[TResult](self, command: ICommand[TResult]) -> TResult:
        raise NotImplementedError()
