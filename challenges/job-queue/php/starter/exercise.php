<?php
declare(strict_types=1);

namespace Refresher;

use Closure;
use LogicException;

final class JobQueue implements JobQueuePort
{
    public function __construct(
        int $visibilityMs,
        int $maxAttempts,
        Closure $clock,
    ) {
        throw new LogicException("Not implemented");
    }

    public function enqueue(string $payload): string
    {
        throw new LogicException("Not implemented");
    }

    public function reserve(): ?array
    {
        throw new LogicException("Not implemented");
    }

    public function ack(string $receipt): bool
    {
        throw new LogicException("Not implemented");
    }

    public function nack(string $receipt): bool
    {
        throw new LogicException("Not implemented");
    }

    public function deadLetters(): array
    {
        throw new LogicException("Not implemented");
    }
}
