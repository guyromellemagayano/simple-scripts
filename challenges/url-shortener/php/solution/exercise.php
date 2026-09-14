<?php
declare(strict_types=1);

namespace Refresher;

final class URLShortener
{
    private array $urls = [];
    private array $codes = [];
    private int $nextId = 1;

    public function shorten(string $url): string
    {
        if (array_key_exists($url, $this->urls)) {
            return $this->urls[$url];
        }
        $alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
        $number = $this->nextId++;
        $digits = [];
        while ($number > 0) {
            $digits[] = $alphabet[$number % 62];
            $number = intdiv($number, 62);
        }
        $code = implode('', array_reverse($digits));
        $this->urls[$url] = $code;
        $this->codes[$code] = $url;
        return $code;
    }

    public function resolve(string $code): ?string
    {
        return $this->codes[$code] ?? null;
    }
}
