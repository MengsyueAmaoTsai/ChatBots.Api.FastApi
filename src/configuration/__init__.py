from configuration.abstractions import IConfigurationSource

from .abstractions import IConfigurationBuilder, IConfigurationProvider, IConfigurationRoot, IConfigurationSection


class ConfigurationSection(IConfigurationSection):
    def __init__(self, root: IConfigurationRoot, path: str) -> None:
        self._root = root
        self._path = path


class ConfigurationRoot(IConfigurationRoot):
    def __init__(self, providers: list[IConfigurationProvider]) -> None:
        self._providers = providers

        for provider in providers:
            provider.load()

    def __getitem__(self, key: str) -> str:
        raise NotImplementedError

    def get_section(self, key: str) -> IConfigurationSection:
        raise NotImplementedError

    def get_children(self) -> list[IConfigurationSection]:
        raise NotImplementedError

    @property
    def providers(self) -> list[IConfigurationProvider]:
        raise NotImplementedError

    def reload(self) -> None:
        raise NotImplementedError


class ConfigurationBuilder(IConfigurationBuilder):
    def __init__(self) -> None:
        self._sources: list[IConfigurationSource] = []

    def add(self, source: IConfigurationSource) -> IConfigurationBuilder:
        self._sources.append(source)
        return self

    def build(self) -> IConfigurationRoot:
        providers = [source.build(self) for source in self._sources]

        return ConfigurationRoot(providers)
