from dependency_injection import (
    ServiceCollection,
    ServiceProvider,
    ServiceProviderOptions,
)


class IMyService:
    """"""


class MyService(IMyService):
    pass


class IOtherService:
    """"""


class OtherService(IOtherService):
    pass


services = ServiceCollection()
services.make_read_only()
print(services.length)


provider = ServiceProvider(services, ServiceProviderOptions())

service = provider.get_required_service(IMyService)

print(f"Get service from container: {service}")
