from .ServiceLifetime import ServiceLifetime


class ServiceDescriptor:
    """ServiceDescriptor class"""

    def __init__(self, service_type: type, implementation_type: type, lifetime: ServiceLifetime) -> None:
        self.service_type = service_type
        self.implementation_type = implementation_type
        self.lifetime = lifetime
