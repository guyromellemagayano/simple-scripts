<?php
declare(strict_types=1);

namespace Refresher;

use Closure;
use LogicException;

final class TTLStore implements KeyValueStore
{
    public function __construct(Closure $clock) {
        throw new LogicException("Not implemented");
    }

    public function put(string $key, string $value, int $ttlMs): void
    {
        throw new LogicException("Not implemented");
    }

    public function get(string $key): ?string
    {
        throw new LogicException("Not implemented");
    }

    public function delete(string $key): bool
    {
        throw new LogicException("Not implemented");
    }
}
