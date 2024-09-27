from infrastructure.resources import ResourceService
from infrastructure.resources.contracts.users import UserResponse


class ListUsersCommand:
    pass


class ListUsersCommandHandler:
    def __init__(self, resource_service: ResourceService) -> None:
        self._resource_service = resource_service

    async def handle(self, command: ListUsersCommand) -> list[UserResponse]:
        users = await self._resource_service.list_users()

        return users
