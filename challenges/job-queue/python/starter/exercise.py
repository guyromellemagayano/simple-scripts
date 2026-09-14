"""Implement the contract in the challenge README. Reference code is separate."""
from tooling.python.contracts import Clock, Delivery


class JobQueue:

    def __init__(self, visibility_ms: int, max_attempts: int, clock: Clock):
        raise NotImplementedError('Not implemented: __init__')

    def enqueue(self, payload: str) -> str:
        raise NotImplementedError('Not implemented: enqueue')

    def reserve(self) -> Delivery | None:
        raise NotImplementedError('Not implemented: reserve')

    def ack(self, receipt: str) -> bool:
        raise NotImplementedError('Not implemented: ack')

    def nack(self, receipt: str) -> bool:
        raise NotImplementedError('Not implemented: nack')

    def dead_letters(self) -> list[dict]:
        raise NotImplementedError('Not implemented: dead_letters')
