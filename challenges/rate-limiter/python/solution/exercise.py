"""Reference: one accepted-timestamp deque per client."""
from collections import deque

from tooling.python.contracts import Clock


class SlidingWindowLimiter:
    def __init__(self, limit: int, window_ms: int, clock: Clock):
        self._limit = limit
        self._window_ms = window_ms
        self._clock = clock
        self._requests: dict[str, deque[int]] = {}

    def allow(self, client: str) -> bool:
        now = self._clock()
        timestamps = self._requests.setdefault(client, deque())
        while timestamps and timestamps[0] <= now - self._window_ms:
            timestamps.popleft()
        if len(timestamps) >= self._limit:
            return False
        timestamps.append(now)
        return True
