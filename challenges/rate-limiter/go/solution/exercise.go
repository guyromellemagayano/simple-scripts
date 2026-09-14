package exercise

import "refresher/tooling/go/contracts"

type SlidingWindowLimiter struct {
	limit    int
	windowMS int64
	clock    contracts.Clock
	clients  map[string][]int64
}

func NewSlidingWindowLimiter(limit int, windowMS int64, clock contracts.Clock) *SlidingWindowLimiter {
	return &SlidingWindowLimiter{limit, windowMS, clock, make(map[string][]int64)}
}

func (l *SlidingWindowLimiter) Allow(client string) bool {
	now := l.clock()
	history := l.clients[client]
	head := 0
	for head < len(history) && history[head] <= now-l.windowMS {
		head++
	}
	history = history[head:]
	if len(history) >= l.limit {
		l.clients[client] = history
		return false
	}
	l.clients[client] = append(history, now)
	return true
}
