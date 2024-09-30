from typing import Callable, Optional

from configuration import ConfigurationManager, IConfiguration
from dependency_injection import ServiceCollection, ServiceDescriptor
from dependency_injection.abstractions import IServiceProvider

from .abstractions import IHost


class LoggingBuilder:
    def __init__(self, services: ServiceCollection) -> None:
        self._services = services

    @property
    def services(self) -> ServiceCollection:
        return self._services


class MetricsBuilder:
    def __init__(self, services: ServiceCollection) -> None:
        self._services = services

    @property
    def services(self) -> ServiceCollection:
        return self._services


class Environments:
    PRODUCTION = "Production"
    STAGING = "Staging"
    DEVELOPMENT = "Development"


class HostingEnvironment:
    environment_name: str
    application_name: str
    content_root_path: str
    content_root_file_provider: object


class HostBuilderContext:
    def __init__(self, properties: dict[object, object]):
        self._properties = properties
        self.configuration: IConfiguration
        self.hosting_environment: HostingEnvironment

    @property
    def properties(self) -> dict[object, object]:
        return self._properties


class HostBuilder:
    def __init__(self) -> None: ...

    @staticmethod
    def resolve_host(service_provider: IServiceProvider) -> IHost:
        host = service_provider.get_required_service(IHost)

        return host

    @staticmethod
    def create_hosting_environment(host_configuration: IConfiguration) -> tuple[HostingEnvironment, object]:
        hosting_environment = HostingEnvironment()
        hosting_environment.environment_name = host_configuration["environment"] or Environments.PRODUCTION
        # hosting_environment.content_root_path = self.resolve_content_root_path(host_configuration["contentRoot"], base_directory)

        application_name = host_configuration["applicationName"]

        if not application_name:
            application_name = "<UndefinedApplicationName>"

        if application_name is not None:
            hosting_environment.application_name = application_name

        file_provider = object()
        hosting_environment.content_root_file_provider = file_provider

        return hosting_environment, file_provider

    @staticmethod
    def populate_service_collection(
        services: ServiceCollection,
        host_builder_context: HostBuilderContext,
        hosting_environment: HostingEnvironment,
        file_provider: object,
        app_configuration: IConfiguration,
        service_provider_getter: Callable[[], IServiceProvider],
    ) -> None:
        pass
        # services.add_singleton(HostingEnvironment, hosting_environment)
        # services.add_singleton(IHostEnvironment, hosting_environment)
        # services.add_singleton(host_builder_context)
        # services.add_singleton(_ => app_configuration)

        # services.add_singleton(s => s.get_required_service(IHostApplicationLifetime))
        # services.add_singleton(IHostApplicationLifetime, ApplicationLifetime)

        # AddLifetime(services)
        # services.add_singleton(IHost, _ =>
        # {
        #     appServices = service_provider_getter()
        #     return new Internal.Host(appServices,
        #         hostingEnvironment,
        #         defaultFileProvider,
        #         appServices.GetRequiredService<IHostApplicationLifetime>(),
        #         appServices.GetRequiredService<ILogger<Internal.Host>>(),
        #         appServices.GetRequiredService<IHostLifetime>(),
        #         appServices.GetRequiredService<IOptions<HostOptions>>());
        # })

        # services.AddOptions().Configure<HostOptions>(options => { options.Initialize(hostBuilderContext.Configuration); });
        # services.AddLogging()
        # services.AddMetrics()


class HostApplicationBuilderSettings:
    disable_defaults: bool = False
    args: Optional[list[str]] = None
    configuration: Optional[ConfigurationManager] = None
    environment_name: Optional[str] = None
    application_name: Optional[str] = None
    content_root_path: Optional[str] = None


class HostApplicationBuilder:
    def __init__(self, settings: Optional[HostApplicationBuilderSettings]) -> None:
        self._service_collection = ServiceCollection()
        self._app_services: Optional[IServiceProvider] = None

        if settings is None:
            settings = HostApplicationBuilderSettings()

        self._configuration = settings.configuration if settings.configuration is not None else ConfigurationManager()

        host_builder_context = self.initialize(settings)
        self._host_builder_context = host_builder_context
        self._environment = None
        self._logging = None
        self._metrics = None

        if not settings.disable_defaults:
            pass

        self._create_service_provider = lambda: None
        self._configure_container = lambda: None
        self._host_builder_adapter = None

    @property
    def services(self) -> ServiceCollection:
        return self._service_collection

    @property
    def configuration(self) -> ConfigurationManager:
        return self._configuration

    def initialize(self, settings: HostApplicationBuilderSettings) -> HostBuilderContext:
        option_list: list[tuple[str, str]] = []

        if settings.application_name is not None:
            option_list.append(("applicationName", settings.application_name))

        if settings.environment_name is not None:
            option_list.append(("environment", settings.environment_name))

        if settings.content_root_path is not None:
            option_list.append(("contentRoot", settings.content_root_path))

        if len(option_list) != 0:
            pass

        (hosting_environment, file_provider) = HostBuilder.create_hosting_environment(self._configuration)
        # self.configuration.set_file_provider(file_provider)

        host_builder_context = HostBuilderContext({})
        host_builder_context.hosting_environment = hosting_environment
        host_builder_context.configuration = self._configuration

        HostBuilder.populate_service_collection(
            self.services,
            host_builder_context,
            hosting_environment,
            file_provider,
            self.configuration,
            lambda: self._app_services,  # type: ignore
        )

        self._logging = LoggingBuilder(self.services)
        self._metrics = MetricsBuilder(self.services)

        return host_builder_context

    def build(self) -> IHost:
        self._app_services = self._create_service_provider()

        return HostBuilder.resolve_host(self._app_services)  # type: ignore


class BootstrapHostBuilder:
    def __init__(self, builder: HostApplicationBuilder) -> None:
        self._builder = builder

    def run_default_callbacks(self) -> "ServiceDescriptor": ...


class Host: ...
