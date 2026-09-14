import type { JobQueuePort, KeyValueStore, Sender } from "../../../../tooling/typescript/contracts.js";

export class NotificationDispatcher {
  constructor(private store: KeyValueStore, private queue: JobQueuePort,
              private sender: Sender, private idempotencyTtlMs: number) {}

  submit(key: string, message: string): string {
    const existing = this.store.get(key);
    if (existing !== null) return existing;
    const jobId = this.queue.enqueue(message);
    this.store.put(key, jobId, this.idempotencyTtlMs);
    return jobId;
  }

  processOne(): string {
    const delivery = this.queue.reserve();
    if (delivery === null) return "idle";
    let success: boolean;
    try {
      success = this.sender(delivery.payload);
    } catch {
      success = false;
    }
    if (success) {
      this.queue.ack(delivery.receipt);
      return "sent";
    }
    this.queue.nack(delivery.receipt);
    return "failed";
  }
}
