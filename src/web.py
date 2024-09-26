import logging
import os
from argparse import ArgumentParser

import uvicorn
from fastapi import FastAPI

from endpoints import LineMessagingEndpoint

logging.basicConfig(
    format=f"[%(asctime)s %(levelname)s] {__name__} - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


class WebApplication:
    def __init__(self):
        self.__app = FastAPI()

    @property
    def app(self):
        return self.__app

    @staticmethod
    def create_builder():
        return WebApplicationBuilder()

    def run(self):
        parser = ArgumentParser()
        parser.add_argument("--host", default="127.0.0.1", type=str)
        parser.add_argument("--port", default=10002, type=int)
        parser.add_argument("--watch", action="store_true")
        parser.add_argument("--environment", default="Development", type=str)

        parsed_args = parser.parse_args()
        content_root_path = os.getcwd()

        logger.info(f"Now listening on: http://{parsed_args.host}:{parsed_args.port}")
        logger.info("Application started. Press Ctrl+C to shut down.")
        logger.info(f"Hosting environment: {parsed_args.environment}")
        logger.info(f"Content root path: {content_root_path}")

        uvicorn.run(
            "main:app.app",
            host=parsed_args.host,
            port=parsed_args.port,
            reload=parsed_args.watch,
            log_level="debug",
            access_log=True,
            use_colors=True,
            workers=4,
        )

    def map_endpoints(self):
        endpoints = [LineMessagingEndpoint()]

        for endpoint in endpoints:
            self.__app.include_router(endpoint.router)


class WebApplicationBuilder:
    def __init__(self):
        pass

    def build(self):
        web_app = WebApplication()
        return web_app
