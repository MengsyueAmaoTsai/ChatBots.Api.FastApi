from typing import Protocol

from line.messaging import LineMessagingClient
from shared_kernel import Result


class ILineBotService(Protocol):
    async def reply_text_message(self, reply_token: str, text_message: str) -> Result:
        raise NotImplementedError()


class LineBotService(ILineBotService):
    def __init__(self, line_messaging_client: LineMessagingClient) -> None:
        self._messaging_client = line_messaging_client

    async def reply_text_message(self, reply_token: str, text_message: str) -> Result:
        result = await self._messaging_client.send_reply_message(reply_token, text_message)

        if result.is_failure:
            return Result.failure(result.error)

        return Result.success()
