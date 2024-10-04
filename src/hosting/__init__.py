import os
from abc import ABC
from dataclasses import dataclass
from typing import Any, Callable, Optional, overload

from configuration import ConfigurationManager, IConfiguration
from dependency_injection import IServiceCollection, IServiceProvider, ServiceCollection


class IHostEnvironment(ABC):
    environment_name: str
    application_name: str
    content_root_path: str
    content_root_file_provider: object


class IHostingEnvironment(ABC):
    environment_name: str
    application_name: str
    content_root_path: str
    content_root_file_provider: object


@dataclass()
class HostApplicationBuilderSettings:
    disable_defaults: bool = False
    args: Optional[list[str]] = None
    configuration: Optional[ConfigurationManager] = None
    application_name: Optional[str] = None
    environment_name: Optional[str] = None
    content_root_path: Optional[str] = None


class LoggingBuilder:
    def __init__(self, services: IServiceCollection) -> None:
        self._services = services

    @property
    def services(self) -> IServiceCollection:
        return self._services


class MetricsBuilder:
    def __init__(self, services: IServiceCollection) -> None:
        self._services = services

    @property
    def services(self) -> IServiceCollection:
        return self._services


class HostBuilderContext:
    def __init__(self, properties: dict[object, object]) -> None:
        self._properties = properties
        self.configuration: Optional[IConfiguration] = None
        self.hosting_environment: Optional[IHostEnvironment] = None

    @property
    def properties(self) -> dict[object, object]:
        return self._properties


@dataclass()
class HostingEnvironment(IHostingEnvironment, IHostEnvironment):
    environment_name: str = str()
    application_name: str = str()
    content_root_path: str = str()
    content_root_file_provider: object = object()


class HostDefaults:
    EnvironmentKey = "environment"
    ApplicationKey = "applicationName"
    ContentRootKey = "contentRoot"


class Environments:
    Production = "Production"
    Staging = "Staging"
    Development = "Development"


class HostBuilder:
    @classmethod
    def create_hosting_environment(cls, host_configuration: IConfiguration) -> tuple[IHostEnvironment, object]:
        hosting_environment = HostingEnvironment(
            environment_name=host_configuration[HostDefaults.EnvironmentKey] or Environments.Production,
            content_root_path=HostBuilder._resolve_content_root_path(
                host_configuration[HostDefaults.ContentRootKey], os.getcwd()
            ),
        )

        application_name = host_configuration[HostDefaults.ApplicationKey]

        if application_name is None or application_name == str():
            application_name = os.path.basename(os.getcwd())

        hosting_environment.application_name = application_name

        physical_file_provider = object()
        hosting_environment.content_root_file_provider = physical_file_provider

        return hosting_environment, physical_file_provider

    @classmethod
    def _resolve_content_root_path(cls, content_root_path: Optional[str], base_path: str) -> str:
        if content_root_path == str() or content_root_path is None:
            return base_path

        if content_root_path == os.getcwd():
            return content_root_path

        return os.path.join(base_path, content_root_path)

    @staticmethod
    def populate_service_collection(
        services: IServiceCollection,
        host_builder_context: HostBuilderContext,
        hosting_environment: HostingEnvironment,
        default_file_provider: object,
        app_configuration: IConfiguration,
        service_provider_getter: Callable[[], IServiceProvider],
    ) -> None:
        pass


class HostApplicationBuilder:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, args: Optional[list[str]]) -> None: ...

    @overload
    def __init__(self, settings: Optional[HostApplicationBuilderSettings]) -> None: ...

    @overload
    def __init__(self, settings: Optional[HostApplicationBuilderSettings], empty: bool) -> None: ...

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._service_collection = ServiceCollection()
        self._app_services: Optional[IServiceProvider] = None

        if len(args) == 0:
            print("No args")

        if (len(args) == 1) and isinstance(args[0], list):
            print("List args")

        if (len(args) == 1) and isinstance(args[0], HostApplicationBuilderSettings):
            settings = args[0] or HostApplicationBuilderSettings()
            self._configuration = settings.configuration or ConfigurationManager()

            if not settings.disable_defaults:
                ...

            context, environment, logging, metrics = self.__initialize(settings)

            print(environment)
            print(context)

            service_provider_options = None

            if not settings.disable_defaults:
                ...

        if (len(args) == 2) and isinstance(args[0], HostApplicationBuilderSettings) and isinstance(args[1], bool):
            print("HostApplicationBuilderSettings and bool args")

    @property
    def services(self) -> IServiceCollection:
        return self._service_collection

    def __initialize(
        self, settings: HostApplicationBuilderSettings
    ) -> tuple[HostBuilderContext, IHostEnvironment, LoggingBuilder, MetricsBuilder]:
        # add_command_config(self._configuration, settings.args)
        options = {}

        if settings.application_name is not None:
            options["application_name"] = settings.application_name

        if settings.environment_name is not None:
            options["environment_name"] = settings.environment_name

        if settings.content_root_path is not None:
            options["content_root_path"] = settings.content_root_path

        if not options:
            print("No options")  # self._configuration.add_in_memory_collection(options)

        hosting_environment, physical_file_provider = HostBuilder.create_hosting_environment(self._configuration)
        # self._configuration.set_file_provider(physical_file_provider)

        host_builder_context = HostBuilderContext({})
        host_builder_context.hosting_environment = hosting_environment
        host_builder_context.configuration = self._configuration

        HostBuilder.populate_service_collection(
            self.services,
            host_builder_context,
            hosting_environment,
            physical_file_provider,
            self._configuration,
            lambda: self._app_services,
        )

        return host_builder_context, hosting_environment, LoggingBuilder(self.services), MetricsBuilder(self.services)
