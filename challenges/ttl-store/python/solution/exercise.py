"""Reference: lazy expiration with an injected clock."""
from tooling.python.contracts import Clock


class TTLStore:
    def __init__(self, clock: Clock):
        self._clock = clock
        self._entries: dict[str, tuple[str, int]] = {}

    def put(self, key: str, value: str, ttl_ms: int) -> None:
        self._entries[key] = (value, self._clock() + ttl_ms)

    def get(self, key: str) -> str | None:
        entry = self._entries.get(key)
        if entry is None:
            return None
        value, deadline = entry
        if self._clock() >= deadline:
            del self._entries[key]
            return None
        return value

    def delete(self, key: str) -> bool:
        if self.get(key) is None:
            return False
        del self._entries[key]
        return True
