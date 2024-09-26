import httpx


class LineMessagingErrorResponse:
    """"""


class SendReplyMessageRequest:
    """"""


class ReplyMessageSentResponse:
    """"""


class LineMessagingClient:
    """"""

    CHANNEL_ACCESS_TOKEN = "MpUtsRPDJZJFf97uu2Xeby8F0aH0IQw6wPd8ovdmAUMoqPGX8IOcZaiixNCY5scbQCkAKf6qh3r+wII3ry1VojhZHxFj0ZcstUZq/52tKILB8GA4eQB+Q5+GjM2k+aBn8fDU5eUS7ykZhBQwjC3WfQdB04t89/1O/w1cDnyilFU="
    CHANNEL_SECRET = "059dc70ee4cae01e3df05ac5813ed971"

    async def send_reply_message(self, reply_token: str, message: str) -> None:
        """"""
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(
                "https://api.line.me/v2/bot/message/reply",
                headers={"Authorization": f"Bearer {self.CHANNEL_ACCESS_TOKEN}"},
                json={
                    "replyToken": reply_token,
                    "messages": [{"type": "text", "text": message}],
                },
            )

            if response.status_code >= 400:
                print(f"Error [{response.status_code}]: {response.text}")
                return

            print(f"Success [{response.status_code}]: {response.text}")
            return
