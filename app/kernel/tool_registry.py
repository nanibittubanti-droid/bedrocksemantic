from typing import Any


class ToolRegistry:
    def __init__(self) -> None:
        self.tools: dict[str, Any] = {}

    def register(self, name: str, tool: Any) -> None:
        self.tools[name] = tool

    def get(self, name: str) -> Any:
        return self.tools.get(name)
