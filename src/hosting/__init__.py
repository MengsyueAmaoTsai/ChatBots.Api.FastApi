from typing import Optional

from dependency_injection import ServiceCollection, ServiceDescriptor, ServiceProvider


class HostBuilder:
    def __init__(self) -> None: ...

    @staticmethod
    def resolve_host(service_provider: ServiceProvider) -> object:
        pass


class HostApplicationBuilderSettings: ...


class HostApplicationBuilder:
    def __init__(self, settings: HostApplicationBuilderSettings) -> None:
        self._create_service_provider = lambda: ServiceProvider()
        self._service_collection = ServiceCollection()
        self._app_services: Optional[ServiceProvider] = None

    @property
    def services(self) -> ServiceCollection:
        return self._service_collection

    def build(self) -> object:
        self._app_services = self._create_service_provider()

        return HostBuilder.resolve_host(self._app_services)


class BootstrapHostBuilder:
    def __init__(self, builder: HostApplicationBuilder) -> None:
        self._builder = builder

    def run_default_callbacks(self) -> "ServiceDescriptor": ...


class Host: ...
