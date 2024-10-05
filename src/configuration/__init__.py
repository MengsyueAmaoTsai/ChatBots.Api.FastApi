from abc import ABC
from typing import Optional


class IConfigurationBuilder(ABC): ...


class IConfiguration(ABC):
    def __getitem__(self, key: str) -> Optional[str]: ...


class ConfigurationManager(IConfiguration): ...
