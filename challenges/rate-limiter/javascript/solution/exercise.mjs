// Independent JavaScript practice track; no TypeScript build needed.
export class SlidingWindowLimiter {
    limit;
    windowMs;
    clock;
    // A head index avoids O(n) Array.shift on every expiration.
    clients = new Map();
    constructor(limit, windowMs, clock) {
        this.limit = limit;
        this.windowMs = windowMs;
        this.clock = clock;
    }
    allow(client) {
        const now = this.clock();
        let history = this.clients.get(client);
        if (history === undefined) {
            history = { timestamps: [], head: 0 };
            this.clients.set(client, history);
        }
        while (history.head < history.timestamps.length &&
            history.timestamps[history.head] <= now - this.windowMs) {
            history.head++;
        }
        // Compact geometrically so storage remains O(limit) and cost is amortized.
        if (history.head > 0 && history.head * 2 >= history.timestamps.length) {
            history.timestamps = history.timestamps.slice(history.head);
            history.head = 0;
        }
        if (history.timestamps.length - history.head >= this.limit)
            return false;
        history.timestamps.push(now);
        return true;
    }
}
