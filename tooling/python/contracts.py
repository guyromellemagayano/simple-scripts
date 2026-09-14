"""Structural ports for the dispatcher; these contain no implementations."""
from collections.abc import Callable
from typing import Protocol, TypedDict

Clock = Callable[[], int]
Sender = Callable[[str], bool]


class Delivery(TypedDict):
    job_id: str
    payload: str
    attempt: int
    receipt: str


class KeyValueStore(Protocol):
    def put(self, key: str, value: str, ttl_ms: int) -> None: ...
    def get(self, key: str) -> str | None: ...


class JobQueuePort(Protocol):
    def enqueue(self, payload: str) -> str: ...
    def reserve(self) -> Delivery | None: ...
    def ack(self, receipt: str) -> bool: ...
    def nack(self, receipt: str) -> bool: ...
