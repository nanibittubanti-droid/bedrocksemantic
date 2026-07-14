from typing import Any


class MemoryStore:
    def __init__(self) -> None:
        self.store: dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self.store[key] = value

    def get(self, key: str) -> Any:
        return self.store.get(key)
