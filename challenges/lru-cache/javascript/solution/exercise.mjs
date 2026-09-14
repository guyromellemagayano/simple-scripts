// Independent JavaScript practice track; no TypeScript build needed.
export class LRUCache {
    capacity;
    entries = new Map();
    constructor(capacity) {
        this.capacity = capacity;
    }
    get(key) {
        const value = this.entries.get(key);
        if (value === undefined)
            return null;
        this.entries.delete(key);
        this.entries.set(key, value);
        return value;
    }
    put(key, value) {
        this.entries.delete(key);
        this.entries.set(key, value);
        if (this.entries.size > this.capacity) {
            const oldest = this.entries.keys().next().value;
            this.entries.delete(oldest);
        }
    }
}
