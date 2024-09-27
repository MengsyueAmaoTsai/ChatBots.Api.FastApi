from enum import Enum


class ServiceLifetime(Enum):
    Singleton = 1
    Transient = 2
    Scoped = 3
