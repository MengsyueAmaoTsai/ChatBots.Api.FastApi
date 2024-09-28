class ICommandBase: ...


class ICommand[TResult](ICommandBase): ...


class ICommandHandlerBase: ...


class ICommandHandler[TCommand, TResult](ICommandHandlerBase):
    async def handle(self, command: TCommand) -> TResult:
        raise NotImplementedError()


class ICommandSender:
    async def handle[TResult](self, command: ICommand[TResult]) -> TResult:
        raise NotImplementedError()
