import inspect
from enum import Enum
from typing import Any, Protocol, TypeVar

TImplementation = TypeVar("TImplementation")


class ServiceLifetime(Enum):
    Singleton = 1
    Scoped = 2
    Transient = 3


class ServiceDescriptor:
    def __init__(
        self, type: type, implementation_type: type, lifetime: ServiceLifetime
    ) -> None:
        self.type = type
        self.implementation_type = implementation_type
        self.lifetime = lifetime
        self.implementation: object | None = None


class ServiceCollection:
    def __init__(self) -> None:
        self.__service_descriptors: list[ServiceDescriptor] = []

    def add_singleton(self, type: type, implementation: type) -> "ServiceCollection":
        self.__service_descriptors.append(
            ServiceDescriptor(type, implementation, ServiceLifetime.Singleton)
        )

        return self

    def add_scoped(self, type: type, implementation: type) -> "ServiceCollection":
        self.__service_descriptors.append(
            ServiceDescriptor(type, implementation, ServiceLifetime.Scoped)
        )
        return self

    def add_transient(self, type: type, implementation: type) -> "ServiceCollection":
        self.__service_descriptors.append(
            ServiceDescriptor(type, implementation, ServiceLifetime.Transient)
        )
        return self

    def build_service_provider(self) -> "ServiceProvider":
        return ServiceProvider(self.__service_descriptors)


class ServiceProvider:
    def __init__(self, service_descriptors: list[ServiceDescriptor]) -> None:
        self.__service_descriptors = service_descriptors
        self.__singletons: dict[type[Any], Any] = {}

    def get_required_service(
        self, service_type: type[TImplementation]
    ) -> TImplementation:
        service = self.__get_service_descriptor(service_type)

        if service.lifetime == ServiceLifetime.Singleton:
            if service.type in self.__singletons:
                return self.__singletons[service.type]

        constructor = service.implementation_type
        constructor_params = inspect.signature(constructor).parameters

        dependencies = [
            self.get_required_service(param.annotation)
            for param in constructor_params.values()
            if param.annotation is not inspect.Parameter.empty
        ]

        instance = constructor(*dependencies)

        if service.lifetime == ServiceLifetime.Singleton:
            self.__singletons[service.type] = instance

        return instance

    def __get_service_descriptor(self, service_type: type) -> ServiceDescriptor:
        service = next(
            (
                descriptor
                for descriptor in self.__service_descriptors
                if descriptor.type == service_type
            ),
            None,
        )

        if service is None:
            raise Exception(f"No service for type {service_type}")

        return service


class IMockService(Protocol):
    def mock(self) -> None:
        raise NotImplementedError()


class MockService(IMockService):
    def mock(self) -> None:
        print("Do mock!!")


class ITestService(Protocol):
    def test(self) -> None:
        raise NotImplementedError()


class TestService(ITestService):
    def __init__(self, mock_service: IMockService) -> None:
        self.mock_service = mock_service
        print("Test service init")

    def test(self) -> None:
        print("Do test!!")


if __name__ == "__main__":
    services = ServiceCollection()

    services.add_singleton(IMockService, MockService)
    services.add_singleton(ITestService, TestService)

    # services.add_scoped()
    # services.add_transient()

    service_provider = services.build_service_provider()

    mock_service = service_provider.get_required_service(IMockService)
    mock_service.mock()

    test_service = service_provider.get_required_service(ITestService)
    test_service.test()
