from abc import ABC, abstractmethod

from infrastructure.resources.contracts.users import UserDetailsResponse
from shared_kernel.Result import ResultT


class ICommand[TResult](ABC): ...


class ICommandHandlerBase(ABC):
    @abstractmethod
    async def send[TResult](self, command: ICommand[TResult]) -> TResult: ...


class ICommandHandler[TCommand, TResult](ABC): ...


class ICommandSender(ABC):
    @abstractmethod
    async def send[TResult](self, command: ICommand[TResult]) -> TResult: ...


class CommandSender(ICommandSender):
    """"""

    def __init__(self) -> None:
        self._command_handlers: dict[type, ICommandHandlerBase] = {}

    async def send[TResult](self, command: ICommand[TResult]) -> TResult:
        command_type = type(command)

        handler = self._command_handlers.get(command_type)

        if handler is None:
            raise ValueError(f"No handler found for command {command_type}")

        return await handler.send(command)


class GetUserCommand(ICommand[ResultT[UserDetailsResponse]]):
    id: str


class GetUserCommandHandler(ICommandHandler[GetUserCommand, ResultT[UserDetailsResponse]]):
    async def handle(self, command: GetUserCommand) -> ResultT[UserDetailsResponse]: ...
