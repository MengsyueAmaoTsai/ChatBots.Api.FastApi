from typing import Protocol, TypeVar

TImplementation = TypeVar("TImplementation")


class IServiceCollection(Protocol):
    def add_transient(self, service_type: type) -> "IServiceCollection":
        raise NotImplementedError()

    def add_scoped(self, service_type: type) -> "IServiceCollection":
        raise NotImplementedError()

    def add_singleton(self, service_type: type) -> "IServiceCollection":
        raise NotImplementedError()

    def add_endpoints(self) -> "IServiceCollection":
        raise NotImplementedError()


class IServiceProvider(Protocol):
    def get_required_service(self, service_type: type[TImplementation]) -> TImplementation:
        raise NotImplementedError()
