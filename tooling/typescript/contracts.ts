/** Shared ports for the independent notification-dispatcher exercise. */
export type Clock = () => number;
export type Delivery = { job_id: string; payload: string; attempt: number; receipt: string };
export type DeadLetter = { job_id: string; payload: string; attempts: number };
export interface KeyValueStore {
  put(key: string, value: string, ttlMs: number): void;
  get(key: string): string | null;
}
export interface JobQueuePort {
  enqueue(payload: string): string;
  reserve(): Delivery | null;
  ack(receipt: string): boolean;
  nack(receipt: string): boolean;
}
export type Sender = (message: string) => boolean;
