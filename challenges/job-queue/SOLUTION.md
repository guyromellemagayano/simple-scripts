# Reference explanation: Reliable In-Memory Job Queue

Read this after making an attempt.

Use a ready FIFO, an active-receipt map, and an ordered dead-letter list. Reservations increment attempts and create deadlines plus unique receipts. A common refresh step sorts expired leases by deadline and lease sequence, then retries or dead-letters them. Ack removes an active lease; nack uses the same failure transition as expiry. With L active leases, refresh is O(L + E log E) for E expirations, bounded by O(L log L); queue operations outside refresh are O(1). Retained state is O(ready + leased + dead).

## Language rehearsal

- Python: explain the chosen container and its mutation semantics; use explicit None checks.
- JavaScript: explain Map versus a plain object, reference identity, and synchronous exceptions.
- TypeScript: use the public types to express absence and dependency contracts.
- Go: explain pointer versus value ownership, zero values, and explicit success/error results.
- PHP: explain associative arrays, strict scalar types, closures, and null handling.

## Check the reference

```sh
python3 practice.py test job-queue --language python --target solution
```

Repeat with javascript, typescript, go, and php. Compare the implementations only
after solving independently; their algorithm is shared but their containers and
type systems differ.
