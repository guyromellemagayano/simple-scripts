<?php
declare(strict_types=1);

namespace Refresher;

use Closure;
use RuntimeException;
use SplQueue;

// These doubles deliberately omit visibility scheduling and production storage.
final class FakeStore implements KeyValueStore
{
    private array $entries = [];
    public function __construct(private Closure $clock) {}
    public function get(string $key): ?string
    {
        $entry = $this->entries[$key] ?? null;
        return $entry !== null && ($this->clock)() < $entry[1] ? $entry[0] : null;
    }
    public function put(string $key, string $value, int $ttlMs): void
    {
        $this->entries[$key] = [$value, ($this->clock)() + $ttlMs];
    }
}

final class FakeQueue implements JobQueuePort
{
    private SplQueue $ready;
    private array $active = [];
    public array $dead = [];
    private int $nextJob = 1;
    private int $nextLease = 1;
    public function __construct(private int $maxAttempts) { $this->ready = new SplQueue(); }
    public function enqueue(string $payload): string
    {
        $id = 'job-' . $this->nextJob++;
        $this->ready->enqueue(['job_id' => $id, 'payload' => $payload, 'attempts' => 0]);
        return $id;
    }
    public function reserve(): ?array
    {
        if ($this->ready->isEmpty()) {
            return null;
        }
        $job = $this->ready->dequeue();
        $job['attempts']++;
        $receipt = 'lease-' . $this->nextLease++;
        $this->active[$receipt] = $job;
        return ['job_id' => $job['job_id'], 'payload' => $job['payload'],
            'attempt' => $job['attempts'], 'receipt' => $receipt];
    }
    public function ack(string $receipt): bool
    {
        if (!isset($this->active[$receipt])) {
            return false;
        }
        unset($this->active[$receipt]);
        return true;
    }
    public function nack(string $receipt): bool
    {
        if (!isset($this->active[$receipt])) {
            return false;
        }
        $job = $this->active[$receipt];
        unset($this->active[$receipt]);
        if ($job['attempts'] >= $this->maxAttempts) {
            $this->dead[] = $job;
        } else {
            $this->ready->enqueue($job);
        }
        return true;
    }
}

final class FakeSender
{
    public array $attempts = [];
    public array $sent = [];
    public function __construct(private array $outcomes) {}
    public function send(string $message): bool
    {
        $this->attempts[] = $message;
        $outcome = array_shift($this->outcomes) ?? 'ok';
        if ($outcome === 'raise') {
            throw new RuntimeException('Scripted sender failure');
        }
        if ($outcome === 'fail') {
            return false;
        }
        $this->sent[] = $message;
        return true;
    }
}
