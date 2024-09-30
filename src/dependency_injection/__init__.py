from enum import Enum


class ServiceLifetime(Enum):
    Singleton = 1
    Scoped = 2
    Transient = 3


class ServiceDescriptor: ...


class ServiceCollection:
    def __init__(self) -> None:
        self._descriptors: list[ServiceDescriptor] = []

    @property
    def count(self) -> int:
        return len(self._descriptors)

    def add(self, descriptor: ServiceDescriptor) -> "ServiceCollection":
        self._descriptors.append(descriptor)
        return self

    def remove(self, descriptor: ServiceDescriptor) -> "ServiceCollection":
        self._descriptors.remove(descriptor)
        return self

    def index_of(self, descriptor: ServiceDescriptor) -> int:
        return self._descriptors.index(descriptor)

    def insert(self, index: int, descriptor: ServiceDescriptor) -> "ServiceCollection":
        self._descriptors.insert(index, descriptor)
        return self

    def clear(self) -> "ServiceCollection":
        self._descriptors.clear()
        return self

    def remove_at(self, index: int) -> "ServiceCollection":
        self._descriptors.pop(index)
        return self

    def contains(self, descriptor: ServiceDescriptor) -> bool:
        return descriptor in self._descriptors

    def copy_to(self, array: list[ServiceDescriptor], array_index: int) -> None:
        for index, descriptor in enumerate(self._descriptors):
            array[array_index + index] = descriptor


class ServiceProvider: ...
