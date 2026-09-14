# 04. URL Shortener

Intermediate · Suggested time: 30–45 minutes

Prerequisites: Bidirectional lookup, integer arithmetic, encoding.

## Problem

Implement the allocation and lookup core of a URL-shortening service without an HTTP server.

## Contract

- Construct an empty shortener. shorten(url) returns a short code, not a complete URL.
- Allocate increasing integer IDs beginning at 1 and encode them in base 62 using exactly 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ, without leading zeroes.
- Repeated identical URLs return the same code and do not consume an ID.
- resolve(code) returns the original URL or the absent-value result. Unknown-code lookups do not allocate IDs.
- Treat URLs as opaque, nonempty strings: do not normalize case, trailing slashes, or query parameters. Input URL validation is outside this exercise.
- Target O(log ID) encoding for new URLs and average O(1) lookup. Tests allocate at most 10,000 IDs.

The function names above use conceptual snake_case. JavaScript/TypeScript and PHP
use camelCase; Go uses exported PascalCase methods. Starter signatures define the
exact language binding. Missing strings are None in Python, null in JavaScript,
TypeScript and PHP, and ("", false) in Go. Mutating void operations have null
fixture results. All inputs satisfy the stated constraints; malformed input
validation is not assessed. Test times and numeric inputs are safe integers.

## Example

Starting configuration: {}; clock defaults to 0 ms.

```text
shorten("https://example.test/a") -> "1"
resolve("1") -> "https://example.test/a"
resolve("missing") -> null
```

## Work on it

1. Choose a starter below. Implement that file without importing reference code.
2. Run the examples, then the full suite from the repository root:

```sh
python3 practice.py test url-shortener --language python --suite examples
python3 practice.py test url-shortener --language python
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

- How would you allocate collision-free IDs across writers?
- How would custom aliases, expiration, and deletion affect the model?
- What would you cache and measure in a read-heavy redirect service?
