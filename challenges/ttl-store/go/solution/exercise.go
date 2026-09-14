package exercise

import "refresher/tooling/go/contracts"

type entry struct {
	value    string
	deadline int64
}

type TTLStore struct {
	clock   contracts.Clock
	entries map[string]entry
}

func NewTTLStore(clock contracts.Clock) *TTLStore {
	return &TTLStore{clock: clock, entries: make(map[string]entry)}
}

func (s *TTLStore) Put(key, value string, ttlMS int64) {
	s.entries[key] = entry{value, s.clock() + ttlMS}
}

func (s *TTLStore) Get(key string) (string, bool) {
	e, exists := s.entries[key]
	if !exists {
		return "", false
	}
	if s.clock() >= e.deadline {
		delete(s.entries, key)
		return "", false
	}
	return e.value, true
}

func (s *TTLStore) Delete(key string) bool {
	if _, exists := s.Get(key); !exists {
		return false
	}
	delete(s.entries, key)
	return true
}
