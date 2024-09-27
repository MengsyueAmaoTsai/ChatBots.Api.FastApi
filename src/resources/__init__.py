import httpx

from .contracts import SignalResponse


class ResourceService:
    """"""

    async def list_signals(self) -> list[SignalResponse]:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get("https://localhost:10000/api/v1/signals")

            print(f"Response: {response.json()}")

            return [SignalResponse(**signal) for signal in response.json()]
