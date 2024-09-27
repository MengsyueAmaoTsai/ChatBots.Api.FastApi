from fastapi import APIRouter

from contracts import ApiRoutes, LineMessagingRequest
from infrastructure.resources import ResourceService
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

        self.__resource_service = ResourceService()

    async def send_line_command(self, request: LineMessagingRequest):
        for event in request.events:
            if event.message.text.strip().startswith("signals list"):
                reply_message = await self.get_signals_reply_message()
                await self.__messaging_service.send_reply_message(
                    reply_token=event.reply_token, message=reply_message
                )

        return {
            "message": "OK",
            "status": 200,
        }

    async def get_signals_reply_message(self) -> str:
        signals = await self.__resource_service.list_signals()
        signals = sorted(signals, key=lambda x: x.created_time_utc, reverse=True)
        signals = signals[:3]
        reply_message = "Signals list:\n"

        for signal in signals:
            reply_message += f"[{signal.time}] {signal.source_id} {signal.origin} {signal.trade_type} {signal.quantity} {signal.symbol} @ {signal.latency}\n"

        return reply_message
