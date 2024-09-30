class HostApplicationBuilderSettings: ...


class HostApplicationBuilder:
    def __init__(self, settings: HostApplicationBuilderSettings) -> None:
        pass


class BootstrapHostBuilder:
    def __init__(self, builder: HostApplicationBuilder) -> None:
        self._builder = builder
