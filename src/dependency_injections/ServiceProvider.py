import inspect
from typing import Any

from .abstractions import IServiceProvider, TImplementation
from .ServiceDescriptor import ServiceDescriptor
from .ServiceLifetime import ServiceLifetime


class ServiceProvider(IServiceProvider):
    def __init__(self, service_descriptors: list[ServiceDescriptor]) -> None:
        self._service_descriptors = service_descriptors
        self._singletons: dict[type[Any], Any] = {}

    def get_required_service(self, service_type: type[TImplementation]) -> TImplementation:
        service = self._get_service_descriptor(service_type)

        if service.lifetime == ServiceLifetime.Singleton:
            if service.type in self._singletons:
                return self._singletons[service.type]

        constructor = service.implementation_type
        constructor_params = inspect.signature(constructor).parameters

        dependencies = [
            self.get_required_service(param.annotation)
            for param in constructor_params.values()
            if param.annotation is not inspect.Parameter.empty
        ]

        instance = constructor(*dependencies)

        if service.lifetime == ServiceLifetime.Singleton:
            self._singletons[service.type] = instance

        return instance

    def _get_service_descriptor(self, service_type: type[TImplementation]) -> ServiceDescriptor:
        descriptor = next(
            (descriptor for descriptor in self._service_descriptors if descriptor.type == service_type),
            None,
        )

        if descriptor is None:
            raise Exception(f"Service of type {service_type.__name__} not found.")

        return descriptor
