// Independent JavaScript practice track; no TypeScript build needed.
export class JobQueue {
    visibilityMs;
    maxAttempts;
    clock;
    ready = [];
    head = 0;
    active = new Map();
    dead = [];
    nextJob = 1;
    nextLease = 1;
    constructor(visibilityMs, maxAttempts, clock) {
        this.visibilityMs = visibilityMs;
        this.maxAttempts = maxAttempts;
        this.clock = clock;
    }
    fail(job) {
        if (job.attempts >= this.maxAttempts)
            this.dead.push({ ...job });
        else
            this.ready.push(job);
    }
    refresh() {
        const now = this.clock();
        const expired = [...this.active.entries()]
            .filter(([, lease]) => lease.deadline <= now)
            .sort((a, b) => a[1].deadline - b[1].deadline || a[1].sequence - b[1].sequence);
        for (const [receipt, lease] of expired) {
            this.active.delete(receipt);
            this.fail(lease.job);
        }
    }
    enqueue(payload) {
        this.refresh();
        const jobId = "job-" + this.nextJob++;
        this.ready.push({ job_id: jobId, payload, attempts: 0 });
        return jobId;
    }
    reserve() {
        this.refresh();
        if (this.head === this.ready.length)
            return null;
        const job = this.ready[this.head++];
        if (this.head * 2 >= this.ready.length) {
            this.ready = this.ready.slice(this.head);
            this.head = 0;
        }
        job.attempts++;
        const sequence = this.nextLease++;
        const receipt = "lease-" + sequence;
        this.active.set(receipt, { job, deadline: this.clock() + this.visibilityMs, sequence });
        return { job_id: job.job_id, payload: job.payload, attempt: job.attempts, receipt };
    }
    ack(receipt) {
        this.refresh();
        return this.active.delete(receipt);
    }
    nack(receipt) {
        this.refresh();
        const lease = this.active.get(receipt);
        if (lease === undefined)
            return false;
        this.active.delete(receipt);
        this.fail(lease.job);
        return true;
    }
    deadLetters() {
        this.refresh();
        return this.dead.map(job => ({ ...job }));
    }
}
