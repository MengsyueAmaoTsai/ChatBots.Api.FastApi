import os
from abc import ABC
from dataclasses import dataclass
from typing import Any, Callable, Optional, cast, overload

from configuration import ConfigurationManager, IConfiguration
from dependency_injection import IServiceCollection, IServiceProvider, ServiceCollection, ServiceDescriptor


class IHostApplicationLifetime(ABC): ...


class IApplicationLifetime(ABC): ...


class IHostingEnvironment(ABC):
    environment_name: str
    application_name: str
    content_root_path: str
    content_root_file_provider: object


class IHostBuilder(ABC): ...


class IHostService(ABC): ...


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
        self.hosting_environment: Optional[IHostingEnvironment] = None

    @property
    def properties(self) -> dict[object, object]:
        return self._properties


@dataclass()
class HostingEnvironment(IHostingEnvironment):
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


class ApplicationLifetime(IHostApplicationLifetime): ...


class HostBuilder:
    @classmethod
    def create_hosting_environment(cls, host_configuration: IConfiguration) -> tuple[IHostingEnvironment, object]:
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
        hosting_environment: IHostingEnvironment,
        default_file_provider: object,
        app_configuration: IConfiguration,
        service_provider_getter: Callable[[], IServiceProvider],
    ) -> None:
        services.add_singleton(IHostingEnvironment, hosting_environment)
        services.add_singleton(host_builder_context)
        services.add_singleton(IConfiguration, lambda _: app_configuration)
        # services.add_singleton(s => (IApplicationLifetime)s.get_required_service(IHostApplicationLifetime));
        services.add_singleton(IHostApplicationLifetime, ApplicationLifetime)


# AddLifetime(services);
# services.AddSingleton<IHost>(_ =>
# {
#     IServiceProvider appServices = serviceProviderGetter();
#     return new Internal.Host(appServices,
#         hostingEnvironment,
#         defaultFileProvider,
#         appServices.GetRequiredService<IHostApplicationLifetime>(),
#         appServices.GetRequiredService<ILogger<Internal.Host>>(),
#         appServices.GetRequiredService<IHostLifetime>(),
#         appServices.GetRequiredService<IOptions<HostOptions>>());
# });
# services.add_options().configure(HostOptions, lambda options: options.initialize(host_builder_context.configuration); });
# services.add_logging();
# services.add_metrics();


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
        self._app_services: IServiceProvider

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

            print("TODO: ServiceProviderOptions", service_provider_options)

        if (len(args) == 2) and isinstance(args[0], HostApplicationBuilderSettings) and isinstance(args[1], bool):
            print("HostApplicationBuilderSettings and bool args")

    def _create_service_provider(self) -> IServiceProvider:
        print("Create service provider")
        raise NotImplementedError("Create service provider")

    @property
    def services(self) -> IServiceCollection:
        return self._service_collection

    def __initialize(
        self, settings: HostApplicationBuilderSettings
    ) -> tuple[HostBuilderContext, IHostingEnvironment, LoggingBuilder, MetricsBuilder]:
        # add_command_config(self._configuration, settings.args)
        options = {}

        if settings.application_name is not None:
            options["application_name"] = settings.application_name

        if settings.environment_name is not None:
            options["environment_name"] = settings.environment_name

        if settings.content_root_path is not None:
            options["content_root_path"] = settings.content_root_path

        if not options:
            print("self._configuration.add_in_memory_collection(options)")

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


class BootstrapHostBuilder(IHostBuilder):
    def __init__(self, builder: HostApplicationBuilder) -> None:
        self._configure_host_actions = []
        self._configure_app_actions = []
        self._configure_service_actions = []

        self._builder = builder
        self._context: Optional[HostBuilderContext] = None

        for descriptor in self._builder.services:
            if descriptor.service_type == HostBuilderContext:
                self._context = cast(HostBuilderContext, descriptor.implementation_instance)
                break

        if self._context is None:  # type: ignore
            raise ValueError("HostBuilderContext not found")

    @property
    def context(self) -> HostBuilderContext:
        return cast(HostBuilderContext, self._context)

    @property
    def properties(self) -> dict[object, object]:
        return self.context.properties

    def run_default_callbacks(self) -> ServiceDescriptor:
        raise NotImplementedError("Not implemented yet")
        for action in self._configure_host_actions:
            print(action)

        for action in self._configure_app_actions:
            print(action)

        for action in self._configure_service_actions:
            print(action)

        generic_web_host_service_descriptor: Optional[ServiceDescriptor] = None

        for i in range(len(self._builder.services) - 1, -1, -1):
            descriptor = self._builder.services[i]

            if descriptor.service_type == IHostService:
                generic_web_host_service_descriptor = descriptor
                self._builder.services.remove_at(i)
                break

        if generic_web_host_service_descriptor is None:
            raise ValueError("GenericWebHostServiceDescriptor not found")

        return generic_web_host_service_descriptor
