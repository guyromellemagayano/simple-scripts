<?php
declare(strict_types=1);

namespace Refresher;

use Closure;
use LogicException;

final class LRUCache
{
    public function __construct(int $capacity) {
        throw new LogicException("Not implemented");
    }

    public function get(string $key): ?string
    {
        throw new LogicException("Not implemented");
    }

    public function put(string $key, string $value): void
    {
        throw new LogicException("Not implemented");
    }
}
