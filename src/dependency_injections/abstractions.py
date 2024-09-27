from typing import Protocol, TypeVar, overload

TImplementation = TypeVar("TImplementation")


class IServiceCollection(Protocol):
    @overload
    def add_transient(self, service_type: type) -> "IServiceCollection":
        raise NotImplementedError()

    @overload
    def add_transient(self, service_type: type, implementation_type: type) -> "IServiceCollection":
        raise NotImplementedError()

    @overload
    def add_scoped(self, service_type: type) -> "IServiceCollection":
        raise NotImplementedError()

    @overload
    def add_scoped(self, service_type: type, implementation_type: type) -> "IServiceCollection":
        raise NotImplementedError()

    @overload
    def add_singleton(self, service_type: type) -> "IServiceCollection":
        raise NotImplementedError()

    @overload
    def add_singleton(self, service_type: type, implementation_type: type) -> "IServiceCollection":
        raise NotImplementedError()

    def add_endpoints(self) -> "IServiceCollection":
        raise NotImplementedError()


class IServiceProvider(Protocol):
    def get_required_service(self, service_type: type[TImplementation]) -> TImplementation:
        raise NotImplementedError()
