from dataclasses import dataclass
from typing import Any, Callable, Optional, overload

from configuration import ConfigurationManager
from dependency_injection import ServiceDescriptor
from hosting import (
    BootstrapHostBuilder,
    HostApplicationBuilder,
    HostApplicationBuilderSettings,
    IHostBuilder,
    WebHostBuilderContext,
)


@dataclass()
class WebApplicationOptions:
    args: Optional[list[str]] = None
    application_name: Optional[str] = None
    environment_name: Optional[str] = None
    content_root_path: Optional[str] = None
    web_root_path: Optional[str] = None


class WebApplicationBuilder:
    @overload
    def __init__(
        self, options: WebApplicationOptions, configure_defaults: Optional[Callable[[IHostBuilder], None]] = None
    ) -> None: ...

    @overload
    def __init__(
        self,
        options: WebApplicationOptions,
        slim: bool,
        configure_defaults: Optional[Callable[[IHostBuilder], None]] = None,
    ) -> None: ...

    @overload
    def __init__(
        self,
        options: WebApplicationOptions,
        slim: bool,
        empty: bool,
        configure_defaults: Optional[Callable[[IHostBuilder], None]] = None,
    ) -> None: ...

    def __init__(self, options: WebApplicationOptions, *args: Any, **kwargs: Any) -> None:
        configuration = ConfigurationManager()

        self._host_application_builder = HostApplicationBuilder(
            HostApplicationBuilderSettings(
                args=options.args,
                application_name=options.application_name,
                environment_name=options.environment_name,
                content_root_path=options.content_root_path,
                configuration=configuration,
            )
        )

        if options.web_root_path is not None:
            raise NotImplementedError("Web root path is not supported yet")

        bootstrap_host_builder = BootstrapHostBuilder(self._host_application_builder)

        configure_defaults: Optional[Callable[[IHostBuilder], None]] = args[-1]

        if configure_defaults is not None:
            configure_defaults(bootstrap_host_builder)

        # bootstrap_host_builder.configure_web_host_defaults()

        self._generic_web_host_service_descriptor = self.__initialize_hosting(bootstrap_host_builder)

    def __initialize_hosting(self, bootstrap_host_builder: BootstrapHostBuilder) -> ServiceDescriptor:
        descriptor = bootstrap_host_builder.run_default_callbacks()

        web_host_context = bootstrap_host_builder.properties[WebHostBuilderContext]

        print("WebHostBuilderContext: ", web_host_context)
        return descriptor


class WebApplication:
    @overload
    @staticmethod
    def create_builder() -> WebApplicationBuilder: ...

    @overload
    @staticmethod
    def create_builder(args: list[str]) -> WebApplicationBuilder: ...

    @overload
    @staticmethod
    def create_builder(options: WebApplicationOptions) -> WebApplicationBuilder: ...

    @staticmethod
    def create_builder(*args: list[str] | WebApplicationOptions, **_: Any) -> WebApplicationBuilder:
        if len(args) == 0:
            return WebApplicationBuilder(WebApplicationOptions(), None)

        if len(args) == 1 and isinstance(args[0], list):
            arguments = args[0]
            return WebApplicationBuilder(WebApplicationOptions(args=arguments), None)

        if len(args) == 1 and isinstance(args[0], WebApplicationOptions):
            options = args[0]
            return WebApplicationBuilder(options, None)

        raise ValueError("Invalid arguments")
