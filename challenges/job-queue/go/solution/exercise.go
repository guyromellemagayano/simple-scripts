package exercise

import (
	"container/list"
	"fmt"
	"refresher/tooling/go/contracts"
	"sort"
)

type job struct {
	id, payload string
	attempts    int
}
type lease struct {
	job      *job
	deadline int64
	sequence int
}
type expiredLease struct {
	receipt string
	lease   lease
}

type JobQueue struct {
	visibilityMS       int64
	maxAttempts        int
	clock              contracts.Clock
	ready              *list.List
	active             map[string]lease
	dead               []contracts.DeadLetter
	nextJob, nextLease int
}

func NewJobQueue(visibilityMS int64, maxAttempts int, clock contracts.Clock) *JobQueue {
	return &JobQueue{
		visibilityMS: visibilityMS, maxAttempts: maxAttempts, clock: clock,
		ready: list.New(), active: make(map[string]lease),
		dead: []contracts.DeadLetter{}, nextJob: 1, nextLease: 1,
	}
}

func (q *JobQueue) fail(j *job) {
	if j.attempts >= q.maxAttempts {
		q.dead = append(q.dead, contracts.DeadLetter{JobID: j.id, Payload: j.payload, Attempts: j.attempts})
	} else {
		q.ready.PushBack(j)
	}
}

func (q *JobQueue) refresh() {
	now := q.clock()
	expired := make([]expiredLease, 0)
	for receipt, l := range q.active {
		if l.deadline <= now {
			expired = append(expired, expiredLease{receipt, l})
		}
	}
	sort.Slice(expired, func(i, j int) bool {
		a, b := expired[i].lease, expired[j].lease
		if a.deadline == b.deadline {
			return a.sequence < b.sequence
		}
		return a.deadline < b.deadline
	})
	for _, e := range expired {
		delete(q.active, e.receipt)
		q.fail(e.lease.job)
	}
}

func (q *JobQueue) Enqueue(payload string) string {
	q.refresh()
	id := fmt.Sprintf("job-%d", q.nextJob)
	q.nextJob++
	q.ready.PushBack(&job{id: id, payload: payload})
	return id
}

func (q *JobQueue) Reserve() *contracts.Delivery {
	q.refresh()
	element := q.ready.Front()
	if element == nil {
		return nil
	}
	j := q.ready.Remove(element).(*job)
	j.attempts++
	sequence := q.nextLease
	q.nextLease++
	receipt := fmt.Sprintf("lease-%d", sequence)
	q.active[receipt] = lease{j, q.clock() + q.visibilityMS, sequence}
	return &contracts.Delivery{JobID: j.id, Payload: j.payload, Attempt: j.attempts, Receipt: receipt}
}

func (q *JobQueue) Ack(receipt string) bool {
	q.refresh()
	if _, exists := q.active[receipt]; !exists {
		return false
	}
	delete(q.active, receipt)
	return true
}

func (q *JobQueue) Nack(receipt string) bool {
	q.refresh()
	l, exists := q.active[receipt]
	if !exists {
		return false
	}
	delete(q.active, receipt)
	q.fail(l.job)
	return true
}

func (q *JobQueue) DeadLetters() []contracts.DeadLetter {
	q.refresh()
	return append([]contracts.DeadLetter{}, q.dead...)
}
