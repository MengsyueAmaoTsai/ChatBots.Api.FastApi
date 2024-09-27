from fastapi import APIRouter

from contracts import ApiRoutes, SendReplyMessageRequest
from line import LineMessagingClient

from .ApiTags import ApiTags


class LineMessagingEndpoint:
    CHANNEL_ACCESS_TOKEN = "MpUtsRPDJZJFf97uu2Xeby8F0aH0IQw6wPd8ovdmAUMoqPGX8IOcZaiixNCY5scbQCkAKf6qh3r+wII3ry1VojhZHxFj0ZcstUZq/52tKILB8GA4eQB+Q5+GjM2k+aBn8fDU5eUS7ykZhBQwjC3WfQdB04t89/1O/w1cDnyilFU="
    CHANNEL_SECRET = "059dc70ee4cae01e3df05ac5813ed971"

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
        self.__messaging_service = LineMessagingClient(
            channel_access_token=self.CHANNEL_ACCESS_TOKEN,
            channel_secret=self.CHANNEL_SECRET,
        )

    async def send_line_command(self, request: SendReplyMessageRequest):
        """"""
        for event in request.events:
            text = event.message.text
            reply_token = event.reply_token
            user_id = event.source.user_id
            print(f"Received message from user: {user_id} - {text}")

            await self.__messaging_service.send_reply_message(reply_token, text)
