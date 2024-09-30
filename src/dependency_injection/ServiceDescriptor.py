from typing import Any, Callable, Optional, overload

from .abstractions import IServiceProvider
from .ServiceLifetime import ServiceLifetime


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
        self, service_type: type, factory: Callable[[IServiceProvider], object], lifetime: ServiceLifetime
    ) -> None: ...

    @overload
    def __init__(
        self,
        service_type: type,
        service_key: Optional[object],
        factory: Callable[[IServiceProvider, Optional[object]], object],
    ) -> None: ...

    @overload
    def __init__(self, service_type: type, service_key: Optional[object], lifetime: ServiceLifetime) -> None: ...

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._service_type = args[0]
        self._lifetime = ServiceLifetime.Singleton if len(args) == 2 else args[-1]

    @property
    def lifetime(self) -> ServiceLifetime:
        return self._lifetime

    @property
    def service_key(self) -> Optional[object]:
        raise NotImplementedError()

    @property
    def service_type(self) -> type:
        return self._service_type

    def __repr__(self) -> str:
        text = ""
        text += f"ServiceType: {self._service_type.__name__}, Lifetime: {self.lifetime}"
        return text
