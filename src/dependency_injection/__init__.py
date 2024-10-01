from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional, overload


class ServiceDescriptor: ...


class IServiceProvider(ABC):
    @abstractmethod
    def get_service(self, service_type: type) -> Optional[object]: ...


class IKeyedServiceProvider(ABC):
    @abstractmethod
    def get_keyed_service(self, service_type: type, service_key: Optional[object]) -> Optional[object]: ...

    @abstractmethod
    def get_required_keyed_service(self, service_type: type, service_key: Optional[object]) -> object: ...


@dataclass(frozen=True)
class ServiceProviderOptions:
    validate_scopes: bool = False
    validate_on_build: bool = False

    @staticmethod
    def default() -> "ServiceProviderOptions":
        return ServiceProviderOptions()


class IServiceCollection(ABC):
    @overload
    def build_service_provider(self) -> "IServiceProvider": ...

    @overload
    def build_service_provider(self, validate_scopes: bool) -> IServiceProvider: ...

    @overload
    def build_service_provider(self, options: ServiceProviderOptions) -> IServiceProvider: ...

    def build_service_provider(self, *args: Any, **kwargs: Any) -> IServiceProvider:
        if len(args) == 1 and isinstance(args[0], ServiceProviderOptions):
            options = args[0]
            return ServiceProvider(self, options)

        if len(args) == 1 and isinstance(args[0], bool):
            validate_scopes = args[0]
            options = ServiceProviderOptions(validate_scopes=validate_scopes)
            return ServiceProvider(self, options)

        if len(args) == 0:
            options = ServiceProviderOptions.default()
            return ServiceProvider(self, options)

        raise ValueError(f"Invalid arguments: {args}")


class ServiceCollection(IServiceCollection): ...


class ServiceProvider(IServiceProvider, IKeyedServiceProvider):
    def __init__(self, service_collection: IServiceCollection, options: ServiceProviderOptions):
        self.service_collection = service_collection
        self.options = options

    def get_keyed_service(self, service_type: type, service_key: Optional[object]) -> Optional[object]:
        raise NotImplementedError

    def get_required_keyed_service(self, service_type: type, service_key: Optional[object]) -> object:
        raise NotImplementedError

    def get_service(self, service_type: type) -> Optional[object]:
        raise NotImplementedError
