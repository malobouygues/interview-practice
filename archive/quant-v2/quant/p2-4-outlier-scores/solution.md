### A. Reasoning — why compare several scores

"Outlier" is not a property of a number, it is the result of a method, and each method encodes an assumption about the distribution. On fat-tailed commodity returns containing a data error, the classic z-score is blinded by the error, the IQR rule cries wolf, and only a robust score separates the two kinds of extremes. Seeing the disagreement is the point.

### B. Theory

- z-score: assumes roughly normal data; the mean and std include the outliers → **masking** (a huge error hides smaller genuine extremes).
- Modified z-score (Iglewicz–Hoaglin): median and MAD have a 50 % breakdown point; 0.6745 rescales MAD to a std for normal data; the usual threshold is 3.5.
- IQR rule: based on quartiles, robust, but its 1.5 multiplier fits a normal distribution, not fat tails.
- Rolling, past-only versions (`shift(1)`) are what a desk can compute in real time; full-sample versions describe history with hindsight.
- Always score **returns**: on a trending price level, every new high looks extreme.

### C. Implementation

{{code}}

### D. Interpretation (this dataset)

| method | days flagged | hurricane day (2017-08-28, +15 %) | error day (2019-05-14) |
|---|---|---|---|
| \|z\| > 3 | **2** | z = **1.3** (missed) | 19.7 |
| \|modified z\| > 3.5 | 7 | 9.6 | 149 |
| IQR rule | **16** | flagged | flagged |
| \|rolling modified z\| > 5 | 3 | 11.7 | 109 |

- The two error days (+2.32 then −2.27 log points: the price ×10 and back) multiply the standard deviation by about seven (0.118 instead of 0.017), so the z-score sees nothing else.
- The IQR rule flags 16 days: with fat tails, many ordinary big days fall outside 1.5 × IQR.
- The robust scores rank correctly: one enormous anomaly, one strong genuine shock.

### E. Decision

Use a robust, past-only score to *flag* (rolling modified z), then classify each flagged day with other evidence (step 2.5) — never delete on a score alone.

### F. Pitfalls and limits

- Removing everything above |z| > 3: you keep the error-free extremes hidden and may delete real events.
- Full-sample thresholds in a backtest: they use the future.
- Scoring levels instead of returns.
- Thresholds (3, 3.5, 5) are conventions: check sensitivity.

### G. Interview defence

> **Q: "How would you detect outliers in a product price series?"**
>
> **A:** On returns, with a robust score — median and MAD rather than mean and standard deviation — and computed on past data only if it's used in real time. The classic z-score is fragile: in my RBOB data a single fat-finger print inflates the standard deviation so much that a genuine 15 % hurricane move gets a z of 1.3. The modified z-score gives it about 10 and the error about 150. The IQR rule flags 16 days because returns are fat-tailed. And a flag isn't a verdict: I then check whether related markets moved and whether the move reverses, before calling anything an error.
