from typing import Protocol


class ICommand(Protocol):
    pass


class HelpCommand(ICommand):
    pass


class CreateUserCommand(ICommand):
    pass


class ListUsersCommand(ICommand):
    pass


class GetUserCommand(ICommand):
    id: str
