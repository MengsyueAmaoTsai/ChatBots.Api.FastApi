class ICommand[TResult]: ...


class ICommandHandler[TCommand, TResult]:
    async def handle(self, command: TCommand) -> TResult:
        raise NotImplementedError()
