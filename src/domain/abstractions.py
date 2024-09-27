from typing import Protocol

from shared_kernel import Result


class ILineBotService(Protocol):
    async def reply_text_message(self, reply_token: str, text_message: str) -> Result:
        raise NotImplementedError()
