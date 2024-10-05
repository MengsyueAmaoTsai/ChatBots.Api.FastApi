from typing import Optional

from configuration.abstractions import IConfigurationSource

from .abstractions import IConfigurationBuilder, IConfigurationProvider, IConfigurationRoot, IConfigurationSection


class MemoryConfigurationSource(IConfigurationSource):
    def __init__(self, initial_data: dict[str, Optional[str]]) -> None:
        self.initial_data = initial_data

    def build(self, builder: IConfigurationBuilder) -> IConfigurationProvider:
        return MemoryConfigurationProvider(self)


class ConfigurationProvider(IConfigurationProvider):
    def __init__(self) -> None:
        self.data: dict[str, Optional[str]] = {}

    def try_get(self, key: str) -> str | None:
        return self.data.get(key)

    def set(self, key: str, value: str | None) -> None:
        self.data[key] = value

    def load(self) -> None: ...

    def get_child_keys(self, earlier_keys: list[str], parent_path: str | None) -> list[str]:
        results: list[str] = []
        if parent_path is None:
            results.extend([self.__segment(k, 0) for k in self.data.keys()])
        else:
            for key in self.data.keys():
                if len(key) > len(parent_path) and key.startswith(parent_path) and key[len(parent_path)] == ":":
                    results.append(self.__segment(key, len(parent_path) + 1))

        results.extend(earlier_keys)
        results.sort()
        return results

    def __repr__(self) -> str:
        return self.__class__.__name__

    def __segment(self, key: str, prefix_length: int) -> str:
        index_of = key.index(":", prefix_length)

        if index_of == -1:
            return key[prefix_length:]

        return key[prefix_length:index_of]


class MemoryConfigurationProvider(ConfigurationProvider):
    def __init__(self, source: MemoryConfigurationSource) -> None:
        super().__init__()
        self._source = source

        if self._source.initial_data is not None:  # type: ignore
            for key, value in self._source.initial_data.items():
                self.data[key] = value


class ConfigurationSection(IConfigurationSection):
    def __init__(self, root: IConfigurationRoot, path: str) -> None:
        self._root = root
        self._path = path


class ConfigurationRoot(IConfigurationRoot):
    def __init__(self, providers: list[IConfigurationProvider]) -> None:
        self._providers: list[IConfigurationProvider] = providers

        for provider in providers:
            provider.load()

    def __getitem__(self, key: str) -> Optional[str]:
        return self._get_configuration(self._providers, key)

    def get_section(self, key: str) -> IConfigurationSection:
        raise NotImplementedError

    def get_children(self) -> list[IConfigurationSection]:
        raise NotImplementedError

    @property
    def providers(self) -> list[IConfigurationProvider]:
        raise NotImplementedError

    def reload(self) -> None:
        raise NotImplementedError

    def _get_configuration(self, providers: list[IConfigurationProvider], key: str) -> Optional[str]:
        for provider in providers:
            value = provider.try_get(key)
            if value is not None:
                return value

        return None


class ConfigurationBuilder(IConfigurationBuilder):
    def __init__(self) -> None:
        self._sources: list[IConfigurationSource] = []

    def add(self, source: IConfigurationSource) -> IConfigurationBuilder:
        self._sources.append(source)
        return self

    def build(self) -> IConfigurationRoot:
        providers = [source.build(self) for source in self._sources]

        return ConfigurationRoot(providers)

    @property
    def properties(self) -> dict[str, object]:
        raise NotImplementedError

    @property
    def sources(self) -> list[IConfigurationSource]:
        return self._sources
