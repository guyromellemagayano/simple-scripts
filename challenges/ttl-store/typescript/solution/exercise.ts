import type { Clock, KeyValueStore } from "../../../../tooling/typescript/contracts.js";

export class TTLStore implements KeyValueStore {
  private entries = new Map<string, { value: string; deadline: number }>();

  constructor(private clock: Clock) {}

  put(key: string, value: string, ttlMs: number): void {
    this.entries.set(key, { value, deadline: this.clock() + ttlMs });
  }

  get(key: string): string | null {
    const entry = this.entries.get(key);
    if (entry === undefined) return null;
    if (this.clock() >= entry.deadline) {
      this.entries.delete(key);
      return null;
    }
    return entry.value;
  }

  delete(key: string): boolean {
    if (this.get(key) === null) return false;
    return this.entries.delete(key);
  }
}
