// Synchronous capstone doubles; these import no challenge implementations.
export class FakeStore {
  entries = new Map();
  constructor(clock) { this.clock = clock; }
  get(key) {
    const entry = this.entries.get(key);
    return entry !== undefined && this.clock() < entry.deadline ? entry.value : null;
  }
  put(key, value, ttlMs) {
    this.entries.set(key, { value, deadline: this.clock() + ttlMs });
  }
}

export class FakeQueue {
  ready = [];
  active = new Map();
  dead = [];
  nextJob = 1;
  nextLease = 1;
  constructor(maxAttempts) { this.maxAttempts = maxAttempts; }
  enqueue(payload) {
    const id = "job-" + this.nextJob++;
    this.ready.push({ job_id: id, payload, attempts: 0 });
    return id;
  }
  reserve() {
    const job = this.ready.shift();
    if (job === undefined) return null;
    job.attempts++;
    const receipt = "lease-" + this.nextLease++;
    this.active.set(receipt, job);
    return { job_id: job.job_id, payload: job.payload, attempt: job.attempts, receipt };
  }
  ack(receipt) { return this.active.delete(receipt); }
  nack(receipt) {
    const job = this.active.get(receipt);
    if (job === undefined) return false;
    this.active.delete(receipt);
    if (job.attempts >= this.maxAttempts) this.dead.push({ ...job });
    else this.ready.push(job);
    return true;
  }
}

export class FakeSender {
  attempts = [];
  sent = [];
  constructor(outcomes) { this.outcomes = [...outcomes]; }
  send(message) {
    this.attempts.push(message);
    const outcome = this.outcomes.shift() ?? "ok";
    if (outcome === "raise") throw new Error("Scripted sender failure");
    if (outcome === "fail") return false;
    this.sent.push(message);
    return true;
  }
}
