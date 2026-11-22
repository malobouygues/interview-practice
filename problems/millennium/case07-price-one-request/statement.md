**Desk context**

Quote a single client request around fair value, charging more for size and get the side exactly right. A client BUY means the market maker is SELLING, so you quote the ask (above reference); a client SELL means the maker is BUYING, so you quote the bid (below reference).

**Problem**

Implement `quote_request(reference, half_spread, side, quantity, size_params, tick_size)`.

**Formula**

```text
BUY:  ceil((ref + hs + k*q) / tick) * tick
SELL: floor((ref - hs - k*q) / tick) * tick
```

with size penalty `k = size_params['k']` and `q = quantity`.

> *Dans l'énoncé original les crochets sont des symboles de plafond et de plancher ; transcrits ici en ceil / floor pour lever l'ambiguïté.*

**Rules**

- A bigger quantity worsens the price (the `k*quantity` penalty).
- Round outward to the tick grid: ask up, bid down.

**Constraints**

- `side` is `'BUY'` or `'SELL'`. numpy available.

**Sample I/O**

```python
quote_request(100.0, 0.05, 'BUY', 100, {'k':1e-5}, 0.01) -> 100.06
quote_request(100.0, 0.05, 'SELL', 100, {'k':1e-5}, 0.01) -> 99.94
```

**Notes**

- The side confusion is the trap: client BUY => maker sells the ask; client SELL => maker buys the bid.
