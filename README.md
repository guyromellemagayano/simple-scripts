# System Design Coding Refresher

A hands-on interview workbook: **six progressively harder challenges in Python,
JavaScript, TypeScript, Go, and PHP**. Implement small stateful systems, test their
behavior, then explain how the design would change under concurrency and scale.

Each challenge has a problem statement, exact starter interfaces, examples, an
assessment suite, progressive hints, a self-review rubric, and separate reference
solutions. JavaScript and TypeScript are independent tracks, both running on Node.js.

## Start practising

Open [TTL Key-Value Store](challenges/ttl-store/README.md), choose a language, and
edit its starter—for example, the [Python starter](challenges/ttl-store/python/starter/exercise.py).
Run the examples, then the full suite:

    python3 practice.py test ttl-store --language python --suite examples
    python3 practice.py test ttl-store --language python

New starters deliberately raise **Not implemented**. Replace those placeholders,
including the constructor, as you solve the problem. Tests default to your starter
and never substitute reference code. Use --language javascript, typescript, go,
or php for another track. After your attempt, check the reference:

    python3 practice.py test ttl-store --language python --target solution

## Curriculum

1. [TTL Key-Value Store](challenges/ttl-store/README.md) — expiration, maps, injected clocks. 20–30 minutes.
2. [LRU Cache](challenges/lru-cache/README.md) — bounded storage, recency, eviction. 30–40 minutes.
3. [Sliding-Window Rate Limiter](challenges/rate-limiter/README.md) — per-client quotas and time boundaries. 35–45 minutes.
4. [URL Shortener](challenges/url-shortener/README.md) — bidirectional lookup and ID encoding. 30–45 minutes.
5. [Job Queue](challenges/job-queue/README.md) — receipts, visibility timeouts, retries, dead letters. 60–75 minutes.
6. [Notification Dispatcher](challenges/notification-dispatcher/README.md) — idempotency, dependency injection, delivery failures. 60–75 minutes.

Timeboxes are per language attempt. Add 10–15 minutes to explain the design
follow-ups aloud. Exercises run locally in one process using memory; no database,
HTTP server, account, or network connection is needed to run the assessments.

## Setup

Python 3.11 or newer runs the common CLI. Install only the runtime for the language
you are practising; full repository verification requires all five tracks.

- **Python:** standard-library unittest; no pip dependencies.
- **JavaScript:** Node.js 22 or newer; ES modules and node:test. No npm installation required.
- **TypeScript:** Node.js 22 or newer and npm. Run npm ci to install the locked local compiler and Node types.
- **Go:** Go 1.22 or newer; standard-library testing, with no external module dependencies.
- **PHP:** PHP CLI 8.2 or newer with its standard SPL extension. Explicit checks work regardless of PHP assert() settings. Composer is not required.

Initial verification used Python 3.14.7, Node.js 26.8.2, Go 1.27.1, PHP 8.2.11,
and TypeScript 7.0.2. Earlier listed runtime baselines have not been separately tested.

    npm ci
    python3 practice.py list
    python3 practice.py verify

After dependency installation, assessments run offline. Missing runtimes or a
missing compiler produce a failing command with setup guidance. Compilation and
Go caches stay under ignored .cache/. Individual TypeScript tests compile only
the selected attempt and its imports.

Run examples from the repository root, or use an absolute path to practice.py
from another directory.

## Rehearsal routes

**One language at a time:** solve challenges 1–6 in Python, then repeat in JavaScript,
TypeScript, Go, and PHP. Concentrate on language fluency before switching.

**One design across languages:** solve challenge 1 in all five languages before
moving to challenge 2. Compare containers, typing, absence, errors, and ownership.
Start each attempt from its own starter.

For each attempt: read the contract, sketch the state and transitions, implement,
run examples, run the full suite, explain complexity, answer the follow-ups, then
review hints or reference code as needed. Keep notes and scores locally; there is
no automatic progress tracker or remote judge.

## Commands and verification

    python3 practice.py list
    python3 practice.py test job-queue --language go --suite examples
    python3 practice.py test notification-dispatcher --language php
    python3 practice.py test rate-limiter --language typescript --target solution
    python3 practice.py verify

The test command defaults to --target starter --suite full. Full includes examples
and additional assessment cases. Failures return a nonzero exit code. Every case
gets a fresh instance and a controllable clock, with no sleeps.

The verify command tests all 30 references, loads or compiles all 30 starter
interfaces without invoking unfinished methods, compiles TypeScript, and runs
the runner's regression tests and original Python suite. It checks workbook
integrity; use the test command to assess your implementation. Subprocesses have
a 120-second timeout to catch accidental infinite loops.

Fixtures are visible. Passing demonstrates assessed behavior, not a complexity
guarantee or readiness for production.

## Layout

- challenges/: prompts, hints, explanations, and shared fixtures.
- Each challenge's language directories contain independent starter/ and solution/ folders.
- tooling/: language adapters, dependency ports, and capstone doubles.
- tests/: regression tests for the runner.
- python/: preserved original scripts and tests.

See [the harness guide](tooling/README.md) for fixture semantics and extension points.

## Original Python scripts

Original games, utilities, and basic exercises remain at their existing paths.
See [the Python catalog](python/README.md).

    python3 python/utils/password_generator.py
    python3 -m unittest discover -s python/tests -v
    make -C python test
