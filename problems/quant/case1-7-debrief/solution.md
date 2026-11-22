### Reference answer

> **Short version: the TTF price behaves like a random walk, not like a series that mean-reverts to 20 — so we should analyse returns, not levels.**
>
> I ran the two standard tests with opposite starting assumptions. The ADF test, which assumes a unit root, can't reject it on the price level (p ≈ 0.91); the KPSS test, which assumes stationarity, rejects it (p below 1 %). Two tests built from opposite sides agree: shocks to the price are permanent and there is no level it is pulled back to. On daily log returns the picture is reversed — both tests say stationary.
>
> That's also why "mean-reverts to 20" doesn't hold up: the level's average depends entirely on the window — 17.5 €/MWh in the first nine months, 31 in the last nine — so its mean and standard deviation aren't stable quantities to revert to. On returns, risk is about 2.1 % a day (≈ 33 % annualised), with much fatter tails than a normal distribution: four days beyond four standard deviations in three years where a normal would expect almost none.
>
> What I'm not sure about: three years is short for these tests, which have low power against a very slow mean reversion; a structural break would also distort them; and "returns are stationary" doesn't mean volatility is constant or that returns are predictable. I also checked that I'm not mistaking a deterministic trend for a random walk — that's what happened with diesel demand, which I detrend rather than difference. If we found a clear break, or a second price TTF is economically tied to, I would revisit — the latter is a cointegration question, not a reason to model the level on its own.

### What makes this a strong interview answer

1. **Conclusion first**, in the vocabulary of the person asking ("random walk", "returns"), then the evidence.
2. **Nulls stated correctly**: "can't reject a unit root" — never "the test proves a unit root".
3. **The two tests are used as a pair** and the reason is given (opposite nulls).
4. **Numbers with units and an order of magnitude** (€/MWh, % per day), not a list of statistics.
5. **Explicit limits** (power, breaks, what stationarity does not imply) — a senior expects them and trusts the answer more for them.
6. **Shows judgement**: not every trend is differenced (the demand counter-example), and the next question (a relationship with another market) is named.

### Common weaknesses

- "ADF p > 0.05 so it's non-stationary, so we difference" — wrong logic and no evidence from the second test.
- Reporting the standard deviation of the price as its volatility.
- Ten statistics without a conclusion; or a conclusion with no limits.
