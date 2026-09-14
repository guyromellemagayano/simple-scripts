# 02. LRU Cache

Foundation → intermediate · Suggested time: 30–40 minutes

Prerequisites: Hash maps, linked lists, ordering and amortized complexity.

## Problem

Build a bounded cache that evicts the least recently used item when a new key exceeds capacity.

## Contract

- Construct with a positive integer capacity.
- put(key, value) inserts or overwrites a string and makes that key most recently used.
- get(key) returns a stored string and makes the key most recently used, or returns the absent-value result on a miss.
- A miss must not change recency. Updating an existing key must not evict another key.
- On a new insertion over capacity, evict exactly the least recently used key. Empty strings are valid.
- Target average O(1) get/put and O(capacity) memory. Standard-library ordered containers are allowed; explain their costs.

The function names above use conceptual snake_case. JavaScript/TypeScript and PHP
use camelCase; Go uses exported PascalCase methods. Starter signatures define the
exact language binding. Missing strings are None in Python, null in JavaScript,
TypeScript and PHP, and ("", false) in Go. Mutating void operations have null
fixture results. All inputs satisfy the stated constraints; malformed input
validation is not assessed. Test times and numeric inputs are safe integers.

## Example

Starting configuration: {"capacity": 2}; clock defaults to 0 ms.

```text
put("a", "A") -> null
put("b", "B") -> null
get("a") -> "A"
put("c", "C") -> null
get("b") -> null
get("c") -> "C"
```

## Work on it

1. Choose a starter below. Implement that file without importing reference code.
2. Run the examples, then the full suite from the repository root:

```sh
python3 practice.py test lru-cache --language python --suite examples
python3 practice.py test lru-cache --language python
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

- When would LFU or TTL-based eviction be preferable?
- How would concurrent gets affect locking and recency?
- How would you reduce a cache stampede on popular missing keys?
