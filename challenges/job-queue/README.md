# 05. Reliable In-Memory Job Queue

Intermediate → advanced · Suggested time: 60–75 minutes

Prerequisites: Queues, state machines, maps, leases and retries.

## Problem

Build a job queue whose workers can reserve work, acknowledge success, or retry failed and abandoned deliveries.

## Contract

- Construct with positive visibility_ms, positive max_attempts, and a monotonic millisecond clock. enqueue(payload) assigns job-1, job-2, ... and appends the string payload to the ready FIFO.
- reserve() returns null/None/nil if empty; otherwise it removes the oldest ready job and returns {job_id, payload, attempt, receipt}. Attempts start at 1 and increase on each reservation. Receipts are globally increasing lease-1, lease-2, ... per queue.
- A receipt is active until clock() >= its reservation time + visibility_ms. ack(receipt) completes an active delivery; nack(receipt) fails it. Both return false for unknown, expired, or previously consumed receipts.
- A failed or expired delivery is appended to the ready FIFO unless its attempt count has reached max_attempts, in which case it enters the dead-letter list. Retries preserve the job ID and receive a new receipt.
- Before EVERY public operation, process expired receipts in ascending (deadline, numeric lease sequence) order. Append retries behind already-ready jobs. A nack at the exact expiry boundary returns false because expiration has already processed it.
- dead_letters() returns ordered snapshots of {job_id, payload, attempts}, in the order jobs exhausted their attempts. Acknowledged jobs are never redelivered.
- Keep this implementation single-threaded. A scan of active leases is acceptable: discuss its O(L log L) worst-case sorting cost and how a deadline heap would improve it.

The function names above use conceptual snake_case. JavaScript/TypeScript and PHP
use camelCase; Go uses exported PascalCase methods. Starter signatures define the
exact language binding. Missing strings are None in Python, null in JavaScript,
TypeScript and PHP, and ("", false) in Go. Mutating void operations have null
fixture results. All inputs satisfy the stated constraints; malformed input
validation is not assessed. Test times and numeric inputs are safe integers.

## Example

Starting configuration: {"visibility_ms": 100, "max_attempts": 3}; clock defaults to 0 ms.

```text
enqueue("email") -> "job-1"
reserve() -> {"job_id": "job-1", "payload": "email", "attempt": 1, "receipt": "lease-1"}
ack("lease-1") -> true
reserve() -> null
dead_letters() -> []
```

## Work on it

1. Choose a starter below. Implement that file without importing reference code.
2. Run the examples, then the full suite from the repository root:

```sh
python3 practice.py test job-queue --language python --suite examples
python3 practice.py test job-queue --language python
```

Replace python with javascript, typescript, go, or php. The default target is
starter. Change only your selected starter; every case constructs a fresh instance.

- [Python starter](python/starter/) · [Python reference](python/solution/)
- [JavaScript starter](javascript/starter/) · [JavaScript reference](javascript/solution/)
- [TypeScript starter](typescript/starter/) · [TypeScript reference](typescript/solution/)
- [Go starter](go/starter/) · [Go reference](go/solution/)
- [PHP starter](php/starter/) · [PHP reference](php/solution/)

[Progressive hints](HINTS.md) · [Reference explanation](SOLUTION.md) ·
[Assessment fixture format](../../tooling/README.md)

The full suite is visible in cases.json. Treat it as an assessment: first solve
from the contract, then inspect failing cases. There is no remote or hidden judge.

## Self-review

- Correctness (0–4): examples, boundary cases, and full suite pass.
- Complexity (0–2): explain runtime and retained memory, including cleanup.
- Code clarity (0–2): use idiomatic types, names, and small state transitions.
- Design reasoning (0–2): explain one failure mode and one scaling tradeoff.

A passing suite is necessary; it is not a proof of complexity or production readiness.

## System-design follow-ups

- What must be persisted to survive a process crash?
- Why do visibility timeouts imply at-least-once processing rather than exactly-once side effects?
- How would backoff, a deadline heap, and multiple workers alter the implementation?
