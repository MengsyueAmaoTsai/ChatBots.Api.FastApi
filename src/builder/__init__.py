import os
from argparse import ArgumentParser

import uvicorn
from fastapi import FastAPI


class WebApplicationBuilder:
    """A builder for web application and services"""

    def build(self) -> "WebApplication":
        app = WebApplication()
        return app


class WebApplication:
    """"""

    def __init__(self) -> None:
        self._asgi_app = FastAPI()

    @property
    def asgi_app(self):
        return self._asgi_app

    @staticmethod
    def create_builder() -> WebApplicationBuilder:
        return WebApplicationBuilder()

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
