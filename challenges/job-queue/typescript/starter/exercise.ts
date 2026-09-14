import type { Clock, DeadLetter, Delivery, JobQueuePort } from "../../../../tooling/typescript/contracts.js";

// Implement the challenge contract here.
export class JobQueue implements JobQueuePort {
  constructor(visibilityMs: number, maxAttempts: number, clock: Clock) {
    throw new Error("Not implemented: constructor");
  }

  enqueue(payload: string): string {
    throw new Error("Not implemented: enqueue");
  }

  reserve(): Delivery | null {
    throw new Error("Not implemented: reserve");
  }

  ack(receipt: string): boolean {
    throw new Error("Not implemented: ack");
  }

  nack(receipt: string): boolean {
    throw new Error("Not implemented: nack");
  }

  deadLetters(): DeadLetter[] {
    throw new Error("Not implemented: deadLetters");
  }
}
