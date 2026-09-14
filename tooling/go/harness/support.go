package harness

import (
	"errors"
	"fmt"
	"refresher/tooling/go/contracts"
)

type fakeEntry struct {
	value    string
	deadline int64
}
type FakeStore struct {
	clock   contracts.Clock
	entries map[string]fakeEntry
}

func NewFakeStore(clock contracts.Clock) *FakeStore {
	return &FakeStore{clock, make(map[string]fakeEntry)}
}
func (s *FakeStore) Put(key, value string, ttlMS int64) {
	s.entries[key] = fakeEntry{value, s.clock() + ttlMS}
}
func (s *FakeStore) Get(key string) (string, bool) {
	entry, exists := s.entries[key]
	if !exists || s.clock() >= entry.deadline {
		return "", false
	}
	return entry.value, true
}

// This synchronous double intentionally does not implement visibility scheduling.
type fakeJob struct {
	id, payload string
	attempts    int
}
type FakeQueue struct {
	maxAttempts, nextJob, nextLease int
	ready                           []*fakeJob
	active                          map[string]*fakeJob
	Dead                            []contracts.DeadLetter
}

func NewFakeQueue(maxAttempts int) *FakeQueue {
	return &FakeQueue{maxAttempts: maxAttempts, nextJob: 1, nextLease: 1,
		ready: []*fakeJob{}, active: make(map[string]*fakeJob), Dead: []contracts.DeadLetter{}}
}
func (q *FakeQueue) Enqueue(payload string) string {
	id := fmt.Sprintf("job-%d", q.nextJob)
	q.nextJob++
	q.ready = append(q.ready, &fakeJob{id: id, payload: payload})
	return id
}
func (q *FakeQueue) Reserve() *contracts.Delivery {
	if len(q.ready) == 0 {
		return nil
	}
	job := q.ready[0]
	q.ready = q.ready[1:]
	job.attempts++
	receipt := fmt.Sprintf("lease-%d", q.nextLease)
	q.nextLease++
	q.active[receipt] = job
	return &contracts.Delivery{JobID: job.id, Payload: job.payload, Attempt: job.attempts, Receipt: receipt}
}
func (q *FakeQueue) Ack(receipt string) bool {
	if _, exists := q.active[receipt]; !exists {
		return false
	}
	delete(q.active, receipt)
	return true
}
func (q *FakeQueue) Nack(receipt string) bool {
	job, exists := q.active[receipt]
	if !exists {
		return false
	}
	delete(q.active, receipt)
	if job.attempts >= q.maxAttempts {
		q.Dead = append(q.Dead, contracts.DeadLetter{JobID: job.id, Payload: job.payload, Attempts: job.attempts})
	} else {
		q.ready = append(q.ready, job)
	}
	return true
}

type FakeSender struct {
	outcomes       []string
	Attempts, Sent []string
}

func NewFakeSender(config Config) *FakeSender {
	sender := &FakeSender{Attempts: []string{}, Sent: []string{}}
	if outcomes, exists := config["sender_outcomes"]; exists {
		for _, value := range outcomes.([]any) {
			sender.outcomes = append(sender.outcomes, value.(string))
		}
	}
	return sender
}
func (s *FakeSender) Send(message string) error {
	s.Attempts = append(s.Attempts, message)
	outcome := "ok"
	if len(s.outcomes) > 0 {
		outcome, s.outcomes = s.outcomes[0], s.outcomes[1:]
	}
	if outcome != "ok" {
		return errors.New("Scripted sender failure: " + outcome)
	}
	s.Sent = append(s.Sent, message)
	return nil
}
