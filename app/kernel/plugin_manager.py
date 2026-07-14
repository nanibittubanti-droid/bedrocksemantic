from typing import Any


class PluginManager:
    def __init__(self) -> None:
        self.plugins: dict[str, Any] = {}

    def register(self, name: str, plugin: Any) -> None:
        self.plugins[name] = plugin

    def get(self, name: str) -> Any:
        return self.plugins.get(name)
