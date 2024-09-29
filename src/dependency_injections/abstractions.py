from typing import Protocol, TypeVar, overload

from .ServiceDescriptor import ServiceDescriptor

TImplementation = TypeVar("TImplementation")


class IServiceCollection(Protocol):
    def add(self, service_descriptor: ServiceDescriptor) -> "IServiceCollection": ...

    @overload
    def add_transient(self, service_type: type) -> "IServiceCollection": ...

    @overload
    def add_transient(self, service_type: type, implementation_type: type) -> "IServiceCollection": ...

    @overload
    def add_scoped(self, service_type: type) -> "IServiceCollection": ...

    @overload
    def add_scoped(self, service_type: type, implementation_type: type) -> "IServiceCollection": ...

    @overload
    def add_singleton(self, service_type: type) -> "IServiceCollection": ...

    @overload
    def add_singleton(self, service_type: type, implementation_type: type) -> "IServiceCollection": ...

    def add_endpoints(self) -> "IServiceCollection": ...
    def add_commands(self) -> "IServiceCollection": ...


class IServiceProvider(Protocol):
    def get_required_service(self, service_type: type[TImplementation]) -> TImplementation: ...
