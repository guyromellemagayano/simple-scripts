<?php
declare(strict_types=1);

namespace Refresher;

use RuntimeException;
use ReflectionMethod;
use Throwable;

require_once __DIR__ . '/contracts.php';
require_once __DIR__ . '/support.php';

function canonical(mixed $value): mixed
{
    if (!is_array($value)) {
        return $value;
    }
    if (!array_is_list($value)) {
        ksort($value);
    }
    return array_map(canonical(...), $value);
}

try {
    require getenv('PRACTICE_IMPLEMENTATION');
    $class = __NAMESPACE__ . '\\' . getenv('PRACTICE_CLASS');
    if (!class_exists($class)) {
        throw new RuntimeException('Missing public class: ' . $class);
    }
    $names = ['process_one' => 'processOne', 'dead_letters' => 'deadLetters'];
    foreach (json_decode(getenv('PRACTICE_METHODS') ?: '[]', true, flags: JSON_THROW_ON_ERROR) as $method) {
        $nativeMethod = $names[$method] ?? $method;
        if (!method_exists($class, $nativeMethod) ||
            !(new ReflectionMethod($class, $nativeMethod))->isPublic()) {
            throw new RuntimeException('Missing public method: ' . $method);
        }
    }
    if (getenv('PRACTICE_STRUCTURE') === '1') {
        exit(0);
    }
    $fixture = json_decode(file_get_contents(getenv('PRACTICE_FIXTURE')), true, flags: JSON_THROW_ON_ERROR);
    $selected = array_values(array_filter($fixture['cases'],
        fn(array $case): bool => getenv('PRACTICE_SUITE') === 'full' || $case['suite'] === 'examples'));
    if (count($selected) === 0) {
        throw new RuntimeException('No assessment cases selected');
    }
    $failures = 0;
    foreach ($selected as $case) {
        try {
            $config = $case['config'];
            $now = $config['start_ms'] ?? 0;
            $clock = function () use (&$now): int { return $now; };
            $observations = [];
            switch (getenv('PRACTICE_CHALLENGE')) {
                case 'ttl-store': $subject = new $class($clock); break;
                case 'lru-cache': $subject = new $class($config['capacity']); break;
                case 'rate-limiter': $subject = new $class($config['limit'], $config['window_ms'], $clock); break;
                case 'url-shortener': $subject = new $class(); break;
                case 'job-queue': $subject = new $class($config['visibility_ms'], $config['max_attempts'], $clock); break;
                case 'notification-dispatcher':
                    $queue = new FakeQueue($config['max_attempts']);
                    $sender = new FakeSender($config['sender_outcomes'] ?? []);
                    $subject = new $class(new FakeStore($clock), $queue, $sender->send(...), $config['idempotency_ttl_ms']);
                    $observations = ['sent_messages' => fn() => $sender->sent,
                        'send_attempts' => fn() => $sender->attempts, 'dead_letters' => fn() => $queue->dead];
                    break;
                default: throw new RuntimeException('Unknown challenge');
            }
            foreach ($case['operations'] as $index => $operation) {
                $name = $operation['op'];
                if ($name === 'advance') {
                    $now += $operation['args'][0];
                    continue;
                }
                $method = $names[$name] ?? $name;
                $actual = isset($observations[$name])
                    ? $observations[$name]() : $subject->$method(...$operation['args']);
                if (canonical($actual) !== canonical($operation['expect'])) {
                    throw new RuntimeException('Step ' . ($index + 1) . ': ' . $name .
                        ' expected ' . json_encode($operation['expect'], JSON_THROW_ON_ERROR) .
                        ', got ' . json_encode($actual, JSON_THROW_ON_ERROR));
                }
            }
            echo 'PASS ' . $case['name'] . PHP_EOL;
        } catch (Throwable $error) {
            $failures++;
            fwrite(STDERR, 'FAIL ' . $case['name'] . ': ' . $error->getMessage() . PHP_EOL);
        }
    }
    echo count($selected) . ' cases; ' . $failures . ' failed' . PHP_EOL;
    exit($failures === 0 ? 0 : 1);
} catch (Throwable $error) {
    fwrite(STDERR, 'Assessment error: ' . $error->getMessage() . PHP_EOL);
    exit(1);
}
