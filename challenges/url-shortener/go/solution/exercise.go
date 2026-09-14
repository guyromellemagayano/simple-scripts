package exercise

type URLShortener struct {
	urls   map[string]string
	codes  map[string]string
	nextID int
}

func NewURLShortener() *URLShortener {
	return &URLShortener{make(map[string]string), make(map[string]string), 1}
}

func (s *URLShortener) Shorten(url string) string {
	if code, exists := s.urls[url]; exists {
		return code
	}
	const alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	number := s.nextID
	s.nextID++
	digits := make([]byte, 0)
	for number > 0 {
		digits = append(digits, alphabet[number%62])
		number /= 62
	}
	for left, right := 0, len(digits)-1; left < right; left, right = left+1, right-1 {
		digits[left], digits[right] = digits[right], digits[left]
	}
	code := string(digits)
	s.urls[url] = code
	s.codes[code] = url
	return code
}

func (s *URLShortener) Resolve(code string) (string, bool) {
	url, exists := s.codes[code]
	return url, exists
}
