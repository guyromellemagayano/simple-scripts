"""Implement the contract in the challenge README. Reference code is separate."""
from tooling.python.contracts import Clock


class SlidingWindowLimiter:

    def __init__(self, limit: int, window_ms: int, clock: Clock):
        raise NotImplementedError('Not implemented: __init__')

    def allow(self, client: str) -> bool:
        raise NotImplementedError('Not implemented: allow')
