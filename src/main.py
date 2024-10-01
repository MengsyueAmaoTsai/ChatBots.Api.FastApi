from typing import Callable

from dependency_injection import ServiceProvider


class IMyService:
    """"""


class MyService(IMyService):
    pass


class IOtherService:
    """"""


class OtherService(IOtherService):
    pass


provider = ServiceProvider()

service = provider.get_required_service(IMyService)

print(f"Get service from container: {service}")
