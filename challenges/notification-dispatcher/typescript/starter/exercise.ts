import type { JobQueuePort, KeyValueStore, Sender } from "../../../../tooling/typescript/contracts.js";

// Implement the challenge contract here.
export class NotificationDispatcher {
  constructor(store: KeyValueStore, queue: JobQueuePort,
              sender: Sender, idempotencyTtlMs: number) {
    throw new Error("Not implemented: constructor");
  }

  submit(key: string, message: string): string {
    throw new Error("Not implemented: submit");
  }

  processOne(): string {
    throw new Error("Not implemented: processOne");
  }
}
