from dataclasses import dataclass
from typing import Callable, Optional, cast


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
    def __init__(self, provider: "ServiceProvider", is_root_scope: bool) -> None: ...


@dataclass()
class ServiceAccessor:
    call_site: Optional[ServiceCallSite] = None
    realized_service: Optional[Callable[[ServiceProviderEngineScope], Optional[object]]] = None


class ServiceDescriptor: ...


class ServiceCacheKey:
    def __init__(self, service_identifier: ServiceIdentifier, slot: int) -> None:
        self._identifier = service_identifier
        self._slot = slot


class CallSiteFactory:
    DEFAULT_SLOT = 0
    _call_site_cache: dict[ServiceCacheKey, ServiceCallSite] = {}

    def __init__(self, service_descriptors: list[ServiceDescriptor]) -> None:
        self.__populate()

    @classmethod
    def add(cls, service_identifier: ServiceIdentifier, call_site: ServiceCallSite) -> None:
        cls._call_site_cache[ServiceCacheKey(service_identifier, cls.DEFAULT_SLOT)] = call_site

    def __populate(self) -> None:
        print("Populating call site factory")


class ServiceCollection(list[ServiceDescriptor]): ...


class IServiceProvider: ...


class ServiceProviderCallSite(ServiceCallSite): ...


class IServiceScopeFactory: ...


class ConstantCallSite: ...


class IServiceProviderIsService: ...


class IServiceProviderIsKeyedService: ...


class ServiceProvider:
    def __init__(self, service_descriptors: list[ServiceDescriptor]) -> None:
        self._root = ServiceProviderEngineScope(self, True)

        self._service_accessors: ServiceAccessorCollection[ServiceIdentifier, ServiceAccessor] = (
            ServiceAccessorCollection()
        )

        self._call_site_factory = CallSiteFactory(service_descriptors)
        CallSiteFactory.add(ServiceIdentifier.from_service_type(type(IServiceProvider)), ServiceProviderCallSite())
        # CallSiteFactory.add(
        #     ServiceIdentifier.from_service_type(type(IServiceScopeFactory)),
        #     ConstantCallSite(type(IServiceScopeFactory), self.root),
        # )
        # CallSiteFactory.add(
        #     ServiceIdentifier.from_service_type(type(IServiceProviderIsService)),
        #     ConstantCallSite(type(IServiceProviderIsService), CallSiteFactory),
        # )
        # CallSiteFactory.add(
        #     ServiceIdentifier.from_service_type(type(IServiceProviderIsKeyedService)),
        #     ConstantCallSite(type(IServiceProviderIsKeyedService), CallSiteFactory),
        # )

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
        call_site = None
        return ServiceAccessor(call_site=call_site, realized_service=lambda _: None)
