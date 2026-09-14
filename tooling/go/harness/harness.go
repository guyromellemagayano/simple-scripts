// Package harness adapts shared fixture operations to native Go tests.
package harness

import (
	"encoding/json"
	"fmt"
	"os"
	"reflect"
	"testing"
)

type Config map[string]any
type Clock struct{ Now int64 }

func (c *Clock) Read() int64             { return c.Now }
func (c Config) Int(key string) int      { return int(c[key].(float64)) }
func (c Config) Int64(key string) int64  { return int64(c[key].(float64)) }
func Str(args []any, index int) string   { return args[index].(string) }
func Number(args []any, index int) int64 { return int64(args[index].(float64)) }
func Optional(value string, exists bool) any {
	if !exists {
		return nil
	}
	return value
}

type Execute func(method string, args []any) any
type Factory func(config Config, clock *Clock) Execute

type operation struct {
	Op     string
	Args   []any
	Expect any
}
type scenario struct {
	Name, Suite string
	Config      Config
	Operations  []operation
}
type fixture struct{ Cases []scenario }

func normalize(t *testing.T, value any) any {
	t.Helper()
	encoded, err := json.Marshal(value)
	if err != nil {
		t.Fatal(err)
	}
	var normalized any
	if err := json.Unmarshal(encoded, &normalized); err != nil {
		t.Fatal(err)
	}
	return normalized
}

func Run(t *testing.T, factory Factory) {
	t.Helper()
	path := os.Getenv("PRACTICE_FIXTURE")
	if path == "" {
		t.Fatal("Use python3 practice.py test <challenge> --language go")
	}
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	var fixtures fixture
	if err := json.Unmarshal(data, &fixtures); err != nil {
		t.Fatal(err)
	}
	count := 0
	for _, scenario := range fixtures.Cases {
		if os.Getenv("PRACTICE_SUITE") != "full" && scenario.Suite != "examples" {
			continue
		}
		count++
		t.Run(scenario.Name, func(t *testing.T) {
			defer func() {
				if failure := recover(); failure != nil {
					t.Fatalf("Implementation panic: %v", failure)
				}
			}()
			clock := &Clock{}
			if start, exists := scenario.Config["start_ms"]; exists {
				clock.Now = int64(start.(float64))
			}
			execute := factory(scenario.Config, clock)
			for index, operation := range scenario.Operations {
				if operation.Op == "advance" {
					clock.Now += Number(operation.Args, 0)
					continue
				}
				actual := normalize(t, execute(operation.Op, operation.Args))
				if !reflect.DeepEqual(actual, operation.Expect) {
					t.Fatalf("Step %d: %s expected %v, got %v", index+1, operation.Op, operation.Expect, actual)
				}
			}
		})
	}
	if count == 0 {
		t.Fatal("No assessment cases selected")
	}
}

func Unknown(method string) any { panic(fmt.Sprintf("Unknown operation: %s", method)) }
