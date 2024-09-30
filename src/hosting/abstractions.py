from abc import ABC

from dependency_injection import ServiceProvider


class IHost(ABC):
    @property
    def services(self) -> ServiceProvider: ...

    async def start(self) -> None: ...
    async def stop(self) -> None: ...
