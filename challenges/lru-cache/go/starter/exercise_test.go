package exercise

import (
	"refresher/tooling/go/harness"
	"testing"
)

func TestAssessment(t *testing.T) {
	harness.Run(t, func(config harness.Config, clock *harness.Clock) harness.Execute {
		subject := NewLRUCache(config.Int("capacity"))
		return func(method string, args []any) any {
			switch method {
			case "put":
				subject.Put(harness.Str(args, 0), harness.Str(args, 1))
				return nil
			case "get":
				return harness.Optional(subject.Get(harness.Str(args, 0)))
			default:
				return harness.Unknown(method)
			}
		}
	})
}
