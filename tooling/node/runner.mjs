import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
import test from "node:test";
import assert from "node:assert/strict";
import { FakeStore, FakeQueue, FakeSender } from "./support.mjs";

const implementation = await import(pathToFileURL(process.env.PRACTICE_IMPLEMENTATION).href);
assert.equal(typeof implementation[process.env.PRACTICE_CLASS], "function", "Missing public class");
const names = { process_one: "processOne", dead_letters: "deadLetters" };
for (const method of JSON.parse(process.env.PRACTICE_METHODS ?? "[]")) {
  assert.equal(typeof implementation[process.env.PRACTICE_CLASS].prototype[names[method] ?? method],
    "function", "Missing public method: " + method);
}

function build(config, clock) {
  const Type = implementation[process.env.PRACTICE_CLASS];
  let subject;
  let observations = {};
  switch (process.env.PRACTICE_CHALLENGE) {
    case "ttl-store": subject = new Type(clock); break;
    case "lru-cache": subject = new Type(config.capacity); break;
    case "rate-limiter": subject = new Type(config.limit, config.window_ms, clock); break;
    case "url-shortener": subject = new Type(); break;
    case "job-queue": subject = new Type(config.visibility_ms, config.max_attempts, clock); break;
    case "notification-dispatcher": {
      const queue = new FakeQueue(config.max_attempts);
      const sender = new FakeSender(config.sender_outcomes ?? []);
      subject = new Type(new FakeStore(clock), queue, sender.send.bind(sender), config.idempotency_ttl_ms);
      observations = {
        sent_messages: () => sender.sent, send_attempts: () => sender.attempts,
        dead_letters: () => queue.dead,
      };
      break;
    }
    default: throw new Error("Unknown challenge");
  }
  return { subject, observations };
}

if (process.env.PRACTICE_STRUCTURE !== "1") {
  const { cases } = JSON.parse(readFileSync(process.env.PRACTICE_FIXTURE, "utf8"));
  const selected = cases.filter(c => process.env.PRACTICE_SUITE === "full" || c.suite === "examples");
  assert.ok(selected.length > 0, "No assessment cases selected");
  for (const scenario of selected) {
    test(scenario.name, () => {
      let now = scenario.config.start_ms ?? 0;
      const { subject, observations } = build(scenario.config, () => now);
      for (const [index, operation] of scenario.operations.entries()) {
        if (operation.op === "advance") {
          now += operation.args[0];
          continue;
        }
        const method = names[operation.op] ?? operation.op;
        const result = Object.hasOwn(observations, operation.op)
          ? observations[operation.op]() : subject[method](...operation.args);
        // Only void put maps undefined to JSON null; absence must explicitly be null.
        const actual = operation.op === "put" && result === undefined ? null : result;
        assert.deepStrictEqual(actual, operation.expect, "Step " + (index + 1) + ": " + operation.op);
      }
    });
  }
}
