export class LRUCache {
  private entries = new Map<string, string>();

  constructor(private capacity: number) {}

  get(key: string): string | null {
    const value = this.entries.get(key);
    if (value === undefined) return null;
    this.entries.delete(key);
    this.entries.set(key, value);
    return value;
  }

  put(key: string, value: string): void {
    this.entries.delete(key);
    this.entries.set(key, value);
    if (this.entries.size > this.capacity) {
      const oldest = this.entries.keys().next().value!;
      this.entries.delete(oldest);
    }
  }
}
