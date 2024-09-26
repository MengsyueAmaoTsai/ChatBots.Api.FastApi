import json

import httpx
from fastapi import APIRouter, Request

from contracts import ApiRoutes
from line import LineMessagingClient

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
        """"""
        ## Get signature from headers
        signature = request.headers["X-Line-Signature"]
        print("Signature: ", signature)

        ## Parse body
        body = await request.body()
        body = body.decode()
        print("Body: ", body)

        data = json.loads(body)

        events = data["events"]

        for event in events:
            text = event["message"]["text"]
            reply_token = event["replyToken"]
            userId = event["source"]["userId"]

            print(f"Received message from user: {userId} - {text}")
            await self.__messaging_service.send_reply_message(reply_token, text)
