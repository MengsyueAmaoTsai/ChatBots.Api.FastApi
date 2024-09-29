from abc import ABC

from .abstractions import IDomainEvent


class Entity[TEntityId](ABC):
    def __init__(self, id: TEntityId) -> None:
        self._domain_events: list[IDomainEvent] = []

        self._id = id

    @property
    def id(self) -> TEntityId:
        return self._id

    def __eq__(self, value: object) -> bool:
        if value is None:
            return False

        if not isinstance(value, Entity):
            return False

        return self.id == value.id  # type: ignore

    def __ne__(self, value: object) -> bool:
        return not self.__eq__(value)

    def __hash__(self) -> int:
        return hash(self.id) * 41
