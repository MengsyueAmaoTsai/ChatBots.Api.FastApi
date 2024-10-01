from dependency_injection import ServiceDescriptor, ServiceProvider


class IMyService:
    """"""


class MyService(IMyService):
    pass


class IOtherService:
    """"""


class OtherService(IOtherService):
    pass


descriptor = ServiceDescriptor()

provider = ServiceProvider([descriptor])

service = provider.get_required_service(IMyService)

print(f"Get service from container: {service}")
