# AMA576 Advanced Topics in Algorithmic Trading

# Lecture 3: Limit Order Books, Liquidity, and Microstructure Signals

Lecturer: Selena QIAN

Hong Kong Polytechnic University

January 22, 2026

Today we connect quotes (order book) to execution quality.

Quotes vs trades   
Measuring liquidity: spread, depth, imbalance, microprice   
Intraday microstructure: returns, realized volatility, inter-arrival times   
Tick size, latency, fragmentation: why they matter for costs   
In-class Python: compute LOB features from real-time snapshots

After this lecture, you should be able to:

Explain how the LOB encodes liquidity (spread, depth, queues)   
Compute basic LOB features from snapshots (spread, imbalance, microprice)   
Link LOB features to short-horizon price changes (a simple predictive check)   
Extend an execution simulator with LOB-based decision rules and constraints   
Write validation checks to avoid microstructure backtest pitfalls

# Quotes vs trades: what data do we actually observe?

Trades record what happened (executions).

Quotes describe what could happen next (available liquidity).

Trade data: price, size, time, aggressor side (if available)   
Quote data (LOB): bid/ask price levels + sizes, updated frequently   
A trade is a transition: it consumes resting liquidity and changes the book

Execution problem: you pay costs based on the book you face, not only past trades.

Let best bid/ask be $b _ { t }$ and $a _ { t }$ with sizes $q _ { t } ^ { b }$ and $q _ { t } ^ { a }$ .

Quoted spread: $s _ { t } = a _ { t } - b _ { t }$   
Midprice: $\begin{array} { r } { m _ { t } = \frac { a _ { t } + b _ { t } } { 2 } } \end{array}$   
Top-of-book depth: $\left( q _ { t } ^ { b } , q _ { t } ^ { a } \right)$

Interpretation: spread captures immediacy cost, depth captures how much you can trade before walking the book.

# Effective spread (trade-based) vs quoted spread (quote-based)

Quoted spread uses quotes; effective spread uses the actual trade price $p _ { t } ^ { \mathsf { t r a d e } }$

$$
\text { Effective   spread } = 2 \left| p _ {t} ^ {\text { trade }} - m _ {t} \right|.
$$

If you trade at the mid, effective spread is near zero (rare).   
If you trade at the ask for a buy, effective spread is about the quoted spread.

Why it matters: quoted spread is an opportunity; effective spread is the realized cost you actually paid.

A simple depth-weighted price is:

$$
p _ {t} ^ {\mathrm{micro}} = \frac {a _ {t} q _ {t} ^ {b} + b _ {t} q _ {t} ^ {a}}{q _ {t} ^ {a} + q _ {t} ^ {b}}.
$$

If $q _ { t } ^ { b } \gg q _ { t } ^ { a }$ , microprice is closer to $a _ { t }$ (more upward pressure).   
If $q _ { t } ^ { a } \gg q _ { t } ^ { b }$ , microprice is closer to $b _ { t }$ (more downward pressure).

# Order imbalance: a simple microstructure signal

Top-of-book imbalance:

$$
\mathrm{OI} _ {t} = \frac {q _ {t} ^ {b} - q _ {t} ^ {a}}{q _ {t} ^ {b} + q _ {t} ^ {a}} \in [ - 1, 1 ].
$$

。 $\mathrm { O I } _ { t } > 0$ : bid side is stronger (more buy-side depth)   
$\mathrm { O I } _ { t } < 0$ : ask side is stronger (more sell-side depth)

Quick check: if $\mathrm { O I } _ { t }$ is strongly positive, should a buyer be more aggressive or more patient?

# A first impact proxy (for later optimization)

A simple linear (temporary) impact proxy:

$$
\Delta p _ {t} \approx \lambda \cdot \frac {q _ {t}}{V _ {t}},
$$

where $q _ { t }$ is your traded quantity, $V _ { t }$ is market volume (or depth proxy), and $\lambda > 0$ is an impact coefficient.

Larger participation $\begin{array} { r } { \frac { q _ { t } } { V _ { t } } \Rightarrow \mathsf { l a r g e r } } \end{array}$ expected price concession   
This motivates participation caps and adaptive slicing

# Inter-arrival times: “how fast does information arrive?”

Let $t _ { i }$ be event times (trades or quote updates). Inter-arrival time:

$$
\Delta_ {i} = t _ {i} - t _ {i - 1}.
$$

Small $\Delta _ { j }$ : intense activity (high arrival rate)   
Large $\Delta _ { j }$ : quiet periods (lower arrival rate)

Why it matters: arrival rates affect how quickly limits may fill and how quickly the book changes.

Prices move on a grid:

$$
p \in \{k \cdot \tau : k \in \mathbb {Z} \},
$$

where τ is the tick size.

Smaller tick ⇒ tighter quotes possible, more price competition   
Larger tick ⇒ wider effective spread, different queue dynamics

Execution implication: one tick often dominates small limit-price improvements.

# We will:

Pull real-time LOB snapshots (public API)   
。 Compute and visualize: spread, depth, imbalance, microprice   
Run a simple predictive check: does imbalance predict next mid move?   
。 Extend the baseline execution simulator with a LOB-informed rule