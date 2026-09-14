"""Implement the contract in the challenge README. Reference code is separate."""
class URLShortener:

    def __init__(self):
        raise NotImplementedError('Not implemented: __init__')

    def shorten(self, url: str) -> str:
        raise NotImplementedError('Not implemented: shorten')

    def resolve(self, code: str) -> str | None:
        raise NotImplementedError('Not implemented: resolve')
