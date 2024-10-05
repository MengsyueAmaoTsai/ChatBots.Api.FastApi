from abc import ABC, abstractmethod
from typing import Optional


class IConfiguration(ABC):
    @abstractmethod
    def __getitem__(self, key: str) -> Optional[str]: ...

    @abstractmethod
    def get_section(self, key: str) -> "IConfigurationSection": ...

    @abstractmethod
    def get_children(self) -> list["IConfigurationSection"]: ...


class IConfigurationSource(ABC):
    @abstractmethod
    def build(self, builder: "IConfigurationBuilder") -> "IConfigurationProvider": ...


class IConfigurationBuilder(ABC):
    @property
    @abstractmethod
    def properties(self) -> dict[str, object]: ...

    @property
    @abstractmethod
    def sources(self) -> list[IConfigurationSource]: ...

    @abstractmethod
    def add(self, source: IConfigurationSource) -> "IConfigurationBuilder": ...

    @abstractmethod
    def build(self) -> "IConfigurationRoot": ...


class IConfigurationProvider(ABC):
    @abstractmethod
    def try_get(self, key: str) -> Optional[str]: ...

    @abstractmethod
    def set(self, key: str, value: Optional[str]) -> None: ...

    @abstractmethod
    def load(self) -> None: ...

    @abstractmethod
    def get_child_keys(self, earlier_keys: list[str], parent_path: Optional[str]) -> list[str]: ...


class IConfigurationRoot(IConfiguration):
    @property
    @abstractmethod
    def providers(self) -> list[IConfigurationProvider]: ...

    @abstractmethod
    def reload(self) -> None: ...


class IConfigurationSection(IConfiguration):
    @property
    @abstractmethod
    def key(self) -> str: ...

    @property
    @abstractmethod
    def path(self) -> str: ...

    @property
    @abstractmethod
    def value(self) -> Optional[str]: ...


class IConfigurationManager(IConfiguration, IConfigurationBuilder): ...
