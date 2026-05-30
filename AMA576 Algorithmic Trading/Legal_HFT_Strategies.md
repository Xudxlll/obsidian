# THE HONG KONG POLYTECHNIC UNIVERSITY

# Department of Applied Mathematics

MASTER-LEVEL TRAINING SERIES · PART 1 OF 2

# Legal HFT Strategies

Statistical Arbitrage · Volatility Arbitrage · Liquidity Provision

3-Hour Session

# SECTION 01

# Statistical Arbitrage

# Pairs Trading

Theory & Cointegration   
Key Equations & Derivations   
Implementation Process   
Case Studies: Renaissance, D.E. √ Shaw   
Performance & Risk

# SECTION 02

# Volatility Arbitrage

# Gamma Scalping

Black-Scholes & The Greeks   
Delta-Hedging P&L   
Implementation Process   
Case Studies: Citadel, Optiver, SIG   
Performance & Risk

# SECTION 03

# Liquidity Provision

# Market Making

Avellaneda-Stoikov Model   
Reservation Price & Optimal Spread   
Implementation Process   
Case Studies: Virtu, Jane Street   
Performance & Risk

# What Is High-Frequency Trading?

"HFT uses algorithmic systems executing thousands of orders per second to profit from microscopic price inefficiencies.

Sub-millisecond execution   
> Positions held seconds to minutes   
> End-of-day flat inventory   
Co-location & direct market access

Source: SEC & CFTC Definition Framework

![](images/365788011ad4e6dbfaefb5bf54ff12148f9248778a6bc21659f773f792e09db8.jpg)

\~50%

US Equity Volume

Attributed to HFT

![](images/38ef5baa38279fb026a36a0da020be53f89057214a88bc82d09e70821a52be5e.jpg)

<1ms

Execution Latency

Critical strategies

![](images/ca85cba3e9425c761b638154434ede79818801db30cd2c1a3d72cde5b5ef9ff2.jpg)

5–6

Sharpe Ratio

Top market makers

# 6 Legal Strategy Categories (Part 1 covers first 3)

1. Statistical Arbitrage

2. Volatility Arbitrage

3. Market Making

4. Cross-Venue Arb

Part 2

5. Order Flow Prediction

Part 2

# Statistical Arbitrage — Pairs Trading

Core Idea: Exploit mean-reversion between two cointegrated assets.

Mechanism: When the spread between Asset A and Asset B diverges beyond a statistical threshold, short the outperformer and long the underperformer. Profit when the spread reverts to its historical mean.

Edge Source: Prices may diverge short-term but are anchored by a long-run economic relationship — cointegration.

# Industry Leaders

Renaissance

Technologies

Medallion Fund

D.E. Shaw

Quant Pioneer

Millennium

Mgmt

Multi-Strategy

Two Sigma

ML-Driven

# Strategy Profile

\$

Profitability

5–50 bps

Per trade

@

Win Rate

55–65%

Per trade

Sharpe Ratio

2–4

Typical range

☆

Latency

1–10 μs

Exec window

Position Hold

Min–Days

Horizon

# Mathematical Framework: Cointegration

# Engle-Granger Cointegration Test

STEP 1 — OLS REGRESSION

$$
P _ {B} = \beta_ {0} + \beta_ {1} \cdot P _ {A} + u _ {t}
$$

STEP 2 — ADF TEST ON RESIDUALS

If ut is stationary (I(O) - assets are cointegrated

β₁ = hedge ratio (units of A per unit of B for market-neutral position)

# Johansen Test (Multi-Asset)

Uses Vector Error Correction Model (VECM) to identify multiple cointegrating relationships. Preferred for portfolios with 3+ assets.

Tests for rank of cointegrating vectors simultaneously.

# Ornstein-Uhlenbeck (OU) Process

$$
d s _ {t} = \lambda (\mu - s _ {t}) d t + \sigma d W _ {t}
$$

s — Spread at time t μ — Long-term mean t

λ — Mean-reversion speed σ — Spread volatility

W — Wiener processt

λ       λ reversion

# Half-Life of Mean Reversion

E[s − μ] = (s₀ − μ)e t  −λt   
Set decay to $( 1 ) ( 2 0 - 1 1 ) \times 2 = 1 0$   
Take ln: ln(½) = −λτ

$$
\tau = - \ln (2) / \lambda
$$

Estimates expected trade duration-critical for position sizing

# Spread Calculation & Z-Score Signals

# Spread Calculation

$$
S p r e a d = P _ {B} - (\beta_ {1} \cdot P _ {A} + \beta_ {0})
$$

β₁ is the OLS-derived hedge ratio measuring deviation from the long-run equilibrium.

# Z-Score Normalization

$$
z = (S p r e a d _ {t} - \mu_ {s p r e a d}) / \sigma_ {s p r e a d}
$$

SHORT spread: z > +2.0

Sell B, Buy A

LONG spread: z < −2.0

Buy B, Sell A

CLOSE: z ≈ 0

Exit both legs

STOP LOSS: |z| > 3.5

Emergency exit

Spread Z-Score Over Time  
![](images/13766dddef74719423c3853471fd9b3202aa28a1967a640d81ebb5ce96d69155.jpg)

<details>
<summary>line</summary>

| Trading Day | Z-Score |
| ----------- | ------- |
| 1           | 0.3     |
| 2           | 0.8     |
| 3           | 1.4     |
| 4           | 1.9     |
| 5           | 2.3     |
| 6           | 2.7     |
| 7           | 2.1     |
| 8           | 1.5     |
| 9           | 0.8     |
| 10          | 0.2     |
| 11          | -0.5    |
| 12          | -1.0    |
| 13          | -1.8    |
| 14          | -2.5    |
| 15          | -2.1    |
| 16          | -1.5    |
| 17          | -0.8    |
| 18          | -0.2    |
| 19          | 0.5     |
| 20          | 1.1     |
| 21          | 1.7     |
| 22          | 2.2     |
| 23          | 2.5     |
| 24          | 1.9     |
| 25          | 1.2     |
| 26          | 0.4     |
| 27          | -0.5    |
| 28          | -1.0    |
| 29          | -1.7    |
| 30          | -2.3    |
| 31          | -2.7    |
| 32          | -2.0    |
| 33          | -1.3    |
| 34          | -0.5    |
| 35          | 0.2     |
| 36          | 0.7     |
| 37          | 1.3     |
| 38          | 0.8     |
| 39          | 0.3     |
| 40          | 0.0     |
</details>

# Implementation: Step-by-Step Process

# 01 Pair Selection

Screen for economic linkage (same industry, ETF vs. components). Filter by correlation > 0.8 over 1-year lookback.

# 02 Cointegration Testing

Run Engle-Granger ADF test. Validate p-value < 0.05. Estimate β₁ hedge ratio via OLS regression.

# OU Parameter Estimation

Fit OU process to spread. Compute mean-reversion speed λ and half-life τ = −ln(2)/λ. Accept τ < 30 days.

# 04 Signal Generation

Calculate z-score in real-time. Trigger LONG spread at z < −2, SHORT at z +2

# Execution & Exit

Submit simultaneous market or limit orders for both legs. Exit when |z| < 0.5 or stop-loss at |z| > 3.5.

# Execution Notes

吕 Use co-location for microsecond execution   
Re-estimate β₁ every 30–60 days (rolling window)   
个 Monitor for regime change cointegration can break   
《 Trade 20–50 pairs simultaneously for diversification   
B Platforms: Horizon, MT5, proprietary quant engines

# Case Studies: Elite Stat Arb Firms

# Renaissance Technologies

Medallion Fund · Founded 1982

Pure mathematical/statistical models; hires physicists and mathematicians, not traditional traders.

Key Signal: Short-term meanreversion across equities, FX, futures thousands of pairs simultaneously.

Performance \~66% ann. return Sharpe \~4.0+

Proprietary signal discovery from non-financial datasets

# D.E. Shaw & Co.

Composite Fund · Founded 1988

Systematic multi-strategy: stat arb, macro, credit. Heavy use of VECM for multi-asset cointegration.

Key Signal: Cross-asset pairs: equities vs. ETFs, convertible bonds vs. equities.

Performance \~25% ann. Sharpe \~2.5–3.0

Statistical signals + fundamental screening

# Two Sigma Investments

Spectrum Fund · Founded 2001

Machine learning overlaid on stat arb. Uses NLP and alternative data to strengthen cointegration signals.

Key Signal: ML-enhanced pair selection; dynamic hedge ratio β₁ updated intraday.

Performance \~17–20% ann. Sharpe \~2.0–3.0

ML Real-time β₁ recalibration with Kalman filter

# Performance Metrics & Key Risks

# Critical Risks

![](images/cb35a8d8bc4d80120ea86d1bd1f51fc278ed39a1be55a1e4165323c74b4539af.jpg)

# Regime Change

HIGH

Economic relationship breaks permanently. Spread diverges without mean-reversion.

![](images/b5fe0d6909f3bd86df9d104959b62745ff06e55350c027497f028fb5da1a90a5.jpg)

# Correlation Breakdown

HIGH

Short-term correlation falters during market stress (e.g., 2008 crisis).

![](images/f06fb4fbdec918938574ff40f8356d854329ab90dd78c642f8cbeb3a66e8e79d.jpg)

# Crowding Risk

MEDIUM

As the strategy becomes well-known, edge erodes due to competition.

Mitigation: Rolling re-estimation of cointegration parameters every 30-60 days

Sharpe Ratio by Firm   
![](images/33e9f67d98897452a79afd318b618b08fc1054054f238bcc630d0185dd430dfb.jpg)

<details>
<summary>bar</summary>

| Category               | Sharpe Ratio |
| ---------------------- | ------------ |
| Renaissance (Medallion) | 4.2          |
| D.E. Shaw              | 2.8          |
| Two Sigma              | 2.5          |
| Millennium Mgmt        | 2.2          |
| Industry Avg (Stat Arb)| 1.5          |
</details>

# Volatility Arbitrage — Gamma Scalping

Core Idea: Profit from the gap between Implied Volatility (IV) and Realized Volatility (RV).

Mechanism: Buy options (long gamma, long vega) when IV is cheap. Delta-hedge continuously to eliminate directional risk. Collect profit as the underlying moves more than IV predicted.

VRP Insight: Historically, IV trades \~2–4 vol points above future RV — a persistent, exploitable mispricing.

# Industry Leaders

![](images/eaa6dcd1890ee5489d85d0746bd5c0697c438453fd04e14c86d720f210aa4d58.jpg)

Citadel

Options / Vol Arb

![](images/0a3884b919966e1744a3343c2f56404010ae98f8c86749b87e5564e8aa72a9dc.jpg)

Optiver

Options MM

![](images/7fbbf4160c465b1224eb8d985f7ba8540735346439e0d496e32850be4fdeaf75.jpg)

Jane Street

ETF & Options

![](images/3fcc23f433047ddf8107dbee8c950b5ed841655be1958d8b13e98f7f13e23911.jpg)

SIG

Susquehanna

![](images/d93f1a4b40258ea0b11dc72436c5decec3948ec5d489bd2c98366576e70e98b5.jpg)

IMC Trading

Market Maker

Strategy Profile 

<table><tr><td>$</td><td>Profitability</td><td>10-100 bpsPer trade</td></tr><tr><td><img src="images/54c2a60daa7c0a54a427cdd8030f3a883ca7947c29fd24f9e838c09be8d1c9a4.jpg"/></td><td>Win Rate</td><td>50-60%Per trade</td></tr><tr><td><img src="images/d8bd8f33651baf58c5cd97401be5741d61c22f7e38e3b980c50e5cbf32dcfcf3.jpg"/></td><td>Sharpe Ratio</td><td>1.5-3Typical range</td></tr><tr><td><img src="images/4ebe601eceaa1b4a2234f18b3f5643105d4a2f9f9e50d6cb8270bc06372966f1.jpg"/></td><td>Latency</td><td>10-100 μsFor hedging</td></tr><tr><td><img src="images/30005cf560e2980442d71dfaf765d721452aa5b26d3865fbbde11d9f782bdd24.jpg"/></td><td>Primary Risk</td><td>Theta DecayDaily bleed</td></tr></table>

# Mathematical Framework: Black-Scholes & Greeks

# Black-Scholes Call Price

$$
C (S, t) = S \cdot N (d _ {1}) - K \cdot e ^ {- r (T - t)} \cdot N (d _ {2})
$$

$$
\mathrm{d} _ {1} = [ \ln (\mathrm{S} / \mathrm{K}) + (\mathrm{r} + \sigma^ {2} / 2) (\mathrm{T} - \mathrm{t}) ] / [ \sigma \sqrt {(\mathrm{T} - \mathrm{t})} ]
$$

$$
\mathrm{d} _ {2} = \mathrm{d} _ {1} - \sigma \sqrt {(\mathrm{T} - \mathrm{t})}
$$

$$
S = \text { Current   asset   price }
$$

$$
K = \text { Strike   price }
$$

$$
r = \text { Risk - free   rate }
$$

$$
\sigma = \text { Implied   volatility }
$$

$$
T - t = \text { Time   to   expiry }
$$

$$
N (\cdot) = \text { Cumulative   normal   CDF }
$$

# The Core Trade

"Buy when IV < Expected RV. The option is 'cheap' - the market underestimates future movement."

Volatility Risk Premium: IV − RV ≈ +2 to +4 vol points (historically)

# Δ Delta

Rate of change of option price per \$1 move in underlying

$$
\Delta = \partial C / \partial S = N (d _ {1})
$$

Delta-hedge = sell/buy underlying to stay directionally neutral

# Θ Theta

Daily cost of holding the option (time decay)

$$
\Theta = - \partial C / \partial t
$$

Primary cost for long gamma — must be offset by gamma scalping profits

# Γ Gamma

Rate of change of Delta per \$1 move in underlying

$$
\begin{array}{l} \Gamma = \partial^ {2} C / \partial S ^ {2} = N ^ {\prime} (d _ {1}) / \\ (S \sigma \sqrt {(T - t)}) \end{array}
$$

Long gamma profits from large price swings — the source of scalping profit

# ν Vega

Price sensitivity to 1% change in IV

$$
v = \partial C / \partial \sigma = S \cdot N ^ {\prime} (d _ {1}) \sqrt {(T - t)}
$$

Must be monitored — IV spike creates vega losses if unhedged

# Delta-Hedging P&L: The Gamma Scalping Engine

# Delta-Hedged P&L Formula

$$
P \& L \approx \frac {1}{2} \Gamma \cdot (\Delta S) ^ {2} - \Theta \cdot \Delta t
$$

½·Γ·(ΔS)² — Gamma gain from moves

−Θ·Δt — Theta decay (daily cost)

# ✓ Profitable Scenario

$$
\mathrm{IV} = 20 \% (\text {paid}) \text {vs RV} = 28 \% (\text {realized})
$$

$$
\text { Gamma   P\&L } \propto \sigma_ {\text { RV }} ^ {2}, \text { Theta   cost } \propto \sigma_ {\text { IV }} ^ {2}
$$

$$
\text { Ratio: } (2 8 / 2 0) ^ {2} = 1. 9 6 \times \rightarrow \text { Net   profit! }
$$

# How Gamma Scalping Works

1. Buy straddle (long Γ > 0, Θ < 0)   
2. Price rises → sell shares to re-hedge   
3. Price falls → buy shares to re-hedge   
4. Each rebalance: sell high, buy low   
5. RV > IV → gamma gains > theta cost ✓

![](images/7f8a1cd2499c8a8ac0ef51a84528fcbb3e89de01399ae7aa3bbe592d5f2b0ac5.jpg)

<details>
<summary>line</summary>

| Trading Day | Price ($) |
| ----------- | --------- |
| 0           | 100       |
| 1           | 101       |
| 2           | 100.5     |
| 3           | 102.5     |
| 4           | 101       |
| 5           | 102.5     |
| 6           | 101.5     |
| 7           | 104       |
| 8           | 102       |
| 9           | 103       |
| 10          | 104       |
| 11          | 103       |
| 12          | 105       |
| 13          | 103.5     |
| 14          | 105       |
| 15          | 104.5     |
| 16          | 106       |
| 17          | 105       |
| 18          | 107       |
| 19          | 106.5     |
| 20          | 107.5     |
| 21          | 105       |
| 22          | 106.5     |
| 23          | 108       |
| 24          | 106.5     |
| 25          | 108.5     |
| 26          | 107.5     |
| 27          | 109       |
| 28          | 108.5     |
| 29          | 110       |
| 30          | 109       |
</details>

![](images/742b7ee327b086a408e1c047c89e129fa297e6d9677132775e7fedeb820ec9e2.jpg)

<details>
<summary>line</summary>

| Trading Day | Cumulative Gamma P&L | Cumulative Theta Decay | Net P&L (Gamma - Theta) |
| ----------- | -------------------- | ---------------------- | ----------------------- |
| 0           | 0.0                  | 0.0                    | 0.0                     |
| 4           | 0.2                  | -0.2                   | 0.0                     |
| 8           | 0.4                  | -0.4                   | 0.1                     |
| 12          | 0.6                  | -0.6                   | 0.2                     |
| 16          | 0.8                  | -0.8                   | 0.2                     |
| 20          | 1.0                  | -1.0                   | 0.2                     |
| 24          | 1.2                  | -1.2                   | 0.3                     |
| 28          | 1.4                  | -1.4                   | 0.3                     |
| 32          | 1.5                  | -1.5                   | 0.3                     |
</details>

# Implementation: Gamma Scalping Process

# Identify IV Undervaluation

Screen options where IV < 30-day historical RV. Use CBOE VIX term structure or proprietary vol forecasting model.

# 02 Enter Long Straddle

Buy ATM call + ATM put. Initial delta ≈ 0. Position is long Γ, long ν, short Θ.

# 03 Dynamic Delta-Hedging

Rebalance underlying every time |Δ| exceeds threshold (e.g., 0.05). Sell when Δ > 0, buy when Δ < 0.

# 04 Monitor Greeks Daily

Track Θ bleed vs. Γ gains. If Γ gains < Θ cost consistently, exit position early.

# 05 Exit Strategy

Close when: (a) IV rises toward target, (b) expiry approaches (gamma risk spikes), (c) stop-loss triggered.

# Key Execution Considerations

Hedge frequency: balance transaction costs vs. gamma capture

Gary's CBBC model (Morgan Stanley, 2018): AI-predicted IV vs. RV gap

Watch: Pin risk near expiry, gap risk overnight

10–100μs execution for competitive hedging

B Ref:Bakshi R &Kapadia (2003)- Negative VRP evidence

# Case Studies & Key Risks

# Industry Leaders

# Citadel

Multi-asset vol arb Continuous deltahedging with MLdriven IV forecasting. Trades VIX derivatives alongside equity options.

Sharpe: \~3.0+ Edge: Real-time IV recalibration

# Optiver

Options MM, Amsterdam Sub-ms gamma scalping on equity and commodity options. Manages thousands of positions simultaneously.

Sharpe: \~2.5 Edge: FPGA-based option pricer

# SIG

Susquehanna Deep expertise in volatility modeling. Trains traders in probability theory and game theory.

Sharpe: \~2.0–2.5 Edge: Behavioral vol modeling

IV vs. RV- The Volatility Risk Premium   
![](images/8281eeceaa847dd2db69f7364a9b333c8a5fb8a98a273df6e0e499337c6d961d.jpg)

<details>
<summary>line</summary>

| Month | Implied Volatility (IV) | Realized Volatility (RV) |
|-------|--------------------------|---------------------------|
| M1    | 18.0                     | 15.0                      |
| M2    | 20.0                     | 17.0                      |
| M3    | 22.0                     | 19.0                      |
| M4    | 19.0                     | 16.0                      |
| M5    | 21.0                     | 18.0                      |
| M6    | 24.0                     | 21.0                      |
| M7    | 28.0                     | 25.0                      |
| M8    | 32.0                     | 28.0                      |
| M9    | 27.0                     | 23.0                      |
| M10   | 22.0                     | 18.0                      |
| M11   | 19.0                     | 16.0                      |
| M12   | 17.0                     | 14.0                      |
| M13   | 18.0                     | 15.0                      |
| M14   | 21.0                     | 18.0                      |
| M15   | 23.0                     | 20.0                      |
| M16   | 20.0                     | 17.0                      |
| M17   | 22.0                     | 19.0                      |
| M18   | 25.0                     | 22.0                      |
| M19   | 30.0                     | 26.0                      |
| M20   | 35.0                     | 30.0                      |
| M21   | 29.0                     | 25.0                      |
| M22   | 24.0                     | 20.0                      |
| M23   | 20.0                     | 17.0                      |
| M24   | 18.0                     | 15.0                      |
</details>

# Critical Risks in Gamma Scalping

![](images/667caafa89b9d8fd307af0389f42f6f82bf7b9e09b81e5a27a39ed3752a6e9cb.jpg)

HIGH

# Vol Regime Shifts

A sudden drop in realized volatility means gamma gains fail to cover theta decay. The trade loses money each day.

Example: Post-earnings IV crush IV drops 40% immediately after earnings release

Mitigation: Use VIX futures to hedge vega exposure. Limit position size near earnings.

√ Θ  Γ

![](images/f88311493adff08704d0429ccd03653e22e0504551bddfd1aaabd6fc08b504eb.jpg)

MEDIUM

# Pin Risk

Near expiry, underlying hovers at strike price. Gamma spikes to infinity — delta becomes binary (0 or 1). Hedging becomes impossible. Example: SPY options pinning at round number strikes on monthly expiry

Mitigation: Roll positions to next expiry 2–5 days before expiration. Never hold to expiry.

![](images/0a1706cfff469629a1875bd250e737be441193daa216ac431ad603b743e7ec0c.jpg)

HIGH

# Gap Risk

Underlying gaps overnight — opens significantly above/below close. Delta hedge is bypassed; position suffers large unhedged directional loss.

Example: Flash Crash 2010- SPY dropped 9% intraday; gamma scalpers caught long delta

Mitigation: Use stop-loss orders. Maintain overnight positions only within VaR limits.

# Liquidity Provision — Market Making

Core Idea: Post simultaneous bid and ask orders; profit from the bid-ask spread on every completed round-trip.

Scale: Virtu Financial: \~1 losing day in 1,238 consecutive days — proof of scaledriven consistency.

Economic Role: Market makers tighten spreads and enable price discovery. Regulatory alignment makes this durable.

1 bps spread × 10M shares × 1,000 trades/day = substantial daily P&L

# Industry Leaders

Virtu Financial Public HFT firm

Citadel Securities Market Making Arm

曲 Jane Street ETF & Options

色 Jump TradingProp Trading

曲 IMC Trading Amsterdam-based

# Strategy Profile

\$

Profitability

0.5–5 bps

Per trade

@

Win Rate

51–53%

Per trade

Sharpe Ratio

3–6 Highest in HFT

Latency

<1 μs Sub-microsecond

山

Trades/Day

Billions Scale is the edge

# The Avellaneda-Stoikov Market Making Model

A stochastic control framework that maximizes expected terminal utility by optimally setting bid/ask quotes.

Balances: (1) capturing the spread, (2) minimizing inventory risk

Avellaneda & Stoikov (2oo8), Quantitative Finance

# Reservation Price r(s, q, t)

$$
r (s, q, t) = s - q \gamma \sigma^ {2} \cdot (T - t)
$$

s = Mid-market price

q = Current inventory

γ = Risk aversion

σ² = Asset variance

(T−t) = Remaining horizon

q > 0 (long): r < s → shift quotes down to attract sellers

q < 0 (short): r > s → shift quotes up to attract buyers

Inventory skew automatically adjusts quotes to reduce position risk

# Optimal Bid-Ask Spread δ

$$
\delta = \gamma \sigma^ {2} (T - t) + (2 / \gamma) \cdot l n (1 + \gamma / \kappa)
$$

γ·σ²·(T−t) — Inventory risk compensation

(2/γ)·ln(1+γ/κ) — Adverse selection compensation

κ = Order arrival intensity

# Final Quote Placement

$$
\mathrm{Ask} = \mathrm{r} + \delta
$$

$$
\mathrm{Bid} = \mathrm{r} - \delta
$$

# Worked Example

$$
s = 1 0 0, q = + 5, \gamma = 0. 1, \sigma^ {2} = 0. 0 4, T - t = 1
$$

$$
r = 1 0 0 - 5 \times 0. 1 \times 0. 0 4 \times 1 = 9 9. 9 8
$$

$$
\delta = 0. 0 4 \rightarrow \text {Bid} = 9 9. 9 4, \text {Ask} = 1 0 0. 0 2
$$

Quotes shift below mid-price when long-MM wants to sell to reduce inventory

# Implementation: Market Making Cycle

# 01 Real-Time Quote Calculation

Compute reservation price r(s,q,t) and optimal spread δ using live market data. Update every microsecond.

# 02 Quote Submission

Post limit orders: Bid = r − δ, Ask = r + δ. Both sides of book simultaneously.

# 03 Fill Monitoring

Track order fills. Each fill changes inventory q. Immediately recalculate r based on new q.

# 04 Inventory Skewing

If |q| exceeds threshold, shift both quotes in direction that reduces inventory. Accept tighter spread to reduce risk.

# 05 Adverse Selection Defense

Use Order Flow Imbalance (OFI) signal: if buy pressure dominates, raise ask price. Cancel quotes ahead of informed flow.

# Execution Considerations

Sub-microsecond latency — colocation mandatory

FPGA hardware for order submission (nanoseconds)

OFI = (Bid volume change − Ask volume change)

Cancel and re-quote if OFI signals informed trader

山 Target: >60% win rate via spread capture

Technology failure risk: catastrophic without failsafe

# Order Book Structure & Quote Skewing

Limit Order Book Depth (Spread = \$0.02)   
![](images/0efe89a0e2fd1ce56b9755162e18f6de740365c222fb1f38e4843863c52f44a7.jpg)

<details>
<summary>bar</summary>

| Price Level ($) | Bid Volume | Ask Volume |
| --------------- | ---------- | ---------- |
| 99.94           | 500        | -          |
| 99.95           | 800        | -          |
| 99.96           | 1200       | -          |
| 99.97           | 900        | -          |
| 99.98           | 600        | -          |
| Mid $99.99      | -          | -          |
| 100.00          | -          | 550        |
| 100.01          | -          | 750        |
| 100.02          | -          | 1100       |
| 100.03          | -          | 850        |
| 100.04          | -          | 500        |
</details>

Quote Skewing by Inventory Level   
![](images/5c173e7c8b2e4a888ccc39463d7ac3cddf25acbbbe39db287ead7f53d082da25.jpg)

<details>
<summary>bar</summary>

| Inventory State       | Bid Price | Ask Price |
| --------------------- | --------- | --------- |
| Normal (q=0)          | $99.96    | $100.02   |
| Long Inv. (q=+10)    | $99.92    | $99.98    |
| Short Inv. (q=-10)   | $100.00   | $100.06   |
</details>

# Case Studies: Virtu Financial & Citadel Securities

# Virtu Financial

Publicly traded HFT market maker (VIRT) · Founded 2008

# 1 losing day in 1,238 consecutive trading days

Trades \~25,000 instruments across 235 venues in 50+ countries   
\$ Spread capture × volume. Revenue uncorrelated with market direction.   
Sharpe: \~5–6 realized   
Sub-microsecond execution; owns fiber-optic networks

Scale + speed + diversification = near-zero variance in daily P&L

# Citadel Securities

Subsidiary of Citadel LLC (Ken Griffin)

# \~28% of US retail equity volume · #1 US options MM

Revenue 2022: \~\$7 billion   
Internalizes retail order flow (PFOF model). Proprietary vol models for hedging.   
Sharpe: \~4.0–5.0 estimated   
Custom silicon chips; direct exchange membership in 40+ markets

Retail flow internalization + institutional MM = unparalleled scale

# Performance & Risk Management

# Critical Risks

![](images/499b65e5986a8edb2c87f2e933e478df80b734db18e42f2535854f6ac9d868ea.jpg)

# Adverse Selection

# CRITICAL

Informed traders pick off stale quotes. Primary source of losses. Defense: OFI signal, rapid cancel-andrequote.

![](images/3ccedc7e5fdd841ec134d0c7c3a0ae889b99ea936e0307dab094f19684a91ea6.jpg)

# Inventory Risk

# HIGH

Accumulated long/short position from imbalanced fills. Defense: A-S model quote skewing + hard inventory limits.

![](images/b4102745257068c07d741ee809917103710ed0335df2051b4128dff7f242086a.jpg)

# Technology Failure

# HIGH

Hardware, network, or software failure can cause flash crash-level losses in milliseconds. Defense: redundant systems, circuit breakers.

Strategy Comparison: Part 1 Summary   
![](images/b818b2b99ca5c7793d92482a38f09e21179e06a7715dd3f2c0a7ac7841c207cd.jpg)

<details>
<summary>bar</summary>

Note: Bps/Trade values shown for relative comparison
| Strategy | Sharpe Ratio | Win Rate (%) | Bps/Trade (×10) |
| :--- | :--- | :--- | :--- |
| Stat Arb | 3 | 60 | 27 |
| Vol Arb | 2.2 | 55 | 55 |
| Market Making | 4.5 | 52 | 2.5 |
</details>

Part 1 Summary: Strategy Comparison   
Recap 

<table><tr><td>Dimension</td><td>Statistical Arbitrage</td><td>Volatility Arbitrage</td><td>Market Making</td></tr><tr><td>Core Mechanism</td><td>Mean-reversion of cointegrated spread</td><td>IV vs. RV differential via gamma scalping</td><td>Bid-ask spread capture at scale</td></tr><tr><td>Mathematical Core</td><td>OU Process, Z-Score, ADF</td><td>Black-Scholes Greeks, ΔHedge P&amp;L</td><td>Avellaneda-Stoikov Model</td></tr><tr><td>Profitability</td><td>5–50 bps/trade</td><td>10–100 bps/trade</td><td>0.5–5 bps/trade</td></tr><tr><td>Win Rate</td><td>55–65%</td><td>50–60%</td><td>51–53%</td></tr><tr><td>Sharpe Ratio</td><td>2–4</td><td>1.5–3</td><td>3–6</td></tr><tr><td>Latency Required</td><td>1–10 μs</td><td>10–100 μs</td><td>&lt;1 μs</td></tr><tr><td>Primary Risk</td><td>Regime / correlation breakdown</td><td>Theta decay, gap risk</td><td>Adverse selection</td></tr><tr><td>Key Firms</td><td>Renaissance, D.E. Shaw, Two Sigma</td><td>Citadel, Optiver, SIG</td><td>Virtu, Citadel Securities, Jane Street</td></tr></table>

Allthree strategies profitfromgenuinemarketinefficiencies-nomanipulationfullregulatoryalignment.

Speed + Mathematical Rigor + Risk Management = Sustainable Edge

# Academic Foundations & Key References

# Peer-Reviewed Literature

Gatev, Goetzmann & Rouwenhorst (2006)   
Pairs Trading: Performance of a Relative-Value Arbitrage Rule   
Review of Financial Studies   
FOUNDATIONAL PAIRS TRADING BACKTESTING

Bakshi & Kapadia (2003)   
Delta-Hedged Gains & the Negative Market Volatility Risk Premium   
Review of Financial Studies   
VRP EVIDENCE FOR GAMMA SCALPING

Avellaneda & Stoikov (2008)   
High-Frequency Trading in a Limit Order Book   
Quantitative Finance   
A-S MARKET MAKING MODEL

Brogaard, Hendershott & Riordan (2014)   
High-Frequency Trading and Price Discovery   
Review of Financial Studies   
HFT'S ROLE IN PRICE EFFICIENCY

# Regulatory & Practitioner Sources

SEC Enforcement Report (2015)   
Spoofing and Layering Enforcement Actions

CFTC Enforcement Report (2015–2020)

Market Manipulation Cases

Easley, López de Prado & O'Hara (2016) The Microstructure of the Flash Crash — VPIN model

# Key Microstructure Principles

Legal strategies contribute to price discovery   
Inventory risk drives quote skewing (legal)   
Adverse selection separates informed vs. uninformed flow

# Discussion Questions & Exercises

# Statistical Arbitrage

Q1 Given λ = 0.023, calculate the half-life τ. Is this pair tradeable with a 30-day horizon?   
Q2 Two stocks have r = 0.91 correlation but fail the ADF test. Can you trade them? Why/why not?   
Q3 How would you adjust the z-score threshold during a high-volatility regime?

# Volatility Arbitrage

Q4 An ATM straddle costs \$3.50. Γ = 0.04, Θ = −\$0.08/day. What daily move breaks even?   
Q5 IV = 25%, expected RV = 20%. Should you buy or sell options? What's the expected VRP capture?   
Q6 At what frequency should you delta-hedge given transaction costs of 0.5 bps/share?

# Market Making

Q7 Given s = \$50, q = −8, γ = 0.1, σ² = 0.02, T−t = 0.5: Compute r and optimal quotes.   
Q8 Order flow shows 70% buy-side imbalance. How do you adjust your quotes? Derive using OFI.   
Q9 Virtu trades 25,000 instruments. How does diversification reduce inventory risk mathematically?

# Part 1 Complete — Up Next: Part 2

Statistical Arbitrage (Pairs Trading)

✓ Volatility Arbitrage (Gamma Scalping)

Liquidity Provision (Market Making)

# 04 Cross-Venue Arbitrage Latency Arbitrage

> exchanges Price discrepancies across HK, US, Singapore   
Microsecond speed advantage   
Key firms: Virtu, Citadel, Jump Trading   
70–85% win rate, 1–10 bps/trade

Critical Latency (<microseconds)

# 05 Order Flow Prediction Machine Learning

ML models on L2 order book imbalance   
VPIN, trade intensity signals   
Key firms: Citadel, Millennium, Optiver   
52–58% win rate, 2–20 bps/trade

High Latency (100–500ms)

InPart2ttilooitctrcreee complete regulatory framework separating legal strategies from market manipulation.

Gary · Visiting Lecturer · PolyU Dept. of Applied Mathematics

HFT Strategies: Legal vs. Illegal — Master-Level Training