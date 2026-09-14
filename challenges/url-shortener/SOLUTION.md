# Reference explanation: URL Shortener

Read this after making an attempt.

Use two hash maps and a monotonically increasing counter. A duplicate URL returns its existing mapping without incrementing the counter. Encode new IDs by repeated division by 62 and reverse the digits. New allocation costs O(log ID), lookups average O(1), and mappings use O(n) space.

## Language rehearsal

- Python: explain the chosen container and its mutation semantics; use explicit None checks.
- JavaScript: explain Map versus a plain object, reference identity, and synchronous exceptions.
- TypeScript: use the public types to express absence and dependency contracts.
- Go: explain pointer versus value ownership, zero values, and explicit success/error results.
- PHP: explain associative arrays, strict scalar types, closures, and null handling.

## Check the reference

```sh
python3 practice.py test url-shortener --language python --target solution
```

Repeat with javascript, typescript, go, and php. Compare the implementations only
after solving independently; their algorithm is shared but their containers and
type systems differ.
