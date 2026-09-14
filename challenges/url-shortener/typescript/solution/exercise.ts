export class URLShortener {
  private urls = new Map<string, string>();
  private codes = new Map<string, string>();
  private nextId = 1;

  shorten(url: string): string {
    const existing = this.urls.get(url);
    if (existing !== undefined) return existing;
    const alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    let number = this.nextId++;
    const digits: string[] = [];
    while (number > 0) {
      digits.push(alphabet[number % 62]);
      number = Math.floor(number / 62);
    }
    const code = digits.reverse().join("");
    this.urls.set(url, code);
    this.codes.set(code, url);
    return code;
  }

  resolve(code: string): string | null {
    return this.codes.get(code) ?? null;
  }
}
