import type { Clock, KeyValueStore } from "../../../../tooling/typescript/contracts.js";

// Implement the challenge contract here.
export class TTLStore implements KeyValueStore {
  constructor(clock: Clock) {
    throw new Error("Not implemented: constructor");
  }

  put(key: string, value: string, ttlMs: number): void {
    throw new Error("Not implemented: put");
  }

  get(key: string): string | null {
    throw new Error("Not implemented: get");
  }

  delete(key: string): boolean {
    throw new Error("Not implemented: delete");
  }
}
