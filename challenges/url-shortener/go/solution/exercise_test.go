package exercise

import (
	"refresher/tooling/go/harness"
	"testing"
)

func TestAssessment(t *testing.T) {
	harness.Run(t, func(config harness.Config, clock *harness.Clock) harness.Execute {
		subject := NewURLShortener()
		return func(method string, args []any) any {
			switch method {
			case "shorten":
				return subject.Shorten(harness.Str(args, 0))
			case "resolve":
				return harness.Optional(subject.Resolve(harness.Str(args, 0)))
			default:
				return harness.Unknown(method)
			}
		}
	})
}
