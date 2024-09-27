from fastapi import APIRouter

from contracts import ApiRoutes, LineMessagingRequest

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

    async def send_line_command(self, request: LineMessagingRequest):
        for event in request.events:
            if event.message.text.strip().startswith("/rc "):
                pass
                ## Map event to command

                ## Process command and get result

                ## Map result to reply message

                # await self.__messaging_service.send_reply_message(reply_token=event.reply_token, message=reply_message)

        return {
            "message": "OK",
            "status": 200,
        }
