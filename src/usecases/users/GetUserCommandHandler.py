from infrastructure.resources import ResourceService
from infrastructure.resources.contracts.users import UserDetailsResponse


class GetUserCommand:
    user_id: str


class GetUserCommandHandler:
    def __init__(self, resource_service: ResourceService) -> None:
        self._resource_service = resource_service

    async def handle(self, command: GetUserCommand) -> UserDetailsResponse:
        user = await self._resource_service.get_user(command.user_id)

        return user
