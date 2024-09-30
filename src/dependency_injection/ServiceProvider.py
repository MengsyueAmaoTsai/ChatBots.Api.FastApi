from .abstractions import IServiceProvider
from .ServiceDescriptor import ServiceDescriptor


class ServiceProvider(IServiceProvider):
    def __init__(self, descriptors: list[ServiceDescriptor]) -> None: ...
    def get_required_service[TImplementation](self, service_type: type[TImplementation]) -> TImplementation: ...
