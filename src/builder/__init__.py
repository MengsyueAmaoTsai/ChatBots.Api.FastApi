from abc import ABC
from dataclasses import dataclass
from typing import Any, Callable, Optional, overload

from configuration import ConfigurationManager
from hosting import HostApplicationBuilder, HostApplicationBuilderSettings


@dataclass()
class WebApplicationOptions:
    args: Optional[list[str]] = None
    application_name: Optional[str] = None
    environment_name: Optional[str] = None
    content_root_path: Optional[str] = None


class IHostBuilder(ABC):
    pass


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
        print("ConfigurationManager", configuration)

        self._host_application_builder = HostApplicationBuilder(
            HostApplicationBuilderSettings(
                args=options.args,
                application_name=options.application_name,
                environment_name=options.environment_name,
                content_root_path=options.content_root_path,
                configuration=configuration,
            )
        )


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
    def create_builder(*args: list[str] | WebApplicationOptions, **kwargs: Any) -> WebApplicationBuilder:
        if len(args) == 0:
            return WebApplicationBuilder(WebApplicationOptions())

        if len(args) == 1 and isinstance(args[0], list):
            arguments = args[0]
            return WebApplicationBuilder(WebApplicationOptions(args=arguments), configure_defaults=None)

        if len(args) == 1 and isinstance(args[0], WebApplicationOptions):
            options = args[0]
            return WebApplicationBuilder(options, configure_defaults=None)

        raise ValueError("Invalid arguments")
