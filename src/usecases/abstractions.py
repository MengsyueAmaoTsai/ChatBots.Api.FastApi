class ICommand[TResult]: ...


class ICommandHandler[TCommand, TResult]:
    async def handle(self, command: TCommand) -> TResult:
        raise NotImplementedError()


class ICommandSender:
    async def handle[TResult](self, command: ICommand[TResult]) -> TResult:
        raise NotImplementedError()
