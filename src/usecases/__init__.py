from abc import ABC, abstractmethod

from dependency_injections.abstractions import IServiceProvider
from infrastructure.resources import ResourceService
from infrastructure.resources.contracts.users import UserDetailsResponse
from shared_kernel.Result import ResultT


class ICommandBase(ABC): ...


class ICommand[TResult](ICommandBase, ABC): ...


class ICommandHandlerBase(ABC):
    @abstractmethod
    async def send[TResult](self, command: ICommand[TResult]) -> TResult: ...


class ICommandHandler[TCommand, TResult](ABC): ...


class ICommandSender(ABC):
    @abstractmethod
    async def send[TResult](self, command: ICommand[TResult]) -> TResult: ...


class CommandSender(ICommandSender):
    """"""

    def __init__(self, service_provider: IServiceProvider) -> None:
        self._service_provider = service_provider
        self._command_handlers: dict[type[ICommandBase], type[ICommandHandlerBase]] = {}

    async def send[TResult](self, command: ICommand[TResult]) -> TResult:
        command_type = type(command)
        handler_type = self._command_handlers.get(command_type, None)

        if handler_type is None:
            raise ValueError(f"No handler found for command {command_type}")

        handler = self._service_provider.get_required_service(handler_type)

        return await handler.send(command)


class GetUserCommand(ICommand[ResultT[UserDetailsResponse]]):
    id: str


class GetUserCommandHandler(ICommandHandler[GetUserCommand, ResultT[UserDetailsResponse]]):
    def __init__(self, resource_service: ResourceService) -> None:
        self._resource_service = resource_service

    async def handle(self, command: GetUserCommand) -> ResultT[UserDetailsResponse]: ...
