import type { Clock, DeadLetter, Delivery, JobQueuePort } from "../../../../tooling/typescript/contracts.js";

type Job = { job_id: string; payload: string; attempts: number };
type Lease = { job: Job; deadline: number; sequence: number };

export class JobQueue implements JobQueuePort {
  private ready: Job[] = [];
  private head = 0;
  private active = new Map<string, Lease>();
  private dead: DeadLetter[] = [];
  private nextJob = 1;
  private nextLease = 1;

  constructor(private visibilityMs: number, private maxAttempts: number, private clock: Clock) {}

  private fail(job: Job): void {
    if (job.attempts >= this.maxAttempts) this.dead.push({ ...job });
    else this.ready.push(job);
  }

  private refresh(): void {
    const now = this.clock();
    const expired = [...this.active.entries()]
      .filter(([, lease]) => lease.deadline <= now)
      .sort((a, b) => a[1].deadline - b[1].deadline || a[1].sequence - b[1].sequence);
    for (const [receipt, lease] of expired) {
      this.active.delete(receipt);
      this.fail(lease.job);
    }
  }

  enqueue(payload: string): string {
    this.refresh();
    const jobId = "job-" + this.nextJob++;
    this.ready.push({ job_id: jobId, payload, attempts: 0 });
    return jobId;
  }

  reserve(): Delivery | null {
    this.refresh();
    if (this.head === this.ready.length) return null;
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

  ack(receipt: string): boolean {
    this.refresh();
    return this.active.delete(receipt);
  }

  nack(receipt: string): boolean {
    this.refresh();
    const lease = this.active.get(receipt);
    if (lease === undefined) return false;
    this.active.delete(receipt);
    this.fail(lease.job);
    return true;
  }

  deadLetters(): DeadLetter[] {
    this.refresh();
    return this.dead.map(job => ({ ...job }));
  }
}
