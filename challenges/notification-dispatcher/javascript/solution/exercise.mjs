// Independent JavaScript practice track; no TypeScript build needed.
export class NotificationDispatcher {
    store;
    queue;
    sender;
    idempotencyTtlMs;
    constructor(store, queue, sender, idempotencyTtlMs) {
        this.store = store;
        this.queue = queue;
        this.sender = sender;
        this.idempotencyTtlMs = idempotencyTtlMs;
    }
    submit(key, message) {
        const existing = this.store.get(key);
        if (existing !== null)
            return existing;
        const jobId = this.queue.enqueue(message);
        this.store.put(key, jobId, this.idempotencyTtlMs);
        return jobId;
    }
    processOne() {
        const delivery = this.queue.reserve();
        if (delivery === null)
            return "idle";
        let success;
        try {
            success = this.sender(delivery.payload);
        }
        catch {
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
