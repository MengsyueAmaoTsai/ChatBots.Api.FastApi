from abc import ABC, abstractmethod

from .abstractions import IDomainEvent


class IEntity(ABC):
    @abstractmethod
    def clear_domain_events(self) -> None: ...

    @abstractmethod
    def register_domain_event(self, domain_event: IDomainEvent) -> None: ...

    @abstractmethod
    def get_domain_events(self) -> list[IDomainEvent]: ...


class Entity[TEntityId](IEntity):
    def __init__(self, id: TEntityId) -> None:
        self._domain_events: list[IDomainEvent] = []

        self._id = id

    @property
    def id(self) -> TEntityId:
        return self._id

    def clear_domain_events(self) -> None:
        self._domain_events.clear()

    def register_domain_event(self, domain_event: IDomainEvent) -> None:
        self._domain_events.append(domain_event)

    def get_domain_events(self) -> list[IDomainEvent]:
        return self._domain_events

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
