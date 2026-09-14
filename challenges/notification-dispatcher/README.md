# 06. Idempotent Notification Dispatcher

Capstone · Suggested time: 60–75 minutes

Prerequisites: Dependency injection, interface composition, idempotency and delivery failures.

## Problem

Compose an idempotency store, a job queue, and a sender into a notification service. Supplied doubles make this exercise independent of the previous solutions.

## Contract

- Construct with a KeyValueStore, JobQueuePort, sender, and positive idempotency_ttl_ms. Read the supplied port definitions and starter signatures for your language.
- submit(key, message) returns a job ID. A live idempotency key returns its original job ID without enqueueing again, changing the original message, or extending the TTL.
- For a new or expired key, enqueue the message, then store the returned job ID for idempotency_ttl_ms. Idempotency persists after delivery until its TTL expires.
- process_one() reserves at most one job. Return 'idle' if none is ready. Call the sender exactly once for a reserved payload.
- If the sender succeeds, acknowledge that receipt and return 'sent'. If it returns false or throws an ordinary exception, negatively acknowledge and return 'failed'. Go represents sender failure with a non-nil error, not a panic.
- Do not retry in a loop: the queue owns retry ordering and exhaustion. The sender is synchronous and does not advance the clock; the receipt remains valid during a call.
- Tests supply a fake TTL store, synchronous retry queue, and scripted sender. sent_messages, send_attempts, and dead_letters are fixture observations, not dispatcher methods you must implement.
- Store/queue calls succeed in this exercise. Single-threaded submit is sufficient; atomic submission and crash consistency are follow-up design questions.

The function names above use conceptual snake_case. JavaScript/TypeScript and PHP
use camelCase; Go uses exported PascalCase methods. Starter signatures define the
exact language binding. Missing strings are None in Python, null in JavaScript,
TypeScript and PHP, and ("", false) in Go. Mutating void operations have null
fixture results. All inputs satisfy the stated constraints; malformed input
validation is not assessed. Test times and numeric inputs are safe integers.

## Example

Starting configuration: {"idempotency_ttl_ms": 100, "max_attempts": 3}; clock defaults to 0 ms.

```text
submit("request-1", "hello") -> "job-1"
submit("request-1", "changed") -> "job-1"
process_one() -> "sent"
process_one() -> "idle"
sent_messages() -> ["hello"]
```

## Work on it

1. Choose a starter below. Implement that file without importing reference code.
2. Run the examples, then the full suite from the repository root:

```sh
python3 practice.py test notification-dispatcher --language python --suite examples
python3 practice.py test notification-dispatcher --language python
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

- What crash window exists between enqueue and storing the idempotency key?
- How could an outbox and a transactional database address that window?
- What happens if sending succeeds but acknowledging fails? Where must downstream idempotency live?
