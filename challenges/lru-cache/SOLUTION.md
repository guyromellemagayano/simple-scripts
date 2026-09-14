# Reference explanation: LRU Cache

Read this after making an attempt.

Maintain values in least-to-most-recent order. A successful get or put moves the key to the newest end; a new key that exceeds capacity removes the oldest. Python OrderedDict, JavaScript/TypeScript Map, a Go map plus container/list, and PHP's ordered associative array provide the implementations. Operations are average O(1); memory is O(capacity).

## Language rehearsal

- Python: explain the chosen container and its mutation semantics; use explicit None checks.
- JavaScript: explain Map versus a plain object, reference identity, and synchronous exceptions.
- TypeScript: use the public types to express absence and dependency contracts.
- Go: explain pointer versus value ownership, zero values, and explicit success/error results.
- PHP: explain associative arrays, strict scalar types, closures, and null handling.

## Check the reference

```sh
python3 practice.py test lru-cache --language python --target solution
```

Repeat with javascript, typescript, go, and php. Compare the implementations only
after solving independently; their algorithm is shared but their containers and
type systems differ.
