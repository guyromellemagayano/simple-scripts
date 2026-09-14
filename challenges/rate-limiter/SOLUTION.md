# Reference explanation: Sliding-Window Rate Limiter

Read this after making an attempt.

For the current client, discard accepted timestamps outside the rolling interval, then accept and append only if fewer than limit remain. Each timestamp is appended and removed once, giving amortized O(1) work and O(clients × limit) retained timestamps. The map still retains idle clients unless a cleanup strategy is added.

## Language rehearsal

- Python: explain the chosen container and its mutation semantics; use explicit None checks.
- JavaScript: explain Map versus a plain object, reference identity, and synchronous exceptions.
- TypeScript: use the public types to express absence and dependency contracts.
- Go: explain pointer versus value ownership, zero values, and explicit success/error results.
- PHP: explain associative arrays, strict scalar types, closures, and null handling.

## Check the reference

```sh
python3 practice.py test rate-limiter --language python --target solution
```

Repeat with javascript, typescript, go, and php. Compare the implementations only
after solving independently; their algorithm is shared but their containers and
type systems differ.
