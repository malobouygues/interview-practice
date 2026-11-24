### A. Reasoning — why evidence, not thresholds, decides

A score tells you a move is unusual, not why. The cost of a wrong decision is asymmetric in both directions: keeping a fat-finger print poisons every statistic (step 2.4 showed the masking), deleting a refinery outage erases precisely the risk the desk trades. The decision therefore rests on the two facts that distinguish them: does anything related move, and does it last?

### B. Theory (PDF, A03-B and Arbre K)

- Probable **error**: isolated, round factor (×10), not seen in related markets, back to the previous level the next day.
- Probable **event**: visible in related markets, persistent, often datable (an outage, a storm, an expiry).
- Errors → correct from a second source or set to `NaN`; events → keep and document; doubt → keep, flag, and test results with and without.
- The bounce after an error is part of the error: once the bad price is removed, both returns are recomputed and the "event" vanishes.

### C. Implementation

{{code}}

The loop over candidates is deliberate: each verdict uses the previous one (the bounce rule) and is easy to read aloud.

### D. Interpretation (this dataset)

| date | RBOB return | score | confirmed | reverses | verdict |
|---|---|---|---|---|---|
| 2017-08-28 | +0.150 | ≈ 12 | yes (ULSD +8.5 %) | no | **market event** — keep |
| 2019-05-14 | +2.323 | ≈ 108 | no | yes | **data error** — RBOB price to NaN |
| 2019-05-15 | −2.271 | ≈ −102 | no | no | **reversal of an error** |

ULSD on its own: one candidate, 2017-08-28, confirmed by RBOB → market event.

### E. Decision

Set the RBOB price of 2019-05-14 to `NaN` (log it), recompute returns, and annotate late August 2017 as a refinery-outage episode to be shown explicitly — with and without it — in any statistic on gasoline cracks.

### F. Pitfalls and limits

- Deleting every flagged day.
- Treating the bounce after an error as a second event.
- Rules that use more than a day of hindsight would not be available in real time; for historical cleaning one day is acceptable — say so.
- Related markets can fail too: two broken feeds the same day would "confirm" each other. A second source beats any rule.

### G. Interview defence

> **Q: "You find a 15 % jump in gasoline futures. Error or real?"**
>
> **A:** I look for confirmation and persistence. On the outage day in my data, RBOB is up 15 % and ULSD up 8.5 % the same day, and the move doesn't reverse — that's a real supply shock, so I keep it and annotate it. On another day RBOB jumps by a factor of ten, nothing else moves, and it comes straight back the next day — that's a decimal error: I remove the price, log why, and the bounce-back return disappears with it. If the evidence were mixed I wouldn't decide on a threshold — I'd check a second source.
