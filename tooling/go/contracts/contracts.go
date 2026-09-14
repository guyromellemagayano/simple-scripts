// Package contracts defines the ports used by the dispatcher and its test doubles.
package contracts

type Clock func() int64

type Delivery struct {
	JobID   string `json:"job_id"`
	Payload string `json:"payload"`
	Attempt int    `json:"attempt"`
	Receipt string `json:"receipt"`
}

type DeadLetter struct {
	JobID    string `json:"job_id"`
	Payload  string `json:"payload"`
	Attempts int    `json:"attempts"`
}

type KeyValueStore interface {
	Put(key, value string, ttlMS int64)
	Get(key string) (string, bool)
}

type JobQueuePort interface {
	Enqueue(payload string) string
	Reserve() *Delivery
	Ack(receipt string) bool
	Nack(receipt string) bool
}

type Sender func(message string) error
