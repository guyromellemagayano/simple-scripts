package exercise

import "refresher/tooling/go/contracts"

// Add the state required by the challenge contract.
type TTLStore struct{}

func NewTTLStore(clock contracts.Clock) *TTLStore {
	panic("Not implemented")
}

func (s *TTLStore) Put(key, value string, ttlMS int64) {
	panic("Not implemented")
}

func (s *TTLStore) Get(key string) (string, bool) {
	panic("Not implemented")
}

func (s *TTLStore) Delete(key string) bool {
	panic("Not implemented")
}
