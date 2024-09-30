from abc import ABC
from typing import Any

from fastapi import APIRouter

type ActionResultBase = Any
type ActionResult[TResponse] = ActionResultBase | TResponse


class Endpoint(ABC): ...


class LineMessagingEndpoint(Endpoint):
    def __init__(self) -> None:
        super().__init__()
        self._router = APIRouter()
        self._router.add_api_route(
            path="api/v1/line-messaging", endpoint=self.handle, methods=["POST"], tags=["LineMessaging"]
        )

    async def handle(self, request: object) -> ActionResult[object]:
        return object()
