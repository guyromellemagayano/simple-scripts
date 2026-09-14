# 03. Sliding-Window Rate Limiter

Intermediate · Suggested time: 35–45 minutes

Prerequisites: Maps, queues, time boundaries, amortized complexity.

## Problem

Protect a service by limiting each client's accepted requests within a rolling time window.

## Contract

- Construct with positive integer limit and window_ms, and an injected monotonic millisecond clock.
- allow(client) returns true and records the request if fewer than limit accepted requests remain in that client's window.
- The active interval is (now - window_ms, now]. A timestamp exactly one window old is no longer active.
- Rejected requests are not recorded and do not extend the window. Multiple requests at the same millisecond count separately.
- Clients are independent; an empty client string is valid. All operations are single-threaded.
- Target amortized O(1) per request and at most limit active timestamps and O(limit) retained timestamp storage per visited client. Idle-client cleanup is a follow-up.

The function names above use conceptual snake_case. JavaScript/TypeScript and PHP
use camelCase; Go uses exported PascalCase methods. Starter signatures define the
exact language binding. Missing strings are None in Python, null in JavaScript,
TypeScript and PHP, and ("", false) in Go. Mutating void operations have null
fixture results. All inputs satisfy the stated constraints; malformed input
validation is not assessed. Test times and numeric inputs are safe integers.

## Example

Starting configuration: {"limit": 2, "window_ms": 100}; clock defaults to 0 ms.

```text
allow("a") -> true
allow("a") -> true
allow("a") -> false
advance clock by 100 ms
allow("a") -> true
```

## Work on it

1. Choose a starter below. Implement that file without importing reference code.
2. Run the examples, then the full suite from the repository root:

```sh
python3 practice.py test rate-limiter --language python --suite examples
python3 practice.py test rate-limiter --language python
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

- How does this differ from a token bucket or fixed window?
- How would multiple application replicas share a limit atomically?
- Would you fail open or closed if the shared limiter became unavailable?
