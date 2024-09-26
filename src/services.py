from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhook import WebhookParser
from linebot.v3.webhooks import MessageEvent, TextMessageContent


class LineMessagingService:
    def __init__(self):
        self.configuration = Configuration(
            access_token="MpUtsRPDJZJFf97uu2Xeby8F0aH0IQw6wPd8ovdmAUMoqPGX8IOcZaiixNCY5scbQCkAKf6qh3r+wII3ry1VojhZHxFj0ZcstUZq/52tKILB8GA4eQB+Q5+GjM2k+aBn8fDU5eUS7ykZhBQwjC3WfQdB04t89/1O/w1cDnyilFU="
        )
        self.api_client = AsyncApiClient(self.configuration)
        self.messaging_api = AsyncMessagingApi(self.api_client)
        self.webhook_parser = WebhookParser("059dc70ee4cae01e3df05ac5813ed971")

    async def reply(self, reply_token: str, message: str) -> bool:
        try:
            await self.messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[TextMessage(text=message)],
                )
            )
            return True

        except Exception as e:
            print("Error: ", e)
            return False

        return True
