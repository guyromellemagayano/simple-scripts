"""Reference: compose ports without owning their storage or retry policy."""
from tooling.python.contracts import JobQueuePort, KeyValueStore, Sender


class NotificationDispatcher:
    def __init__(self, store: KeyValueStore, queue: JobQueuePort,
                 sender: Sender, idempotency_ttl_ms: int):
        self._store = store
        self._queue = queue
        self._sender = sender
        self._ttl_ms = idempotency_ttl_ms

    def submit(self, key: str, message: str) -> str:
        existing = self._store.get(key)
        if existing is not None:
            return existing
        job_id = self._queue.enqueue(message)
        self._store.put(key, job_id, self._ttl_ms)
        return job_id

    def process_one(self) -> str:
        delivery = self._queue.reserve()
        if delivery is None:
            return "idle"
        try:
            success = self._sender(delivery["payload"])
        except Exception:  # noqa: BLE001 -- Any ordinary sender exception must trigger a retry.
            success = False
        if success:
            self._queue.ack(delivery["receipt"])
            return "sent"
        self._queue.nack(delivery["receipt"])
        return "failed"
