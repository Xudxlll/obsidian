# AMA576 Advanced Topics in Algorithmic Trading Lecture 1-2: Baseline Execution Simulator

Lecturer: Selena QIAN

Hong Kong Polytechnic University

January 13, 2026

Core idea: market design → micro data (quotes/trades/LOB) → signals → execution → evaluation.

Goal today: build a baseline execution simulator you can trust.

(Mechanism) Continuous double auction, order types, queues   
(Definitions) bid/ask/mid/spread; returns; simple volatility proxy   
(Execution) market vs limit vs splitting — explicit rules   
(Evaluation) implementation shortfall, fill rate, completion time

After this lecture, you should be able to:

Explain the trade-off: immediacy vs price control (market vs limit)   
Implement three baseline buy executors for Q = 1000 units   
。 Compute execution metrics: average price, IS, fill rate, delay   
Diagnose common backtest/execution mistakes (especially look-ahead)

Definition: A Continuous Double Auction (CDA) is a market where buyers and sellers submit orders at any time, and trades occur continuously whenever an incoming order can be matched against the current limit order book (LOB).

# Limit Order Book (LOB).

Bid side: buy limit orders sorted by higher price first, then time.   
Ask side: sell limit orders sorted by lower price first, then time.   
Best bid/ask: bt = max{bid prices}, at = min{ask prices}.   
Spread and midprice: $\begin{array} { r } { s _ { t } = a _ { t } - b _ { t } , ~ m _ { t } = \frac { a _ { t } + b _ { t } } { 2 } } \end{array}$   
Depth: total quantity available at each price level on both sides.

Core idea. CDA is a two-sided market: liquidity is supplied by limit orders and demanded by marketable orders.

# Matching rules (who trades first).

Price priority: better prices execute first (higher bids, lower asks).   
Time priority (FIFO): within the same price level, earlier orders execute first.

Mini example (walking the book). If $b _ { t } = 9 9 . 9 8$ (size 400) and $a _ { t } = 1 0 0 . 0 0$ (size 300), a buy market order of size 500 executes

$$
3 0 0 \text {   at   } 1 0 0. 0 0 + 2 0 0 \text {   at   next   ask   level   (e.g.,   } 1 0 0. 0 1)
$$

⇒ average execution price increases with depth.

Why CDA matters for algo trading. CDA creates the key trade-off: immediacy (market) vs price improvement / non-fill risk (limit), shaped by spread, depth, and queue position.

Market buy: execute immediately (proxy: next bar price) + slippage   
Limit buy: choose a limit price; filled if the market trades down to it within a wait window   
Splitting (TWAP-like): split Q into N slices; execute one slice each minute Quick check: if you must buy right now and you care about completion, which method feels safest—market, limit, or splitting?

If you buy with a market order at time t, you pay (approximately) the ask $a _ { t }$

$$
\text { cost   vs   mid } = a _ {t} - m _ {t} = a _ {t} - \frac {a _ {t} + b _ {t}}{2} = \frac {a _ {t} - b _ {t}}{2} = \frac {s _ {t}}{2}.
$$

Interpretation: spreads are not optional — they become money paid for immediacy.

# Returns and a simple volatility proxy

$$
p _ {t} = \log (P _ {t}), \quad r _ {t} = p _ {t} - p _ {t - 1} = \log (P _ {t} / P _ {t - 1}).
$$

A simple intraday volatility proxy:

$$
\widehat {\sigma} _ {t} ^ {(3 0 m)} = \operatorname{Std} \left(r _ {t - 2 9}, \dots , r _ {t}\right).
$$

We use this as a first diagnostic for “market difficulty”.

For a buy order of size $Q$ :

$$
\mathrm{IS} = Q \left(\bar {p} _ {\text { exec }} - p _ {0}\right),
$$

where $p _ { 0 }$ is the decision (arrival) price and $\bar { p } _ { \mathrm { e x e c } }$ is the average execution price.

Rule: evaluate strategies on IS-adjusted PnL, not just mid-price returns.

Quick check: For a buy order, what does it mean for implementation shortfall to be positive versus negative in terms of $\bar { p } _ { \mathrm { e x e c } }$ compared with $p _ { 0 } ?$

# A useful decomposition (intuition-level)

A common way to think about IS:

$$
\mathrm{IS}\approx \underbrace{\mathrm{Spread}}_{\mathrm{paying~for~immediacy}} + \underbrace{\mathrm{Impact}}_{\mathrm{your~trade~moves~price}} + \underbrace{\mathrm{Drift}}_{\mathrm{market~moves~while~you~wait}}.
$$

# We fix:

Quantity Q = 1000 units, decision time $t _ { 0 }$   
Execution lag ℓ (bars): decisions at t execute at $t + \ell$ or later   
Slippage (bps): a simple proxy for fees + micro slippage

No look-ahead: you cannot use information from bar t to execute at the price of bar t.

Rule: execute Q at the first feasible time (e.g., next bar).

$$
p _ {\text { exec }} \leftarrow P _ {t _ {0} + \ell} (1 + \text { slip }), \quad \bar {p} _ {\text { exec }} = p _ {\text { exec }}.
$$

Pros: high certainty, fast. Cons: pays spread/slippage; can suffer impact in illiquid conditions.

Choose a limit price:

$$
L = P _ {t _ {0}} (1 - \delta),
$$

where δ is the desired price improvement (in bps).

Fill rule (baseline): filled if within W minutes the low price goes below L:

$$
\min _ {t _ {0} + 1 \leq t \leq t _ {0} + W} \operatorname{Low} _ {t} \leq L.
$$

If filled: execute at L. If not filled: either cancel (unfinished) or convert to market at the end.

Split Q into N slices: $q = Q / N$ . Execute one slice each minute (market slices):

$$
\bar {p} _ {\text { exec }} = \frac {1}{Q} \sum_ {i = 1} ^ {N} q P _ {t _ {i}} (1 + \text { slip }), \quad t _ {i} = t _ {0} + \ell + i.
$$

Pros: reduces instantaneous pressure. Cons: pays spread many times; market drift risk accumulates.

# Evaluation metrics for the three baselines

# Report for each method:

Average execution price $\bar { p } _ { \mathrm { e x e c } }$   
Implementation shortfall (IS)   
。 Completion time (minutes) and fill rate

# Common mistake:

“I observe close at t and also execute at close at t”

# Correct discipline:

decisions at t execute at t + 1 or later (explicit lag)   
use only information available at decision time

We enforce this in code via shifting and explicit execution indices.

# We will:

Load real intraday data and clean timestamps   
Run the three execution baselines for $Q = 1 0 0 0$   
Produce a report: metrics table + trade-off plots

Your task: build an adaptive execution policy to buy Q = 1000 units under a participation cap.

Design an adaptive policy (must be signal-driven):

. Use at least two OHLCV-based signals (e.g., rolling volatility, volume z-score, trend proxy).   
Each minute, decide market qty, limit qty, and αt (limit aggressiveness).

Respect constraints (must pass auto-checks):

No look-ahead: decide at t, execute at t + 1.   
Participation cap: $q _ { t } \leq \mathsf { C A P }$ · volumet each minute.   
Produce a trade log (minute-by-minute actions, fills, remaining quantity).

Evaluate vs baselines:

Compare against market all and split n10 (optionally limit single).   
Run a sweep over multiple t0 and report IS, fill rate, and completion time.   
Include at least two plots that support your conclusions.