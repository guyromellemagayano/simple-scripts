"""Reference: reversible allocation through two maps."""


class URLShortener:
    def __init__(self):
        self._urls: dict[str, str] = {}
        self._codes: dict[str, str] = {}
        self._next_id = 1

    def shorten(self, url: str) -> str:
        if url in self._urls:
            return self._urls[url]
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        number = self._next_id
        digits = []
        while number:
            number, remainder = divmod(number, 62)
            digits.append(alphabet[remainder])
        code = "".join(reversed(digits))
        self._next_id += 1
        self._urls[url] = code
        self._codes[code] = url
        return code

    def resolve(self, code: str) -> str | None:
        return self._codes.get(code)
