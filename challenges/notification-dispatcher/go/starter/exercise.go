package exercise

import "refresher/tooling/go/contracts"

// Add the state required by the challenge contract.
type NotificationDispatcher struct{}

func NewNotificationDispatcher(store contracts.KeyValueStore, queue contracts.JobQueuePort,
	sender contracts.Sender, idempotencyTTLMS int64) *NotificationDispatcher {
	panic("Not implemented")
}

func (d *NotificationDispatcher) Submit(key, message string) string {
	panic("Not implemented")
}

func (d *NotificationDispatcher) ProcessOne() string {
	panic("Not implemented")
}
