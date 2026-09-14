"""Reference: ordered hash-map recency."""
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        self._capacity = capacity
        self._entries: OrderedDict[str, str] = OrderedDict()

    def get(self, key: str) -> str | None:
        if key not in self._entries:
            return None
        self._entries.move_to_end(key)
        return self._entries[key]

    def put(self, key: str, value: str) -> None:
        self._entries[key] = value
        self._entries.move_to_end(key)
        if len(self._entries) > self._capacity:
            self._entries.popitem(last=False)
