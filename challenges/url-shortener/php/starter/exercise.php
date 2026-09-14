<?php
declare(strict_types=1);

namespace Refresher;

use Closure;
use LogicException;

final class URLShortener
{
    public function __construct() { throw new LogicException("Not implemented: constructor"); }

    public function shorten(string $url): string
    {
        throw new LogicException("Not implemented");
    }

    public function resolve(string $code): ?string
    {
        throw new LogicException("Not implemented");
    }
}
