import type { Clock } from "../../../../tooling/typescript/contracts.js";

// Implement the challenge contract here.
export class SlidingWindowLimiter {
  constructor(limit: number, windowMs: number, clock: Clock) {
    throw new Error("Not implemented: constructor");
  }

  allow(client: string): boolean {
    throw new Error("Not implemented: allow");
  }
}
