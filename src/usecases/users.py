from infrastructure.resources import ResourceService
from infrastructure.resources.contracts.users import UserResponse

from .abstractions import ICommand, ICommandHandler


class GetUserCommand(ICommand[list[UserResponse]]):
    pass


class GetUserCommandHandler(ICommandHandler[GetUserCommand, list[UserResponse]]):
    def __init__(self, resource_service: ResourceService) -> None:
        self._resource_service = resource_service

    async def handle(self, command: GetUserCommand) -> list[UserResponse]:
        users = await self._resource_service.list_users()
        return users
