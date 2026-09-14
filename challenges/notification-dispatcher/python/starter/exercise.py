"""Implement the contract in the challenge README. Reference code is separate."""
from tooling.python.contracts import JobQueuePort, KeyValueStore, Sender

class NotificationDispatcher:

    def __init__(self, store: KeyValueStore, queue: JobQueuePort, sender: Sender, idempotency_ttl_ms: int):
        raise NotImplementedError('Not implemented: __init__')

    def submit(self, key: str, message: str) -> str:
        raise NotImplementedError('Not implemented: submit')

    def process_one(self) -> str:
        raise NotImplementedError('Not implemented: process_one')
