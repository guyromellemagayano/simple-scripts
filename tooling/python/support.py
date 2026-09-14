"""Small, synchronous capstone doubles. No earlier exercise is imported."""
from collections import deque


class FakeStore:
    def __init__(self, clock):
        self.clock = clock
        self.entries = {}

    def get(self, key):
        entry = self.entries.get(key)
        return entry[0] if entry is not None and self.clock() < entry[1] else None

    def put(self, key, value, ttl_ms):
        self.entries[key] = (value, self.clock() + ttl_ms)


class FakeQueue:
    """Only synchronous reserve/ack/nack; deliberately no visibility scheduler."""
    def __init__(self, max_attempts):
        self.max_attempts = max_attempts
        self.ready = deque()
        self.active = {}
        self.dead = []
        self.next_job = 1
        self.next_lease = 1

    def enqueue(self, payload):
        job_id = f"job-{self.next_job}"
        self.next_job += 1
        self.ready.append({"job_id": job_id, "payload": payload, "attempts": 0})
        return job_id

    def reserve(self):
        if not self.ready:
            return None
        job = self.ready.popleft()
        job["attempts"] += 1
        receipt = f"lease-{self.next_lease}"
        self.next_lease += 1
        self.active[receipt] = job
        return {"job_id": job["job_id"], "payload": job["payload"],
                "attempt": job["attempts"], "receipt": receipt}

    def ack(self, receipt):
        return self.active.pop(receipt, None) is not None

    def nack(self, receipt):
        job = self.active.pop(receipt, None)
        if job is None:
            return False
        if job["attempts"] >= self.max_attempts:
            self.dead.append(job)
        else:
            self.ready.append(job)
        return True


class FakeSender:
    def __init__(self, outcomes):
        self.outcomes = deque(outcomes)
        self.attempts = []
        self.sent = []

    def __call__(self, message):
        self.attempts.append(message)
        outcome = self.outcomes.popleft() if self.outcomes else "ok"
        if outcome == "raise":
            raise RuntimeError("Scripted sender failure")
        if outcome == "fail":
            return False
        self.sent.append(message)
        return True
