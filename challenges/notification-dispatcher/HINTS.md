# Progressive hints

Try the example suite before opening a hint.

<details>
<summary>Hint 1</summary>

Look up the idempotency key before producing any side effect.

</details>

<details>
<summary>Hint 2</summary>

Separate submission from delivery; duplicate submissions reuse the queued job ID even after it was sent.

</details>

<details>
<summary>Hint 3</summary>

Catch failures from the sender only. Reserve once, send once, then acknowledge or negatively acknowledge the same receipt.

</details>
