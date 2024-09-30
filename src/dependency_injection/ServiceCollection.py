from .ServiceDescriptor import ServiceDescriptor
from .ServiceLifetime import ServiceLifetime


class ServiceCollection:
    def __init__(self) -> None:
        self._descriptors: list[ServiceDescriptor] = []

    @property
    def count(self) -> int:
        return len(self._descriptors)

    def add(self, descriptor: ServiceDescriptor) -> "ServiceCollection":
        self._descriptors.append(descriptor)
        print(f"Added {descriptor} to services")
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

    def add_scoped(self, service_type: type, implementation_type: type) -> "ServiceCollection":
        self._add(service_type, implementation_type, ServiceLifetime.Scoped)
        return self

    def _add(self, service_type: type, implementation_type: type, lifetime: ServiceLifetime) -> "ServiceCollection":
        descriptor = ServiceDescriptor(service_type, implementation_type, lifetime)
        self.add(descriptor)
        return self
