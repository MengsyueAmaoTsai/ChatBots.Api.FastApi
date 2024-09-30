from enum import Enum


class ServiceLifetime(Enum):
    Singleton = 1
    Scoped = 2
    Transient = 3
