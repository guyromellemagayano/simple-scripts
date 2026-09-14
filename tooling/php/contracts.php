<?php
declare(strict_types=1);

namespace Refresher;

interface KeyValueStore
{
    public function put(string $key, string $value, int $ttlMs): void;
    public function get(string $key): ?string;
}

interface JobQueuePort
{
    public function enqueue(string $payload): string;
    /** @return array{job_id:string,payload:string,attempt:int,receipt:string}|null */
    public function reserve(): ?array;
    public function ack(string $receipt): bool;
    public function nack(string $receipt): bool;
}
