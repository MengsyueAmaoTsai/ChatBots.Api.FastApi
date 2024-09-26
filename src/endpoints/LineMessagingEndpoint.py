from fastapi import APIRouter

from contracts import ApiRoutes, SendReplyMessageRequest
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

    async def send_line_command(self, request: SendReplyMessageRequest):
        """"""
        for event in request.events:
            text = event.message.text
            reply_token = event.reply_token
            user_id = event.source.user_id
            print(f"Received message from user: {user_id} - {text}")
            await self.__messaging_service.send_reply_message(reply_token, text)
