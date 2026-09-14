# Assessment harness

Use the root practice.py command to run assessments. It selects exactly one
implementation, supplies fixture metadata, and translates failures into a nonzero
exit status. It never copies a solution into a starter or loads a reference as a fallback.

## Shared cases

Each challenge's cases.json contains a cases array. A case has a unique name,
a suite of examples or assessment, constructor config, and ordered operations.
The full suite includes both categories.

An operation has an op name, positional args, and an expect JSON value.
Object key order does not matter; array order, strings, booleans, and absence do.
Python/Node/PHP distinguish booleans from numbers. Go normalizes typed results
through JSON before comparing them.

The runner owns advance(milliseconds), moving the injected clock without calling
the implementation. Cases start at config.start_ms or zero, use safe integers,
and construct a fresh instance.

Fixtures use snake_case. Node and PHP map process_one to processOne and dead_letters
to deadLetters. Go uses typed adapters beside each implementation. Go's (string,
bool) lookups map to a string when found and JSON null otherwise. Node maps void
put results to null; lookup methods must return null explicitly on absence.

## Language adapters

- Python loads only the selected source with importlib and runs unittest cases.
- JavaScript and compiled TypeScript share the Node test adapter.
- Go runs native tests in the selected target package with typed operation adapters.
- PHP loads its ports and the selected class and runs explicit comparisons.

The runner supplies PRACTICE_IMPLEMENTATION, PRACTICE_FIXTURE, PRACTICE_CHALLENGE,
PRACTICE_CLASS, PRACTICE_SUITE, PRACTICE_METHODS, and PRACTICE_STRUCTURE. These are
internal harness inputs, not exercise APIs. Prefer practice.py over setting them
manually.

Structure checks inspect required public methods in Python, Node, and PHP.
Go compiles its typed test adapters with no tests selected. TypeScript compiles
before the Node structure check. Structure checks do not instantiate starters.

## Independent capstone

Port definitions live in python/contracts.py, typescript/contracts.ts,
go/contracts/, and php/contracts.php. JavaScript uses the same duck-typed
camelCase shape as TypeScript.

Support files beside each runner (or Go's harness package) provide doubles
without importing earlier solutions:

- A store with expiring keys.
- A synchronous FIFO queue with reserve/ack/nack and attempt exhaustion.
  It deliberately omits the visibility scheduler that the dispatcher does not own.
- A sender consuming scripted ok, fail, and raise outcomes, defaulting to success
  afterward. Go represents both failure outcomes with non-nil errors.

Fixture observations sent_messages, send_attempts, and dead_letters read doubles;
they are not dispatcher methods. Sending does not advance the clock, and receipt
completion is synchronous.

## Extend an assessment

Add an operation sequence to shared cases to assess the same behavior in all five
languages. Keep clocks and identifiers deterministic. When an API changes, update
its prompt, ports, starters, references, and adapters together, then run:

    python3 practice.py verify

Passing does not establish asymptotic complexity, durable delivery, or concurrency
safety; address those in the design discussion and subsequent implementations.
