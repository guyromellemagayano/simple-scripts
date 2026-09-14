package exercise

import (
	"refresher/tooling/go/harness"
	"testing"
)

func TestAssessment(t *testing.T) {
	harness.Run(t, func(config harness.Config, clock *harness.Clock) harness.Execute {
		subject := NewJobQueue(config.Int64("visibility_ms"), config.Int("max_attempts"), clock.Read)
		return func(method string, args []any) any {
			switch method {
			case "enqueue":
				return subject.Enqueue(harness.Str(args, 0))
			case "reserve":
				return subject.Reserve()
			case "ack":
				return subject.Ack(harness.Str(args, 0))
			case "nack":
				return subject.Nack(harness.Str(args, 0))
			case "dead_letters":
				return subject.DeadLetters()
			default:
				return harness.Unknown(method)
			}
		}
	})
}
