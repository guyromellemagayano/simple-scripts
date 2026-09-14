"""Run a selected Python implementation against language-neutral fixtures."""
import importlib.util
import json
import os
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tooling.python.support import FakeQueue, FakeSender, FakeStore


def load_implementation(path):
    spec = importlib.util.spec_from_file_location("selected_exercise", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def build(module, slug, config, clock):
    observations = {}
    if slug == "ttl-store":
        subject = module.TTLStore(clock)
    elif slug == "lru-cache":
        subject = module.LRUCache(config["capacity"])
    elif slug == "rate-limiter":
        subject = module.SlidingWindowLimiter(config["limit"], config["window_ms"], clock)
    elif slug == "url-shortener":
        subject = module.URLShortener()
    elif slug == "job-queue":
        subject = module.JobQueue(config["visibility_ms"], config["max_attempts"], clock)
    elif slug == "notification-dispatcher":
        queue = FakeQueue(config["max_attempts"])
        sender = FakeSender(config.get("sender_outcomes", []))
        subject = module.NotificationDispatcher(
            FakeStore(clock), queue, sender, config["idempotency_ttl_ms"])
        observations = {"sent_messages": lambda: sender.sent,
                        "send_attempts": lambda: sender.attempts,
                        "dead_letters": lambda: queue.dead}
    else:
        raise ValueError("Unknown challenge: " + slug)
    return subject, observations


def main():
    module = load_implementation(os.environ["PRACTICE_IMPLEMENTATION"])
    class_name = os.environ["PRACTICE_CLASS"]
    if not hasattr(module, class_name):
        raise RuntimeError("Missing public class: " + class_name)
    for method in json.loads(os.environ.get("PRACTICE_METHODS", "[]")):
        if not callable(getattr(getattr(module, class_name), method, None)):
            raise RuntimeError("Missing public method: " + method)
    if os.environ.get("PRACTICE_STRUCTURE") == "1":
        return 0
    cases = json.loads(Path(os.environ["PRACTICE_FIXTURE"]).read_text())["cases"]
    suite_name = os.environ["PRACTICE_SUITE"]
    selected = [c for c in cases if suite_name == "full" or c["suite"] == "examples"]
    if not selected:
        raise RuntimeError("No assessment cases selected")

    class Assessment(unittest.TestCase):
        pass

    for index, case in enumerate(selected):
        def run_case(self, case=case):
            now = [case["config"].get("start_ms", 0)]
            subject, observations = build(module, os.environ["PRACTICE_CHALLENGE"],
                                          case["config"], lambda: now[0])
            for step, operation in enumerate(case["operations"], 1):
                name = operation["op"]
                with self.subTest(step=step, operation=name):
                    if name == "advance":
                        now[0] += operation["args"][0]
                        continue
                    method = observations.get(name) or getattr(subject, name)
                    actual = method(*operation["args"])
                    expected = operation["expect"]
                    # JSON serialization distinguishes booleans from integers.
                    self.assertEqual(
                        json.dumps(actual, sort_keys=True, ensure_ascii=False),
                        json.dumps(expected, sort_keys=True, ensure_ascii=False))
        run_case.__doc__ = case["name"]
        setattr(Assessment, f"test_{index:02d}", run_case)

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(Assessment))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
