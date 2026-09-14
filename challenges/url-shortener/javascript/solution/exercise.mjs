// Independent JavaScript practice track; no TypeScript build needed.
export class URLShortener {
    urls = new Map();
    codes = new Map();
    nextId = 1;
    shorten(url) {
        const existing = this.urls.get(url);
        if (existing !== undefined)
            return existing;
        const alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
        let number = this.nextId++;
        const digits = [];
        while (number > 0) {
            digits.push(alphabet[number % 62]);
            number = Math.floor(number / 62);
        }
        const code = digits.reverse().join("");
        this.urls.set(url, code);
        this.codes.set(code, url);
        return code;
    }
    resolve(code) {
        return this.codes.get(code) ?? null;
    }
}
