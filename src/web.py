from argparse import ArgumentParser

import uvicorn
from fastapi import FastAPI


class WebApplication:
    def __init__(self):
        self.__app = FastAPI()

    @staticmethod
    def create_builder():
        return WebApplicationBuilder()

    def run(self):
        parser = ArgumentParser()
        parser.add_argument("--host", default="127.0.0.1", type=str)
        parser.add_argument("--port", default=10002, type=int)
        parser.add_argument("--watch", action="store_true")
        parser.add_argument("--environment", default="development", type=str)

        parsed_args = parser.parse_args()

        uvicorn.run(
            "main:app",
            host=parsed_args.host,
            port=parsed_args.port,
            reload=parsed_args.watch,
            log_level="debug",
            access_log=True,
            use_colors=True,
            workers=4,
        )


class WebApplicationBuilder:
    def __init__(self):
        pass

    def build(self):
        web_app = WebApplication()
        return web_app
