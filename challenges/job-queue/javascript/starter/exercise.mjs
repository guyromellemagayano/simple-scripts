// Independent JavaScript practice track; no TypeScript build needed.
// Implement the challenge contract here.
export class JobQueue {
    constructor(visibilityMs, maxAttempts, clock) {
        throw new Error("Not implemented: constructor");
    }
    enqueue(payload) {
        throw new Error("Not implemented: enqueue");
    }
    reserve() {
        throw new Error("Not implemented: reserve");
    }
    ack(receipt) {
        throw new Error("Not implemented: ack");
    }
    nack(receipt) {
        throw new Error("Not implemented: nack");
    }
    deadLetters() {
        throw new Error("Not implemented: deadLetters");
    }
}
