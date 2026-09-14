#!/usr/bin/env python3
"""Local assessment runner. Learner tests default to the selected starter."""
import argparse
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
LANGUAGES = ("python", "javascript", "typescript", "go", "php")
FILENAMES = {"python": "exercise.py", "javascript": "exercise.mjs",
             "typescript": "exercise.ts", "go": "exercise.go", "php": "exercise.php"}
CATALOG = json.loads((ROOT / "challenges/catalog.json").read_text())
BY_SLUG = {entry["slug"]: entry for entry in CATALOG}


def require_runtime(name):
    path = shutil.which(name)
    if path is None:
        raise RuntimeError(f"Required runtime '{name}' was not found on PATH. See README.md setup.")
    return path


def implementation_path(slug, language, target):
    return ROOT / "challenges" / slug / language / target / FILENAMES[language]


def run_process(command, *, env=None, capture=False, timeout=120):
    try:
        process = subprocess.Popen(
            command, cwd=ROOT, env=env, text=True,
            stdout=subprocess.PIPE if capture else None,
            stderr=subprocess.PIPE if capture else None,
            start_new_session=os.name == "posix",
        )
    except FileNotFoundError as error:
        raise RuntimeError(f"Executable not found: {command[0]}") from error
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except (subprocess.TimeoutExpired, KeyboardInterrupt) as error:
        # Node and Go launch children. Stop the assessment's process group so an
        # infinite loop in a child cannot outlive the command on macOS/Linux.
        try:
            if os.name == "posix":
                os.killpg(process.pid, signal.SIGKILL)
            else:
                process.kill()
        except ProcessLookupError:
            pass
        process.communicate()
        if isinstance(error, KeyboardInterrupt):
            raise
        raise RuntimeError(f"Command timed out after {timeout}s: {command[0]}") from error
    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)


def compile_typescript(source=None):
    require_runtime("node")
    compiler = ROOT / "node_modules/.bin/tsc"
    if not compiler.is_file():
        raise RuntimeError("TypeScript compiler is missing. Run npm ci first.")
    cache = ROOT / ".cache"
    cache.mkdir(exist_ok=True)
    if source is None:
        result = run_process([str(compiler), "--project", str(ROOT / "tsconfig.json")], capture=True)
    else:
        # Compile only this attempt and its imports, isolating unrelated exercises.
        config = {"extends": str(ROOT / "tsconfig.json"), "include": [str(source)]}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", dir=cache) as handle:
            json.dump(config, handle)
            handle.flush()
            result = run_process([str(compiler), "--project", handle.name], capture=True)
    if result.returncode:
        raise RuntimeError("TypeScript compilation failed:\n" + result.stdout + result.stderr)


def assessment_command(slug, language, target, suite="full", *, structure=False):
    source = implementation_path(slug, language, target)
    if not source.is_file():
        raise RuntimeError(f"Selected implementation is missing: {source.relative_to(ROOT)}")
    fixture = ROOT / "challenges" / slug / "cases.json"
    data = json.loads(fixture.read_text())
    methods = {op["op"] for case in data["cases"] for op in case["operations"]}
    methods.discard("advance")
    if slug == "notification-dispatcher":
        methods -= {"dead_letters", "sent_messages", "send_attempts"}
    env = os.environ.copy()
    env.update({
        "PRACTICE_IMPLEMENTATION": str(source), "PRACTICE_FIXTURE": str(fixture),
        "PRACTICE_CHALLENGE": slug, "PRACTICE_CLASS": BY_SLUG[slug]["class"],
        "PRACTICE_SUITE": suite, "PRACTICE_STRUCTURE": "1" if structure else "0",
        "PRACTICE_METHODS": json.dumps(sorted(methods)),
        "PYTHONIOENCODING": "utf-8", "XDEBUG_MODE": "off",
    })
    if language == "python":
        command = [sys.executable, str(ROOT / "tooling/python/runner.py")]
    elif language in ("javascript", "typescript"):
        if language == "typescript":
            env["PRACTICE_IMPLEMENTATION"] = str(
                ROOT / ".cache/typescript" / source.relative_to(ROOT).with_suffix(".js"))
        command = [require_runtime("node")]
        if not structure:
            command += ["--test", "--test-reporter=spec"]
        command.append(str(ROOT / "tooling/node/runner.mjs"))
    elif language == "go":
        env["GOCACHE"] = str(ROOT / ".cache/go-build")
        env["GOMODCACHE"] = str(ROOT / ".cache/go-mod")
        env["GOTELEMETRY"] = "off"
        command = [require_runtime("go"), "test", "-count=1"]
        command += ["-run", "^$"] if structure else ["-v"]
        command.append("./" + str(source.parent.relative_to(ROOT)))
    else:
        command = [require_runtime("php"), "-d", "display_errors=stderr",
                   str(ROOT / "tooling/php/runner.php")]
    return command, env


def run_assessment(slug, language, target, suite="full", *, structure=False,
                   capture=False, compiled=False):
    if language == "typescript" and not compiled:
        compile_typescript(implementation_path(slug, language, target))
    command, env = assessment_command(slug, language, target, suite, structure=structure)
    return run_process(command, env=env, capture=capture)


def validate_workbook():
    if len(CATALOG) != 6 or len(BY_SLUG) != 6:
        raise RuntimeError("The workbook must contain six distinct challenges.")
    for entry in CATALOG:
        base = ROOT / "challenges" / entry["slug"]
        for filename in ("README.md", "HINTS.md", "SOLUTION.md"):
            if not (base / filename).is_file():
                raise RuntimeError(f"Missing challenge document: {base / filename}")
        cases = json.loads((base / "cases.json").read_text())["cases"]
        if {case["suite"] for case in cases} != {"examples", "assessment"}:
            raise RuntimeError(f"{entry['slug']} must have examples and assessment cases.")
        if len({case["name"] for case in cases}) != len(cases):
            raise RuntimeError(f"Duplicate case names in {entry['slug']}")
        for case in cases:
            if not case["operations"] or not any(op["op"] != "advance" for op in case["operations"]):
                raise RuntimeError(f"Empty assessment case: {case['name']}")
            for op in case["operations"]:
                if not isinstance(op["args"], list) or "expect" not in op:
                    raise RuntimeError(f"Invalid operation in {case['name']}")
        for language in LANGUAGES:
            for target in ("starter", "solution"):
                if not implementation_path(entry["slug"], language, target).is_file():
                    raise RuntimeError(f"Missing {language}/{target} for {entry['slug']}")


def verify():
    validate_workbook()
    for name in ("node", "go", "php"):
        require_runtime(name)
    compile_typescript()
    print("PASS workbook structure and TypeScript compilation", flush=True)
    failures = []
    for entry in CATALOG:
        for language in LANGUAGES:
            label = entry["slug"] + " / " + language
            passed = True
            for target, structure in (("solution", False), ("starter", True)):
                result = run_assessment(entry["slug"], language, target,
                                        structure=structure, capture=True, compiled=True)
                if result.returncode:
                    passed = False
                    failures.append(label + " / " + target)
                    print(f"FAIL {label} / {target}\n{result.stdout}{result.stderr}", flush=True)
            print(("PASS " if passed else "FAIL ") + label +
                  " (reference cases + starter structure)", flush=True)
    for label, directory in (("runner tests", "tests"), ("legacy Python tests", "python/tests")):
        result = run_process([sys.executable, "-m", "unittest", "discover", "-s", directory, "-v"], capture=True)
        if result.returncode:
            failures.append(label)
            print(f"FAIL {label}\n{result.stdout}{result.stderr}", flush=True)
        else:
            print("PASS " + label, flush=True)
    if failures:
        print(f"\nVerification failed: {len(failures)} check(s).", file=sys.stderr)
        return 1
    print("\nVerified 30 reference implementations, 30 starter interfaces, runner tests, and legacy tests.")
    print("Learner correctness is checked separately with the test command.")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="Show the progressive curriculum")
    test = commands.add_parser("test", help="Test one language and one implementation")
    test.add_argument("challenge", choices=list(BY_SLUG))
    test.add_argument("--language", choices=LANGUAGES, required=True)
    test.add_argument("--target", choices=("starter", "solution"), default="starter")
    test.add_argument("--suite", choices=("examples", "full"), default="full")
    commands.add_parser("verify", help="Verify references, starter structure, and repository tests")
    args = parser.parse_args(argv)
    try:
        if args.command == "list":
            for index, entry in enumerate(CATALOG, 1):
                print(f"{index:02d}. {entry['slug']} — {entry['difficulty']} — {entry['minutes']} min")
            print("\nLanguages: " + ", ".join(LANGUAGES))
            return 0
        if args.command == "verify":
            return verify()
        print(f"Testing {args.challenge} / {args.language} / {args.target} ({args.suite})", flush=True)
        return run_assessment(args.challenge, args.language, args.target, args.suite).returncode
    except (RuntimeError, OSError, ValueError) as error:
        print("Error: " + str(error), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
