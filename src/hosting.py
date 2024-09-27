import logging
import os
from argparse import ArgumentParser

import uvicorn
from fastapi import FastAPI

from dependency_injections import ServiceCollection
from dependency_injections.abstractions import IServiceCollection, IServiceProvider
from endpoints import LineMessagingEndpoint
from middlewares import RequestDebuggingMiddleware
from open_api import OpenApiConstants

logging.basicConfig(
    format=f"[%(asctime)s %(levelname)s] {__name__} - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


class WebApplication:
    def __init__(self, service_provider: IServiceProvider):
        self._asgi_app = FastAPI(
            title=OpenApiConstants.TITLE,
            description=OpenApiConstants.DESCRIPTION,
            version=OpenApiConstants.VERSION,
            contact=OpenApiConstants.CONTACT,
            openapi_url=OpenApiConstants.SCHEMA_URL,
            docs_url=OpenApiConstants.URL,
        )
        self._service_provider = service_provider

    @property
    def asgi_app(self):
        return self._asgi_app

    @property
    def services(self) -> IServiceProvider:
        return self._service_provider

    @staticmethod
    def create_builder():
        return WebApplicationBuilder()

    def run(self):
        parser = ArgumentParser()
        parser.add_argument("--host", default="127.0.0.1", type=str)
        parser.add_argument("--port", default=10004, type=int)
        parser.add_argument("--watch", action="store_true")
        parser.add_argument("--environment", default="Development", type=str)

        parsed_args = parser.parse_args()
        content_root_path = os.getcwd()

        logger.info(f"Now listening on: http://{parsed_args.host}:{parsed_args.port}")
        logger.info("Application started. Press Ctrl+C to shut down.")
        logger.info(f"Hosting environment: {parsed_args.environment}")
        logger.info(f"Content root path: {content_root_path}")

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

    def use_request_debugging(self):
        self._asgi_app.add_middleware(RequestDebuggingMiddleware)

    def map_endpoints(self):
        endpoint_types = [LineMessagingEndpoint]

        for type in endpoint_types:
            instance = self._service_provider.get_required_service(type)
            print("Mapping endpoint:", instance.__class__.__name__)
            self._asgi_app.include_router(instance.router)


class WebApplicationBuilder:
    def __init__(self):
        self._service_collection = ServiceCollection()

    @property
    def services(self) -> IServiceCollection:
        return self._service_collection

    def build(self):
        provider = self._service_collection.build_service_provider()

        web_app = WebApplication(provider)
        return web_app
