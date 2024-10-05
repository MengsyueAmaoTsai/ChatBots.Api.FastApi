from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Optional, SupportsIndex, cast, overload


class ServiceCollectionReadOnlyException(Exception):
    def __init__(self) -> None:
        super().__init__("Service collection is read-only.")


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


class ServiceCacheKey:
    def __init__(self, service_identifier: ServiceIdentifier, slot: int) -> None:
        self._identifier = service_identifier
        self._slot = slot


class ServiceLifetime(Enum):
    Singleton = 0
    Scoped = 1
    Transient = 2


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
        self, service_type: type, factory: Callable[["IServiceProvider"], object], lifetime: ServiceLifetime
    ) -> None: ...

    @overload
    def __init__(
        self,
        service_type: type,
        service_key: Optional[object],
        factory: Callable[["IServiceProvider", Optional[object]], object],
        lifetime: ServiceLifetime,
    ) -> None: ...

    def __init__(self, service_type: type, *args: Any, **kwargs: Any) -> None:
        self._service_type = service_type

        self._implementation_instance: Optional[object] = None
        self._implementation_factory: Optional[Callable[["IServiceProvider"], Optional[object]]] = None
        self._implementation_type: Optional[type] = None

        if len(args) == 2 and isinstance(args[0], type) and isinstance(args[1], ServiceLifetime):
            self._implementation_type = args[0]
            self._lifetime = args[1]

        if (
            len(args) == 3
            and isinstance(args[0], object)
            and isinstance(args[1], type)
            and isinstance(args[2], ServiceLifetime)
        ):
            self._service_key = args[0]
            self._implementation_type = args[1]
            self._lifetime = args[2]

        if len(args) == 1 and isinstance(args[0], object):
            self._implementation_instance = args[0]
            self._lifetime = ServiceLifetime.Singleton
            self._service_key = None

        if len(args) == 2 and isinstance(args[0], object) and isinstance(args[1], object):
            self._implementation_instance = args[1]
            self._lifetime = ServiceLifetime.Singleton
            self._service_key = None

        if len(args) == 2 and callable(args[0]) and isinstance(args[1], ServiceLifetime):
            self._service_key = None
            self._implementation_factory = args[0]
            self._lifetime = args[1]

        if (
            len(args) == 3
            and isinstance(args[0], object)
            and callable(args[1])
            and isinstance(args[2], ServiceLifetime)
        ):
            self._service_key = args[0]
            self._lifetime = args[2]

            if self.service_key is None:
                self._implementation_factory = lambda sp: args[1](sp, None)
            else:
                self._implementation_factory = args[1]

        if len(args) == 2 and isinstance(args[0], object) and isinstance(args[1], ServiceLifetime):
            self._service_key = args[0]
            self._lifetime = args[1]

    @property
    def lifetime(self) -> ServiceLifetime:
        return self._lifetime

    @property
    def service_type(self) -> type:
        return self._service_type

    @property
    def service_key(self) -> Optional[object]:
        return self._service_key

    @property
    def implementation_type(self) -> Optional[type]:
        return None if self.is_keyed_service else self._implementation_type

    @property
    def keyed_implementation_type(self) -> Optional[type]:
        if not self.is_keyed_service:
            raise ValueError("Service is not keyed")

        return self._service_type

    @property
    def implementation_instance(self) -> Optional[object]:
        return None if self.is_keyed_service else self._implementation_instance

    @property
    def keyed_implementation_instance(self) -> Optional[object]:
        if not self.is_keyed_service:
            raise ValueError("Service is not keyed")

        return self._service_key

    @property
    def implementation_factory(self) -> Optional[Callable[["IServiceProvider"], Optional[object]]]:
        return (
            None
            if self.is_keyed_service
            else cast(Callable[["IServiceProvider"], Optional[object]], self._implementation_factory)
        )

    @property
    def keyed_implementation_factory(
        self,
    ) -> Optional[Callable[["IServiceProvider", Optional[object]], Optional[object]]]:
        if not self.is_keyed_service:
            raise ValueError("Service is not keyed")

        return self.keyed_implementation_factory

    @property
    def is_keyed_service(self) -> bool:
        return self._service_key is not None


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


class IServiceProvider: ...


class IServiceCollection(list[ServiceDescriptor], ABC):
    @property
    @abstractmethod
    def length(self) -> int: ...

    @property
    @abstractmethod
    def is_read_only(self) -> bool: ...

    @overload
    def add_singleton(self, service_type: type, implementation_type: type) -> "IServiceCollection": ...

    @overload
    def add_singleton(
        self, service_type: type, implementation_factory: Callable[[IServiceProvider], object]
    ) -> "IServiceCollection": ...

    @overload
    def add_singleton(self, service_type: type) -> "IServiceCollection": ...

    @overload
    def add_singleton(
        self,
        service_type: type,
        implementation_type: type,
        implementation_factory: Callable[["IServiceProvider"], object],
    ) -> "IServiceCollection": ...

    @overload
    def add_singleton(self, service_type: type, implementation_instance: object) -> "IServiceCollection": ...

    @overload
    def add_singleton(self, implementation_instance: object) -> "IServiceCollection": ...

    def add_singleton(self, *args: Any, **kwargs: Any) -> "IServiceCollection":
        if len(args) == 2 and isinstance(args[0], type) and isinstance(args[1], type):
            service_type = args[0]
            implementation_type = args[1]
            self.__add(service_type, implementation_type, ServiceLifetime.Singleton)

        if len(args) == 2 and isinstance(args[0], type) and callable(args[1]):
            service_type = args[0]
            factory = args[1]
            self.__add(service_type, factory, ServiceLifetime.Singleton)

        if len(args) == 1 and isinstance(args[0], type):
            service_type = args[0]
            self.__add(service_type, service_type, ServiceLifetime.Singleton)

        if len(args) == 3 and isinstance(args[0], type) and isinstance(args[1], type) and callable(args[2]):
            service_type = args[0]
            implementation_type = args[1]
            factory = args[2]
            self.__add(service_type, factory, ServiceLifetime.Singleton)

        if len(args) == 1 and isinstance(args[0], object):
            instance = args[0]
            descriptor = ServiceDescriptor(type(instance), instance)
            self.append(descriptor)

        if len(args) == 2 and isinstance(args[0], type):
            service_type = args[0]
            instance = args[1]
            descriptor = ServiceDescriptor(service_type, instance)
            self.append(descriptor)

        return self

    @abstractmethod
    def remove_at(self, index: SupportsIndex) -> None: ...

    @overload
    def __add(
        self,
        service_type: type,
        implementation_factory: Callable[[IServiceProvider], object],
        lifetime: ServiceLifetime,
    ) -> "IServiceCollection": ...

    @overload
    def __add(
        self, service_type: type, implementation_type: type, lifetime: ServiceLifetime
    ) -> "IServiceCollection": ...

    def __add(self, *args: Any, **_: Any) -> "IServiceCollection":
        if len(args) == 3 and callable(args[1]):
            service_type = args[0]
            factory = args[1]
            lifetime = args[2]
            descriptor = ServiceDescriptor(service_type, factory, lifetime)
            self.append(descriptor)

        if len(args) == 3 and isinstance(args[1], type):
            service_type = args[0]
            implementation_type = args[1]
            lifetime = args[2]
            descriptor = ServiceDescriptor(service_type, implementation_type, lifetime)
            self.append(descriptor)

        return self


class ServiceCollection(IServiceCollection):
    def __init__(self) -> None:
        self._is_read_only = False

    @property
    def length(self) -> int:
        return len(self)

    @property
    def is_read_only(self) -> bool:
        return self._is_read_only

    def clear(self) -> None:
        self.__check_read_only()
        return super().clear()

    def make_read_only(self) -> None:
        self._is_read_only = True

    def contains(self, item: ServiceDescriptor) -> bool:
        return item in self

    def copy_to(self, array: list[ServiceDescriptor], array_index: int) -> None:
        self.copy_to(array, array_index)

    def remove(self, item: ServiceDescriptor) -> None:
        self.__check_read_only()
        super().remove(item)

    def index_of(self, item: ServiceDescriptor) -> int:
        return self.index(item)

    def insert(self, index: SupportsIndex, object: ServiceDescriptor) -> None:
        self.__check_read_only()
        return super().insert(index, object)

    def remove_at(self, index: SupportsIndex) -> None:
        self.__check_read_only()
        super().pop(index)

    def append(self, descriptor: ServiceDescriptor) -> None:
        self.__check_read_only()
        return super().append(descriptor)

    def __check_read_only(self) -> None:
        if self.is_read_only:
            raise ServiceCollectionReadOnlyException()

    @overload
    def _add(
        self, service_type: type, implementation_type: type, lifetime: ServiceLifetime
    ) -> "IServiceCollection": ...

    @overload
    def _add(
        self,
        service_type: type,
        implementation_factory: Callable[["IServiceProvider"], object],
        lifetime: ServiceLifetime,
    ) -> "IServiceCollection": ...

    def _add(self, service_type: type, *args: Any, **kwargs: Any) -> "IServiceCollection":
        if len(args) != 2:
            raise ValueError("Invalid number of arguments")

        lifetime = args[1]

        if callable(args[0]):
            print("Factory")
            factory = args[0]
            descriptor = ServiceDescriptor(service_type, factory, lifetime)
        else:
            print("Implementation")
            implementation_type = args[0]
            descriptor = ServiceDescriptor(service_type, implementation_type, lifetime)

        self.append(descriptor)

        return self


class ServiceProviderCallSite(ServiceCallSite): ...


class IServiceScopeFactory: ...


class ConstantCallSite(ServiceCallSite):
    def __init__(self, service_type: type, default_value: Optional[object]) -> None:
        pass


class IServiceProviderIsService: ...


class IServiceProviderIsKeyedService: ...


@dataclass()
class ServiceProviderOptions:
    validate_scopes: bool = False
    validate_on_build: bool = False


class CallSiteValidator: ...


class ServiceProvider:
    def __init__(self, service_descriptors: list[ServiceDescriptor], options: ServiceProviderOptions) -> None:
        self._root = ServiceProviderEngineScope(self, True)

        self._service_accessors: ServiceAccessorCollection[ServiceIdentifier, ServiceAccessor] = (
            ServiceAccessorCollection()
        )

        self._call_site_factory = CallSiteFactory(service_descriptors)

        CallSiteFactory.add(ServiceIdentifier.from_service_type(type(IServiceProvider)), ServiceProviderCallSite())
        CallSiteFactory.add(
            ServiceIdentifier.from_service_type(type(IServiceScopeFactory)),
            ConstantCallSite(type(IServiceScopeFactory), self.root),
        )
        CallSiteFactory.add(
            ServiceIdentifier.from_service_type(type(IServiceProviderIsService)),
            ConstantCallSite(type(IServiceProviderIsService), CallSiteFactory),
        )
        CallSiteFactory.add(
            ServiceIdentifier.from_service_type(type(IServiceProviderIsKeyedService)),
            ConstantCallSite(type(IServiceProviderIsKeyedService), CallSiteFactory),
        )

        if options.validate_scopes:
            self._call_site_validator = CallSiteValidator()

        if options.validate_on_build:
            exceptions: list[Exception] = []
            for descriptor in service_descriptors:
                try:
                    print("Validate service: ", descriptor)
                except Exception as e:
                    exceptions.append(e)

            if exceptions:
                raise Exception(f"Validation failed: {exceptions}")

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
