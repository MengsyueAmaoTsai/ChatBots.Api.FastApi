from abc import ABC


class ConfigurationSection: ...


class IConfiguration(ABC): ...


class IConfigurationManager(IConfiguration): ...


class ConfigurationManager(IConfigurationManager):
    def __init__(self) -> None:
        self._sources = object
        self._properties = object

    def __getitem__(self, key: str) -> str: ...
