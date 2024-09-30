import os
from argparse import ArgumentParser
from typing import Optional

import uvicorn
from fastapi import FastAPI

from configuration import ConfigurationManager
from dependency_injection import ServiceCollection, ServiceDescriptor
from hosting import BootstrapHostBuilder, HostApplicationBuilder, HostApplicationBuilderSettings

from .WebApplicationOptions import WebApplicationOptions


class WebApplicationBuilder:
    def __init__(self, options: WebApplicationOptions):
        self._built_application: Optional[WebApplication] = None

        configuration = ConfigurationManager()

        self._host_application_builder = HostApplicationBuilder(HostApplicationBuilderSettings())

        if options.web_root_path is not None:
            pass

        bootstrap_host_builder = BootstrapHostBuilder(self._host_application_builder)

        # if configure_defaults is not None:

        # bootstrap_host_builder.configure_web_host_defaults()

        self._generic_web_host_service_descriptor = self.initialize_hosting(bootstrap_host_builder)

    @property
    def environment(self) -> object:
        raise NotImplementedError()

    @property
    def services(self) -> ServiceCollection:
        return self._host_application_builder.services

    @property
    def configuration(self) -> ConfigurationManager:
        raise NotImplementedError()

    @property
    def logging(self) -> object:
        raise NotImplementedError()

    @property
    def metrics(self) -> object:
        raise NotImplementedError()

    @property
    def web_host(self) -> object:
        raise NotImplementedError()

    @property
    def host(self) -> object:
        raise NotImplementedError()

    def build(self) -> "WebApplication":
        self._host_application_builder.services.add(self._generic_web_host_service_descriptor)
        self._built_application = WebApplication(self._host_application_builder.build())
        return self._built_application

    def initialize_hosting(self, builder: BootstrapHostBuilder) -> ServiceDescriptor:
        generic_web_host_service_descriptor = builder.run_default_callbacks()

        # web_host_context =
        # self._environment = web_host_context.hosting_environment

        return generic_web_host_service_descriptor


class WebApplication:
    def __init__(self, host: object) -> None:
        self._host = host
        self._asgi_app = FastAPI()

    @property
    def asgi_app(self) -> FastAPI:
        return self._asgi_app

    @staticmethod
    def create_builder() -> WebApplicationBuilder:
        builder = WebApplicationBuilder(WebApplicationOptions())
        return builder

    def run(self) -> None:
        parser = ArgumentParser()
        parser.add_argument("--host", default="127.0.0.1", type=str)
        parser.add_argument("--port", default=10004, type=int)
        parser.add_argument("--watch", action="store_true")
        parser.add_argument("--environment", default="Development", type=str)

        parsed_args = parser.parse_args()
        content_root_path = os.getcwd()

        print(f"Now listening on: http://{parsed_args.host}:{parsed_args.port}")
        print("Application started. Press Ctrl+C to shut down.")
        print(f"Hosting environment: {parsed_args.environment}")
        print(f"Content root path: {content_root_path}")

        uvicorn.run(
            "main:app.asgi_app",
            host=parsed_args.host,
            port=parsed_args.port,
            reload=parsed_args.watch,
            log_level="debug",
            access_log=True,
            use_colors=True,
            workers=4,
        )
