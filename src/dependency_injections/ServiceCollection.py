from typing import Optional, overload

from endpoints import LineMessagingEndpoint

from .abstractions import IServiceCollection, IServiceProvider
from .ServiceDescriptor import ServiceDescriptor
from .ServiceLifetime import ServiceLifetime
from .ServiceProvider import ServiceProvider


class ServiceCollection(IServiceCollection):
    def __init__(self) -> None:
        self._service_descriptors: list[ServiceDescriptor] = []

    @overload
    def add_transient(self, service_type: type) -> IServiceCollection: ...

    @overload
    def add_transient(self, service_type: type, implementation_type: type) -> IServiceCollection: ...

    def add_transient(self, service_type: type, implementation_type: Optional[type] = None) -> IServiceCollection:
        if implementation_type is None:
            implementation_type = service_type

        descriptor = ServiceDescriptor(service_type, implementation_type, ServiceLifetime.Transient)
        self._service_descriptors.append(descriptor)

        print(
            f"Registered {descriptor.lifetime} service. Type: {descriptor.type.__name__} -> {descriptor.implementation_type.__name__}"
        )
        return self

    @overload
    def add_scoped(self, service_type: type) -> IServiceCollection: ...

    @overload
    def add_scoped(self, service_type: type, implementation_type: type) -> IServiceCollection: ...

    def add_scoped(self, service_type: type, implementation_type: Optional[type] = None) -> IServiceCollection:
        if implementation_type is None:
            implementation_type = service_type

        descriptor = ServiceDescriptor(service_type, implementation_type, ServiceLifetime.Scoped)
        self._service_descriptors.append(descriptor)

        print(
            f"Registered {descriptor.lifetime} service. Type: {descriptor.type.__name__} -> {descriptor.implementation_type.__name__}"
        )
        return self

    @overload
    def add_singleton(self, service_type: type) -> IServiceCollection: ...

    @overload
    def add_singleton(self, service_type: type, implementation_type: type) -> IServiceCollection: ...

    def add_singleton(self, service_type: type, implementation_type: Optional[type] = None) -> IServiceCollection:
        if implementation_type is None:
            implementation_type = service_type

        descriptor = ServiceDescriptor(service_type, implementation_type, ServiceLifetime.Singleton)
        self._service_descriptors.append(descriptor)

        print(
            f"Registered {descriptor.lifetime} service. Type: {descriptor.type.__name__} -> {descriptor.implementation_type.__name__}"
        )
        return self

    def build_service_provider(self) -> "IServiceProvider":
        return ServiceProvider(self._service_descriptors)

    def add_endpoints(self) -> "IServiceCollection":
        endpoint_types: list[type] = [LineMessagingEndpoint]

        for endpoint in endpoint_types:
            self.add_transient(endpoint)

        return self
