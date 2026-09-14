package exercise

import (
	"refresher/tooling/go/harness"
	"testing"
)

func TestAssessment(t *testing.T) {
	harness.Run(t, func(config harness.Config, clock *harness.Clock) harness.Execute {
		subject := NewSlidingWindowLimiter(config.Int("limit"), config.Int64("window_ms"), clock.Read)
		return func(method string, args []any) any {
			switch method {
			case "allow":
				return subject.Allow(harness.Str(args, 0))
			default:
				return harness.Unknown(method)
			}
		}
	})
}
