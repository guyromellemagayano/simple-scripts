package exercise

import "refresher/tooling/go/contracts"

type NotificationDispatcher struct {
	store  contracts.KeyValueStore
	queue  contracts.JobQueuePort
	sender contracts.Sender
	ttlMS  int64
}

func NewNotificationDispatcher(store contracts.KeyValueStore, queue contracts.JobQueuePort,
	sender contracts.Sender, idempotencyTTLMS int64) *NotificationDispatcher {
	return &NotificationDispatcher{store, queue, sender, idempotencyTTLMS}
}

func (d *NotificationDispatcher) Submit(key, message string) string {
	if existing, found := d.store.Get(key); found {
		return existing
	}
	id := d.queue.Enqueue(message)
	d.store.Put(key, id, d.ttlMS)
	return id
}

func (d *NotificationDispatcher) ProcessOne() string {
	delivery := d.queue.Reserve()
	if delivery == nil {
		return "idle"
	}
	if err := d.sender(delivery.Payload); err != nil {
		d.queue.Nack(delivery.Receipt)
		return "failed"
	}
	d.queue.Ack(delivery.Receipt)
	return "sent"
}
