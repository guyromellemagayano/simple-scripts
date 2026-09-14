"""Implement the contract in the challenge README. Reference code is separate."""
from tooling.python.contracts import Clock


class TTLStore:

    def __init__(self, clock: Clock):
        raise NotImplementedError('Not implemented: __init__')

    def put(self, key: str, value: str, ttl_ms: int) -> None:
        raise NotImplementedError('Not implemented: put')

    def get(self, key: str) -> str | None:
        raise NotImplementedError('Not implemented: get')

    def delete(self, key: str) -> bool:
        raise NotImplementedError('Not implemented: delete')
