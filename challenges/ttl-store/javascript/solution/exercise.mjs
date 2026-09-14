// Independent JavaScript practice track; no TypeScript build needed.
export class TTLStore {
    clock;
    entries = new Map();
    constructor(clock) {
        this.clock = clock;
    }
    put(key, value, ttlMs) {
        this.entries.set(key, { value, deadline: this.clock() + ttlMs });
    }
    get(key) {
        const entry = this.entries.get(key);
        if (entry === undefined)
            return null;
        if (this.clock() >= entry.deadline) {
            this.entries.delete(key);
            return null;
        }
        return entry.value;
    }
    delete(key) {
        if (this.get(key) === null)
            return false;
        return this.entries.delete(key);
    }
}
