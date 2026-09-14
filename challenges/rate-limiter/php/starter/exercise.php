<?php
declare(strict_types=1);

namespace Refresher;

use Closure;
use LogicException;

final class SlidingWindowLimiter
{
    public function __construct(
        int $limit,
        int $windowMs,
        Closure $clock,
    ) {
        throw new LogicException("Not implemented");
    }

    public function allow(string $client): bool
    {
        throw new LogicException("Not implemented");
    }
}
