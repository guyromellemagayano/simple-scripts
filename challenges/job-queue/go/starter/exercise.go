package exercise

import "refresher/tooling/go/contracts"

// Add the state required by the challenge contract.
type JobQueue struct{}

func NewJobQueue(visibilityMS int64, maxAttempts int, clock contracts.Clock) *JobQueue {
	panic("Not implemented")
}

func (q *JobQueue) Enqueue(payload string) string {
	panic("Not implemented")
}

func (q *JobQueue) Reserve() *contracts.Delivery {
	panic("Not implemented")
}

func (q *JobQueue) Ack(receipt string) bool {
	panic("Not implemented")
}

func (q *JobQueue) Nack(receipt string) bool {
	panic("Not implemented")
}

func (q *JobQueue) DeadLetters() []contracts.DeadLetter {
	panic("Not implemented")
}
