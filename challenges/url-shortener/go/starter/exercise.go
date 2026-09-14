package exercise

// Add the state required by the challenge contract.
type URLShortener struct{}

func NewURLShortener() *URLShortener {
	panic("Not implemented")
}

func (s *URLShortener) Shorten(url string) string {
	panic("Not implemented")
}

func (s *URLShortener) Resolve(code string) (string, bool) {
	panic("Not implemented")
}
