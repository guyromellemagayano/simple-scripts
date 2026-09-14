<?php
declare(strict_types=1);

namespace Refresher;

final class LRUCache
{
    private array $entries = [];

    public function __construct(private int $capacity) {}

    public function get(string $key): ?string
    {
        if (!array_key_exists($key, $this->entries)) {
            return null;
        }
        $value = $this->entries[$key];
        unset($this->entries[$key]);
        $this->entries[$key] = $value;
        return $value;
    }

    public function put(string $key, string $value): void
    {
        unset($this->entries[$key]);
        $this->entries[$key] = $value;
        if (count($this->entries) > $this->capacity) {
            unset($this->entries[array_key_first($this->entries)]);
        }
    }
}
