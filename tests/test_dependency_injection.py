from dependency_injections import ServiceDescriptor, ServiceLifetime


def test_di():
    descriptor = ServiceDescriptor(str, str, ServiceLifetime.Singleton)

    assert descriptor.service_type is str
    assert descriptor.implementation_type is str
    assert descriptor.lifetime is ServiceLifetime.Singleton
