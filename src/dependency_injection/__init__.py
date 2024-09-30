from enum import Enum


class ServiceLifetime(Enum):
    Singleton = 1
    Scoped = 2
    Transient = 3


class ServiceDescriptor: ...


class ServiceCollection:
    def add(self, descriptor: ServiceDescriptor) -> "ServiceCollection":
        return self


class ServiceProvider: ...
