# Reference explanation: Idempotent Notification Dispatcher

Read this after making an attempt.

Submission checks the injected store, returning the stored job ID on a hit. Otherwise it enqueues once and stores that ID with a TTL. Processing reserves once, invokes the sender, and acknowledges success or negatively acknowledges failure. The dispatcher adds O(1) orchestration beyond dependency costs and does not own retry state. This process-local design is not atomic across store and queue and cannot promise exactly-once delivery.

## Language rehearsal

- Python: explain the chosen container and its mutation semantics; use explicit None checks.
- JavaScript: explain Map versus a plain object, reference identity, and synchronous exceptions.
- TypeScript: use the public types to express absence and dependency contracts.
- Go: explain pointer versus value ownership, zero values, and explicit success/error results.
- PHP: explain associative arrays, strict scalar types, closures, and null handling.

## Check the reference

```sh
python3 practice.py test notification-dispatcher --language python --target solution
```

Repeat with javascript, typescript, go, and php. Compare the implementations only
after solving independently; their algorithm is shared but their containers and
type systems differ.
