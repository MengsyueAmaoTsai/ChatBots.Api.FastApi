from assertpy import assert_that

from dependency_injection import ServiceCollection, ServiceCollectionReadOnlyException, ServiceDescriptor


class IFakeService: ...


class IFakeEveryService: ...


class FakeService(IFakeService, IFakeEveryService): ...


class ServiceCollectionTests:
    def test_service_collection(self) -> None:
        services = ServiceCollection()
        descriptor = ServiceDescriptor(type(IFakeService), FakeService())

        services.append(descriptor)

        services.make_read_only()

        descriptor2 = ServiceDescriptor(type(IFakeEveryService), FakeService())

        assert_that(services.append).raises(ServiceCollectionReadOnlyException).when_called_with(descriptor2)
        assert_that(services.clear).raises(ServiceCollectionReadOnlyException)
        assert_that(services.remove).raises(ServiceCollectionReadOnlyException).when_called_with(descriptor)
        assert_that(services.remove_at).raises(ServiceCollectionReadOnlyException)
        assert_that(services.insert).raises(ServiceCollectionReadOnlyException)
        assert_that(services.clear).raises(ServiceCollectionReadOnlyException)

        assert_that(services.length).is_equal_to(1)
        assert_that(services[0]).is_equal_to(descriptor)
