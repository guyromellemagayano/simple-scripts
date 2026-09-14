<?php
declare(strict_types=1);

namespace Refresher;

use Closure;
use LogicException;

final class NotificationDispatcher
{
    public function __construct(
        KeyValueStore $store,
        JobQueuePort $queue,
        Closure $sender,
        int $idempotencyTtlMs,
    ) {
        throw new LogicException("Not implemented");
    }

    public function submit(string $key, string $message): string
    {
        throw new LogicException("Not implemented");
    }

    public function processOne(): string
    {
        throw new LogicException("Not implemented");
    }
}
