<?php
declare(strict_types=1);

namespace Refresher;

use Closure;
use Exception;

final class NotificationDispatcher
{
    public function __construct(
        private KeyValueStore $store,
        private JobQueuePort $queue,
        private Closure $sender,
        private int $idempotencyTtlMs,
    ) {}

    public function submit(string $key, string $message): string
    {
        $existing = $this->store->get($key);
        if ($existing !== null) {
            return $existing;
        }
        $id = $this->queue->enqueue($message);
        $this->store->put($key, $id, $this->idempotencyTtlMs);
        return $id;
    }

    public function processOne(): string
    {
        $delivery = $this->queue->reserve();
        if ($delivery === null) {
            return 'idle';
        }
        try {
            $success = ($this->sender)($delivery['payload']);
        } catch (Exception) {
            $success = false;
        }
        if ($success) {
            $this->queue->ack($delivery['receipt']);
            return 'sent';
        }
        $this->queue->nack($delivery['receipt']);
        return 'failed';
    }
}
