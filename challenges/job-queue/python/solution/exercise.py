"""Reference: ready FIFO and expiring, single-use delivery receipts."""
from collections import deque

from tooling.python.contracts import Clock, Delivery


class JobQueue:
    def __init__(self, visibility_ms: int, max_attempts: int, clock: Clock):
        self._visibility_ms = visibility_ms
        self._max_attempts = max_attempts
        self._clock = clock
        self._ready: deque[dict] = deque()
        self._active: dict[str, tuple[dict, int, int]] = {}
        self._dead: list[dict] = []
        self._next_job = 1
        self._next_lease = 1

    def _fail(self, job: dict) -> None:
        if job["attempts"] >= self._max_attempts:
            self._dead.append(dict(job))
        else:
            self._ready.append(job)

    def _refresh(self) -> None:
        now = self._clock()
        expired = sorted(
            ((deadline, sequence, receipt) for receipt, (_, deadline, sequence)
             in self._active.items() if deadline <= now)
        )
        for _, _, receipt in expired:
            job, _, _ = self._active.pop(receipt)
            self._fail(job)

    def enqueue(self, payload: str) -> str:
        self._refresh()
        job_id = f"job-{self._next_job}"
        self._next_job += 1
        self._ready.append({"job_id": job_id, "payload": payload, "attempts": 0})
        return job_id

    def reserve(self) -> Delivery | None:
        self._refresh()
        if not self._ready:
            return None
        job = self._ready.popleft()
        job["attempts"] += 1
        sequence = self._next_lease
        self._next_lease += 1
        receipt = f"lease-{sequence}"
        self._active[receipt] = (job, self._clock() + self._visibility_ms, sequence)
        return {"job_id": job["job_id"], "payload": job["payload"],
                "attempt": job["attempts"], "receipt": receipt}

    def ack(self, receipt: str) -> bool:
        self._refresh()
        return self._active.pop(receipt, None) is not None

    def nack(self, receipt: str) -> bool:
        self._refresh()
        lease = self._active.pop(receipt, None)
        if lease is None:
            return False
        self._fail(lease[0])
        return True

    def dead_letters(self) -> list[dict]:
        self._refresh()
        return [dict(job) for job in self._dead]
