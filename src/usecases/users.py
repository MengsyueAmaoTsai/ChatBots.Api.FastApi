from infrastructure.resources import ResourceService
from infrastructure.resources.contracts.users import UserDetailsResponse
from shared_kernel.Result import ResultT

from .abstractions import ICommand, ICommandHandler


class GetUserCommand(ICommand[ResultT[UserDetailsResponse]]):
    """Command: /rc users --id <id>"""

    id: str


class GetUserCommandHandler(ICommandHandler[GetUserCommand, ResultT[UserDetailsResponse]]):
    def __init__(self, resource_service: ResourceService):
        self.resource_service = resource_service

    async def handle(self, command: GetUserCommand) -> ResultT[UserDetailsResponse]:
        result = await self.resource_service.get_user(command.id)

        if result.is_failure:
            return ResultT[UserDetailsResponse].failure(result.error)

        user = result.value

        return ResultT[UserDetailsResponse].success(user)
