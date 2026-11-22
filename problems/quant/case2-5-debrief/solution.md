### Reference answer

> I'd hold off — I don't think this regression shows a link. Coffee and Brent are both trending prices, and a regression of one non-stationary price on another gives a high R² and a big t-stat even when there's no relationship at all: in a quick simulation, about nine pairs of completely independent random walks out of ten come out "significant" in levels. The t-stat of 36 just isn't valid evidence here.
>
> The direct check is to look at daily changes, where the statistics are valid. There the link disappears: the correlation of daily returns is about 0.03, the slope has a t-stat of 0.8 and an R² of 0.001. The level fit is coming from the two series having drifted up together over the sample, not from coffee responding to oil.
>
> And even a real correlation wouldn't show that oil drives coffee — both could react to the dollar or to general commodity flows, and correlation says nothing about direction. Statistical significance also isn't the same as economic relevance or predictive value.
>
> The fertiliser / diesel / freight story is plausible, so it's worth testing properly: I'd want a link in changes with a plausible size and lag (input costs feed through over months, not days), a relationship that holds in sub-periods, and, if you want to claim a long-run level relationship, a cointegration test. For comparison, WTI on Brent survives all of this — t = 55 in daily changes — and there's an arbitrage mechanism behind it. Same method, opposite result.

### What makes this a strong interview answer

- **Names the problem precisely** (spurious regression on non-stationary series) and **quantifies** how common it is.
- **Shows the decisive evidence** (the differences regression) rather than arguing in the abstract.
- **Keeps the four notions apart**: statistical significance, economic significance, predictive performance, causality.
- **Constructive**: turns a bad claim into a testable hypothesis with concrete criteria.
- **Uses a control comparison** (Brent–WTI) to show the method can also confirm a link.

### Common weaknesses

- "Correlation isn't causation" and nothing else — true but not an analysis.
- Arguing with the level correlation instead of computing the change correlation.
- Dismissing the economic mechanism instead of saying how it should be tested.
