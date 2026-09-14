package exercise

import (
	"refresher/tooling/go/harness"
	"testing"
)

func TestAssessment(t *testing.T) {
	harness.Run(t, func(config harness.Config, clock *harness.Clock) harness.Execute {
		queue := harness.NewFakeQueue(config.Int("max_attempts"))
		sender := harness.NewFakeSender(config)
		subject := NewNotificationDispatcher(harness.NewFakeStore(clock.Read), queue,
			sender.Send, config.Int64("idempotency_ttl_ms"))
		return func(method string, args []any) any {
			switch method {
			case "submit":
				return subject.Submit(harness.Str(args, 0), harness.Str(args, 1))
			case "process_one":
				return subject.ProcessOne()
			case "sent_messages":
				return sender.Sent
			case "send_attempts":
				return sender.Attempts
			case "dead_letters":
				return queue.Dead
			default:
				return harness.Unknown(method)
			}
		}
	})
}
