from collections.abc import Callable
from enum import Enum
from typing import Any, Optional, overload


class ServiceLifetime(Enum):
    Singleton = 1
    Scoped = 2
    Transient = 3


class ServiceDescriptor:
    @overload
    def __init__(self, service_type: type, implementation_type: type, lifetime: ServiceLifetime) -> None: ...

    @overload
    def __init__(
        self, service_type: type, service_key: Optional[object], implementation_type: type, lifetime: ServiceLifetime
    ) -> None: ...

    @overload
    def __init__(self, service_type: type, instance: object) -> None: ...

    @overload
    def __init__(self, service_type: type, service_key: Optional[object], instance: object) -> None: ...

    @overload
    def __init__(
        self, service_type: type, factory: Callable[["ServiceProvider"], object], lifetime: ServiceLifetime
    ) -> None: ...

    @overload
    def __init__(
        self,
        service_type: type,
        service_key: Optional[object],
        factory: Callable[["ServiceProvider", Optional[object]], object],
    ) -> None: ...

    @overload
    def __init__(self, service_type: type, service_key: Optional[object], lifetime: ServiceLifetime) -> None: ...

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._service_type = args[0]
        self._lifetime = ServiceLifetime.Singleton if len(args) == 2 else args[-1]

    @property
    def lifetime(self) -> ServiceLifetime:
        return self._lifetime

    @property
    def service_key(self) -> Optional[object]:
        raise NotImplementedError()

    @property
    def service_type(self) -> type:
        return self._service_type

    def __repr__(self) -> str:
        text = ""
        text += f"ServiceType: {self._service_type.__name__}, Lifetime: {self.lifetime}"
        return text


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


class ServiceProvider: ...
