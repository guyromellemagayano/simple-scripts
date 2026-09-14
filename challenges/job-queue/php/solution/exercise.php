<?php
declare(strict_types=1);

namespace Refresher;

use Closure;
use SplQueue;

final class JobQueue implements JobQueuePort
{
    private SplQueue $ready;
    private array $active = [];
    private array $dead = [];
    private int $nextJob = 1;
    private int $nextLease = 1;

    public function __construct(
        private int $visibilityMs,
        private int $maxAttempts,
        private Closure $clock,
    ) {
        $this->ready = new SplQueue();
    }

    private function fail(array $job): void
    {
        if ($job['attempts'] >= $this->maxAttempts) {
            $this->dead[] = $job;
        } else {
            $this->ready->enqueue($job);
        }
    }

    private function refresh(): void
    {
        $now = ($this->clock)();
        $expired = array_filter($this->active, fn(array $lease): bool => $lease['deadline'] <= $now);
        uasort($expired, fn(array $a, array $b): int =>
            ($a['deadline'] <=> $b['deadline']) ?: ($a['sequence'] <=> $b['sequence']));
        foreach ($expired as $receipt => $lease) {
            unset($this->active[$receipt]);
            $this->fail($lease['job']);
        }
    }

    public function enqueue(string $payload): string
    {
        $this->refresh();
        $id = 'job-' . $this->nextJob++;
        $this->ready->enqueue(['job_id' => $id, 'payload' => $payload, 'attempts' => 0]);
        return $id;
    }

    public function reserve(): ?array
    {
        $this->refresh();
        if ($this->ready->isEmpty()) {
            return null;
        }
        $job = $this->ready->dequeue();
        $job['attempts']++;
        $sequence = $this->nextLease++;
        $receipt = 'lease-' . $sequence;
        $this->active[$receipt] = [
            'job' => $job, 'deadline' => ($this->clock)() + $this->visibilityMs,
            'sequence' => $sequence,
        ];
        return [
            'job_id' => $job['job_id'], 'payload' => $job['payload'],
            'attempt' => $job['attempts'], 'receipt' => $receipt,
        ];
    }

    public function ack(string $receipt): bool
    {
        $this->refresh();
        if (!isset($this->active[$receipt])) {
            return false;
        }
        unset($this->active[$receipt]);
        return true;
    }

    public function nack(string $receipt): bool
    {
        $this->refresh();
        if (!isset($this->active[$receipt])) {
            return false;
        }
        $job = $this->active[$receipt]['job'];
        unset($this->active[$receipt]);
        $this->fail($job);
        return true;
    }

    public function deadLetters(): array
    {
        $this->refresh();
        return $this->dead;
    }
}
