from abc import ABC


class Endpoint(ABC): ...


class LineMessagingEndpoint(Endpoint):
    def __init__(self) -> None:
        super().__init__()
