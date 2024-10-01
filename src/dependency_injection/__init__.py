from typing import Any, Callable, Optional, cast, overload


class ServiceIdentifier:
    @staticmethod
    def from_service_type(service_type: type) -> "ServiceIdentifier":
        return ServiceIdentifier()


class ServiceCallSite: ...


class ServiceAccessorCollection[TKey, TValue]:
    def __init__(self) -> None:
        self._dict: dict[TKey, TValue] = {}

    def get_or_add(self, key: TKey, factory: Callable[[TKey], TValue]) -> TValue:
        if key in self._dict:
            return self._dict[key]

        value = factory(key)
        self._dict[key] = value
        return value


class ServiceProviderEngineScope:
    pass


class ServiceAccessor:
    call_site: Optional[ServiceCallSite] = None
    realized_service: Optional[Callable[[ServiceProviderEngineScope], Optional[object]]] = None


class ServiceProvider:
    def __init__(self) -> None:
        self._root = ServiceProviderEngineScope()

        self._service_accessors: ServiceAccessorCollection[ServiceIdentifier, ServiceAccessor] = (
            ServiceAccessorCollection()
        )

    @property
    def root(self) -> ServiceProviderEngineScope:
        return self._root

    def get_required_service[TService](self, service_type: type[TService]) -> TService:
        service = self.get_service(service_type)

        if service is None:
            raise Exception(f"Service of type {service_type.__name__} not found")

        return cast(TService, service)

    def get_service(self, service_type: type) -> Optional[object]:
        return self._get_service(ServiceIdentifier.from_service_type(service_type), self.root)

    def _get_service(
        self, service_identifier: ServiceIdentifier, scope: ServiceProviderEngineScope
    ) -> Optional[object]:
        accessor = self._service_accessors.get_or_add(service_identifier, self._create_service_accessor)

        if accessor.realized_service is None:
            return None

        return accessor.realized_service(scope)

    def _create_service_accessor(self, service_identifier: ServiceIdentifier) -> ServiceAccessor:
        return ServiceAccessor()
