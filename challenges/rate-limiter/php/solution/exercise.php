<?php
declare(strict_types=1);

namespace Refresher;

use Closure;
use SplQueue;

final class SlidingWindowLimiter
{
    private array $clients = [];

    public function __construct(
        private int $limit,
        private int $windowMs,
        private Closure $clock,
    ) {}

    public function allow(string $client): bool
    {
        $now = ($this->clock)();
        $timestamps = $this->clients[$client] ??= new SplQueue();
        while (!$timestamps->isEmpty() && $timestamps->bottom() <= $now - $this->windowMs) {
            $timestamps->dequeue();
        }
        if ($timestamps->count() >= $this->limit) {
            return false;
        }
        $timestamps->enqueue($now);
        return true;
    }
}
