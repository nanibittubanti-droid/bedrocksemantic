from typing import Any


def safe_get(data: dict[str, Any], key: str, default: Any = None) -> Any:
    return data.get(key, default)
