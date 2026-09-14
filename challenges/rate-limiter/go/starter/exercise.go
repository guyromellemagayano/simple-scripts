package exercise

import "refresher/tooling/go/contracts"

// Add the state required by the challenge contract.
type SlidingWindowLimiter struct{}

func NewSlidingWindowLimiter(limit int, windowMS int64, clock contracts.Clock) *SlidingWindowLimiter {
	panic("Not implemented")
}

func (l *SlidingWindowLimiter) Allow(client string) bool {
	panic("Not implemented")
}
