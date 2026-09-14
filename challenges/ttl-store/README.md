# 01. TTL Key-Value Store

Foundation · Suggested time: 20–30 minutes

Prerequisites: Classes, dictionaries/maps, optional return values.

## Problem

Build an in-memory store for temporary session data. Callers must never observe an expired value.

## Contract

- Construct with an injected clock returning integer milliseconds. The clock never moves backward.
- put(key, value, ttl_ms) stores a string and replaces any previous value and expiration. Expiration is clock() + ttl_ms.
- get(key) returns the live string or the language's absent-value result. A value is expired when clock() >= expiration.
- delete(key) returns true only if a live value was removed; missing or expired keys return false.
- Empty strings are valid keys and values. TTL is a positive integer. Operations are single-threaded.
- Target average O(1) work per operation. Lazy expiration is sufficient; background cleanup is a discussion topic.

The function names above use conceptual snake_case. JavaScript/TypeScript and PHP
use camelCase; Go uses exported PascalCase methods. Starter signatures define the
exact language binding. Missing strings are None in Python, null in JavaScript,
TypeScript and PHP, and ("", false) in Go. Mutating void operations have null
fixture results. All inputs satisfy the stated constraints; malformed input
validation is not assessed. Test times and numeric inputs are safe integers.

## Example

Starting configuration: {}; clock defaults to 0 ms.

```text
put("session", "alice", 100) -> null
get("session") -> "alice"
advance clock by 100 ms
get("session") -> null
```

## Work on it

1. Choose a starter below. Implement that file without importing reference code.
2. Run the examples, then the full suite from the repository root:

```sh
python3 practice.py test ttl-store --language python --suite examples
python3 practice.py test ttl-store --language python
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

- How would background expiry change memory usage and latency?
- What clock would a single process use? What changes across machines?
- How would you make compare-and-set or concurrent updates atomic?
