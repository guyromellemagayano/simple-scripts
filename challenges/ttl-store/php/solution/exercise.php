<?php
declare(strict_types=1);

namespace Refresher;

use Closure;

final class TTLStore implements KeyValueStore
{
    private array $entries = [];

    public function __construct(private Closure $clock) {}

    public function put(string $key, string $value, int $ttlMs): void
    {
        $this->entries[$key] = [$value, ($this->clock)() + $ttlMs];
    }

    public function get(string $key): ?string
    {
        if (!array_key_exists($key, $this->entries)) {
            return null;
        }
        [$value, $deadline] = $this->entries[$key];
        if (($this->clock)() >= $deadline) {
            unset($this->entries[$key]);
            return null;
        }
        return $value;
    }

    public function delete(string $key): bool
    {
        if ($this->get($key) === null) {
            return false;
        }
        unset($this->entries[$key]);
        return true;
    }
}
