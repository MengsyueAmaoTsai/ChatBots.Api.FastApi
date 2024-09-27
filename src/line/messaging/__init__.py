import httpx


class LineMessagingClient:
    """"""

    BASE_ADDRESS = "https://api.line.me"

    def __init__(self, channel_access_token: str, channel_secret: str) -> None:
        self.channel_access_token = channel_access_token
        self.channel_secret = channel_secret

    async def send_reply_message(self, reply_token: str, message: str) -> None:
        """"""
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(
                f"{self.BASE_ADDRESS}/v2/bot/message/reply",
                headers={"Authorization": f"Bearer {self.channel_access_token}"},
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
