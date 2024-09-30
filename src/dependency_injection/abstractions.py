from abc import ABC, abstractmethod


class IServiceProvider(ABC):
    @abstractmethod
    def get_required_service[TImplementation](self, service_type: type[TImplementation]) -> TImplementation:
        pass
