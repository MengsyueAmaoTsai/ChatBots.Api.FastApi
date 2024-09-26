import httpx
from fastapi import APIRouter, Request

from contracts import ApiRoutes

from .ApiTags import ApiTags


class LineMessagingEndpoint:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.router.add_api_route(
            path=ApiRoutes.LINE_MESSAGING,
            endpoint=self.send_line_command,
            methods=["POST"],
            response_model=None,
            tags=[ApiTags.LineMessaging],
        )

        ## services
        self.__messaging_service = LineMessagingClient()

    async def send_line_command(self, request: Request):
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get("https://localhost:10000/api/v1/signals")

            json = response.json()
            return json
