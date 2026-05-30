# Greeks, Delta Hedging, and Volatility Trading

Lecture Notes — AMA568 Advanced Topics in Quantitative Finance

Andy Lian

Department of Applied Mathematics

The Hong Kong Polytechnic University

Semester 2, 2025/26

# Contents

# I Greeks and the Black–Scholes–Merton Framework 3

# 1 The Greeks 3

1.1 Formulae for European Option Greeks . 3   
1.2 Delta (∆) 3   
1.3 Gamma (Γ) . 4   
1.4 Vega (ν) . . 4   
1.5 Theta (Θ) 4   
1.6 Rho (ρ) 5

# 2 The Black–Scholes–Merton Model: A Trader’s Perspective 5

2.1 Properties of an Option 5   
2.2 Delta Hedging: The Core Idea 5   
2.3 From Hedged P/L to the BSM Equation 6   
2.4 Two Ways to Use the BSM Framework . . 6

# 3 Volatility Measurement and Forecasting 6

3.1 Definition of Volatility . . . 7   
3.2 Alternative Volatility Estimators 7   
3.3 Forecasting Volatility . . . 7

3.3.1 Exponentially Weighted Moving Average (EWMA) . . 7   
3.3.2 GARCH(1,1) Model 8

# 4 Trading Volatility: Implied vs. Realised 8

4.1 Hedging Rules and Frequencies 8

4.1.1 Hedging at Regular Intervals 8

4.1.2 Hedging to a Delta Band 8

4.2 Path Dependency of Discrete Hedging . . . 8

4.3 PnL of Delta-Hedged Options When σi ̸= σr . . . . 9   
4.4 Summary: Delta-Hedged Option P/L . 9

# II Delta Hedging Experiments via Monte Carlo Simulation 10

# 5 Overview 10

# 6 Gamma PnL: Formal Derivation 10

6.1 The Black–Scholes PDE and Greeks . . . . 10   
6.2 The Delta-Hedged Portfolio 10   
6.3 Instantaneous Gamma PnL . 10   
6.4 Expected PnL . . 11

# 7 Simulation Setup 1 1

7.1 Parameters 11   
7.2 Volatility Scenarios . . 11   
7.3 Black–Scholes Call Prices . . 12

# 8 Experiment 1: Constant Realised Volatility (σreal = 50%) 12

8.1 Sample Path . . 12   
8.2 Delta-Hedged PnL 12   
8.3 Cumulative Gamma PnL . . 13   
8.4 Daily Gamma PnL Decomposition 13   
8.5 Summary: Constant Volatility . . . 14

# 9 Experiment 2: Transaction Costs 14

# 10 Experiment 3: Regime-Switching Volatility 1 5

10.1 Motivation . 15   
10.2 Sample Paths . . 16   
10.3 PnL Comparison: Regime vs. Constant 16   
10.4 Why Is the Regime PnL So Different? 17   
10.5 Cumulative Gamma PnL . . 17   
10.6 Daily Gamma PnL 18   
10.7 Transaction Costs: Regime Path . . 18

# 11 Key Takeaways 19

# Part I

# Greeks and the Black–Scholes–Merton Framework

# 1 The Greeks

In mathematical finance, the Greeks are the quantities (partial derivatives, first-order or higher) representing the sensitivity of the price of a derivative instrument to changes in one or more underlying parameters.

The Greeks are vital tools in risk management. Each Greek measures the sensitivity of the value of a portfolio to a small change in a given underlying parameter, so that component risks may be treated in isolation and the portfolio rebalanced accordingly to achieve a desired exposure.

The most common Greeks are the first-order derivatives—Delta, Vega, Theta, Rho—and the second-order derivative Gamma.

# 1.1 Formulae for European Option Greeks

The Greeks of European options under the Black–Scholes model are calculated as follows, where $\phi ( \cdot )$ is the standard normal PDF and $\Phi ( \cdot )$ is the standard normal CDF, with

$$
d _ {1} = \frac {\ln (S / K) + (r - q + \frac {1}{2} \sigma^ {2}) \tau}{\sigma \sqrt {\tau}}, \qquad d _ {2} = d _ {1} - \sigma \sqrt {\tau}.
$$

Table 1: Black–Scholes Greeks for European calls and puts 

<table><tr><td>Greek</td><td>Calls</td><td>Puts</td></tr><tr><td>Value V</td><td> $Se^{-q\tau}\Phi(d_1) - Ke^{-r\tau}\Phi(d_2)$ </td><td> $Ke^{-r\tau}\Phi(-d_2) - Se^{-q\tau}\Phi(-d_1)$ </td></tr><tr><td>Delta Δ</td><td> $e^{-q\tau}\Phi(d_1)$ </td><td> $-e^{-q\tau}\Phi(-d_1)$ </td></tr><tr><td>Gamma Γ</td><td></td><td> $e^{-q\tau} \frac{\phi(d_1)}{S\sigma\sqrt{\tau}}$ </td></tr><tr><td>Vega ν</td><td></td><td> $Se^{-q\tau}\phi(d_1)\sqrt{\tau}$ </td></tr><tr><td>Theta Θ</td><td> $-e^{-q\tau} \frac{S\phi(d_1)\sigma}{2\sqrt{\tau}} - rKe^{-r\tau}\Phi(d_2) + qSe^{-q\tau}\Phi(d_1)$ </td><td> $-e^{-q\tau} \frac{S\phi(d_1)\sigma}{2\sqrt{\tau}} + rKe^{-r\tau}\Phi(-d_2) - qSe^{-q\tau}\Phi(-d_1)$ </td></tr><tr><td>Rho ρ</td><td> $K\tau e^{-r\tau}\Phi(d_2)$ </td><td> $-K\tau e^{-r\tau}\Phi(-d_2)$ </td></tr></table>

# 1.2 Delta (∆)

Delta measures the rate of change of the option value with respect to changes in the underlying asset’s price:

$$
\Delta = \frac {\partial V}{\partial S}.
$$

Delta is always positive for long calls and negative for long puts. The total delta of a complex portfolio is linear in the constituents—simply sum the deltas of each individual position.

# Delta as a Probability Proxy

The absolute value of delta is close to the implied probability that the option expires in-themoney (under the risk-neutral measure). For example:

• An OTM call with ∆ = 0.15: ≈15% chance of expiring ITM.   
• A put with ∆ = −0.25: ≈25% chance of expiring ITM.   
• ATM calls/puts have $\Delta \approx \pm 0 . 5 .$ .

# 1.3 Gamma (Γ)

Gamma measures the rate of change of delta with respect to the underlying price:

$$
\Gamma = \frac {\partial^ {2} V}{\partial S ^ {2}}.
$$

• Most long options have positive gamma; most short options have negative gamma.   
• Gamma is greatest at-the-money (ATM) and diminishes further OTM or ITM.   
• Gamma is important because it corrects for the convexity of the option value function.

# 1.4 Vega (ν)

Vega measures sensitivity to volatility:

$$
\nu = \frac {\partial V}{\partial \sigma}.
$$

All options (both calls and puts) gain value with rising volatility. Vega is typically quoted as the dollar change per 1 percentage-point change in implied volatility. ATM straddle values are extremely vega-sensitive.

# 1.5 Theta (Θ)

Theta measures the sensitivity of the option value to the passage of time—the “time decay”:

$$
\Theta = \frac {\partial V}{\partial t}.
$$

As time passes with decreasing time to expiry, an option’s extrinsic value decreases. Long options typically have negative theta (they lose value over time, all else equal).

By convention, $\tau = T - t$ is measured in years, but practitioners often divide Θ by 252 (or 365) to express decay per trading (or calendar) day.

# 1.6 Rho (ρ)

Rho measures sensitivity to the risk-free interest rate:

$$
\rho = \frac {\partial V}{\partial r}.
$$

Except under extreme circumstances, option values are less sensitive to interest rate changes than to other parameters. Rho is the least-used first-order Greek.

# 2 The Black–Scholes–Merton Model: A Trader’s Perspective

While rigorous derivations carefully walk us through the mathematics, they don’t always make it obvious what to do as a trader. Our goal is to identify and profit from mispriced options. Here we approach the BSM framework from the perspective of a delta-hedged portfolio.

# 2.1 Properties of an Option

Even before making distributional assumptions, a number of financially obvious properties hold:

• A call (put) becomes more valuable as the underlying rises (falls).   
• An option loses value as time passes (less time to become intrinsically valuable).   
• The value of a call (put) can never exceed the value of the underlying (strike).

# 2.2 Delta Hedging: The Core Idea

Assume we hold a delta-hedged option position:

$$
\Pi = C - \Delta S _ {t},
$$

where C is the option value, $S _ { t }$ the underlying price, and $\Delta$ the number of shares shorted.

Over one time step, the underlying changes to $S _ { t + 1 }$ . The change in portfolio value is:

$$
\underbrace {C (S _ {t + 1}) - C (S _ {t})} _ {\text {option P / L}} - \underbrace {\Delta (S _ {t + 1} - S _ {t})} _ {\text {hedge P / L}} + \underbrace {r (C - \Delta S _ {t})} _ {\text {financing}}.
$$

Using a second-order Taylor expansion for the option price change and denoting $\delta S = S _ { t + 1 } - S _ { t }$

$$
C (S _ {t + 1}) - C (S _ {t}) \approx \Delta   \delta S + \frac {1}{2} \Gamma (\delta S) ^ {2} + \Theta   \delta t. \tag {1}
$$

The $\Delta \delta S$ terms cancel, leaving:

$$
\boxed {\text {Hedged P / L} = \frac {1}{2} (\delta S) ^ {2} \Gamma + \Theta + r (C - \Delta S _ {t}).} \tag {2}
$$

# Three Components of the Hedged P/L

1. Gamma effect: $\frac { 1 } { 2 } ( \delta S ) ^ { 2 } \Gamma > 0$ for long options — profit from convexity.   
2. Theta effect: $\Theta < 0$ for long options — cost of carrying optionality.   
3. Financing effect: $r ( C - \Delta S _ { t } )$ — interest on the net investment.

# 2.3 From Hedged P/L to the BSM Equation

Since $( \delta S ) ^ { 2 } \approx \sigma ^ { 2 } S ^ { 2 } \delta t$ , the hedged P/L becomes:

$$
\frac {1}{2} \sigma^ {2} S ^ {2} \Gamma + \Theta + r (C - \Delta S _ {t}).
$$

If this riskless, fully-financed position earns no abnormal profit, we set it to zero:

$$
\boxed {\frac {1}{2} \sigma^ {2} S ^ {2} \Gamma + \Theta + r (C - \Delta S) = 0.} \tag {3}
$$

This is the Black–Scholes–Merton PDE expressed in Greek notation.

# Key Insight: No Drift Dependence

The option price does not depend on the drift $\mu$ of the underlying. While the price change δS does not appear (it cancels via hedging), the square of the price change does—through the volatility σ. This is remarkable and is the foundation of risk-neutral pricing.

# 2.4 Two Ways to Use the BSM Framework

Given that the fair option price is determined by σ, a trader can proceed in two ways:

1. From option price → implied volatility. Using the quoted market price, back out the implied $\sigma .$   
2. From volatility estimate → theoretical price. Using a forecast of future realised volatility, calculate a fair option value.

If the trader’s volatility forecast differs significantly from the market-implied volatility, there is a trading opportunity: buy (sell) options when implied vol is below (above) the forecast, and delta hedge to isolate the volatility bet.

# 3 Volatility Measurement and Forecasting

To trade the spread between implied and realised volatility, we first need to measure and forecast volatility.

# 3.1 Definition of Volatility

The standard definition is the square root of the variance:

$$
s ^ {2} = \frac {1}{N} \sum_ {i = 1} ^ {N} (x _ {i} - \bar {x}) ^ {2}, \tag {4}
$$

where $x _ { i }$ are logarithmic returns, x¯ is the mean return, and N is the sample size. To annualise, multiply by the number of trading periods per year:

$$
\text { Annualised   Variance } = s ^ {2} \times N _ {\text { periods / year }}.
$$

For daily data, $N _ { \mathsf { p e r i o d s / y e a r } } = 2 5 2 .$

# 3.2 Alternative Volatility Estimators

The Parkinson (1980) estimator uses high-low range data:

$$
\sigma_ {\text { Parkinson }} = \sqrt {\frac {1}{4 N \ln 2} \sum_ {i = 1} ^ {N} \left(\ln \frac {h _ {i}}{l _ {i}}\right) ^ {2}}, \tag {5}
$$

where $h _ { i }$ and $l _ { i }$ are the high and low prices. It is more efficient than close-to-close volatility, but is biased in finite samples:

Table 2: Sampling bias in Parkinson variance (ratio to true variance) 

<table><tr><td>Sample Size</td><td>Parkinson / True Variance</td></tr><tr><td>5</td><td>0.55</td></tr><tr><td>10</td><td>0.65</td></tr><tr><td>20</td><td>0.74</td></tr><tr><td>50</td><td>0.82</td></tr><tr><td>100</td><td>0.86</td></tr><tr><td>200</td><td>0.92</td></tr></table>

# 3.3 Forecasting Volatility

# 3.3.1 Exponentially Weighted Moving Average (EWMA)

The simplest forecasting method assumes tomorrow’s variance is a weighted combination of today’s estimate and today’s squared return:

$$
\sigma_ {t} ^ {2} = \lambda \sigma_ {t - 1} ^ {2} + (1 - \lambda) r _ {t - 1} ^ {2}, \tag {6}
$$

where $\lambda \in ( 0 , 1 )$ controls the decay rate (RiskMetrics uses $\lambda = 0 . 9 4$ for daily data).

# 3.3.2 GARCH(1,1) Model

The ${ \mathsf { G A R C H } } ( 1 , 1 )$ model adds mean reversion:

$$
\sigma_ {t} ^ {2} = \omega + \alpha r _ {t - 1} ^ {2} + \beta \sigma_ {t - 1} ^ {2}, \tag {7}
$$

with the stationarity condition $\alpha + \beta < 1$ . The long-run variance is $\sigma _ { \infty } ^ { 2 } = \omega / ( 1 - \alpha - \beta )$ .

# 4 Trading Volatility: Implied vs. Realised

# 4.1 Hedging Rules and Frequencies

# 4.1.1 Hedging at Regular Intervals

The simplest strategy: at the end of each fixed time period, execute an underlying trade that sets the portfolio delta to zero.

# 4.1.2 Hedging to a Delta Band

The Whalley–Wilmott asymptotic solution gives an optimal no-trade band around the BS delta:

$$
\Delta_ {\text { hedge }} = \frac {\partial V}{\partial S} \pm \left(\frac {3 e ^ {- r (T - t)} \lambda S T ^ {2}}{2 \gamma}\right) ^ {1 / 3}, \tag {8}
$$

where λ is the transaction cost rate and $\gamma$ is the risk-aversion parameter.

# 4.2 Path Dependency of Discrete Hedging

The profit/loss for discrete delta hedging is:

$$
\mathsf {P} / \mathsf {L} = \sum_ {i = 1} ^ {N} \left[ C (t _ {i}) - C (t _ {i - 1}) \right] - \Delta (t _ {i - 1}) \left[ S (t _ {i}) - S (t _ {i - 1}) \right]. \tag {9}
$$

Table 3: Effect of hedging frequency (100 simulations, ATM call, $\sigma _ { i } = \sigma _ { r } = 3 0 \% )$ 

<table><tr><td>Hedge Frequency</td><td>Mean P/L</td><td>σ P/L</td><td>Kurtosis</td><td>Skew</td></tr><tr><td>Daily</td><td>-107</td><td>2,615</td><td>4.05</td><td>0.25</td></tr><tr><td>Weekly</td><td>-140</td><td>5,715</td><td>3.66</td><td>0.16</td></tr></table>

Key observations:

• The average P/L is approximately zero (the option is fairly priced).   
• The distribution is roughly normal.   
• Dispersion scales as $N ^ { - 1 / 2 }$ —more frequent hedging reduces noise.

# 4.3 PnL of Delta-Hedged Options When $\sigma _ { i } \neq \sigma _ { r }$

When we sell an option at implied volatility $\sigma _ { i }$ and hedge at realised volatility $\sigma _ { r _ { \mathrm { i } } }$ , the one-step profit is:

$$
\frac {1}{2} \left(\sigma_ {i} ^ {2} - \sigma_ {r} ^ {2}\right) S ^ {2} \Gamma d t. \tag {10}
$$

# Implications of the Gamma PnL Formula

• We make money if $\sigma _ { i } > \sigma _ { \ i }$ (sold expensive vol), but the profit arrives stochastically, not smoothly.   
• The accumulated profit is path-dependent through the weighting $S ^ { 2 } \Gamma$ .   
• The gamma is highly dependent on moneyness, so the P/L is volatile even when the vol forecast is correct.

A complementary way to think of expected profit uses the vega–gamma relationship:

$$
\nu = \sigma \tau S ^ {2} \Gamma ,
$$

so the one-step gamma PnL (10) can be rewritten as:

$$
\frac {\nu}{\sigma \tau} \left(\sigma_ {i} ^ {2} - \sigma_ {r} ^ {2}\right) d t.
$$

# 4.4 Summary: Delta-Hedged Option P/L

# Practical Realities of Volatility Trading

• Hedged option positions are highly path dependent.   
• Correctly predicting realised volatility is no guarantee of being profitable on a single trade.   
• Some variance in P/L can be reduced by hedging more frequently.   
• Hedging at realised vol makes the final P/L more certain but the path noisier.   
• Hedging at implied vol smooths the P/L path but makes the final amount more uncertain.

# Part II

# Delta Hedging Experiments via Monte Carlo Simulation

# 5 Overview

We now put the theory from Part I into practice. Using Monte Carlo simulation, we generate stock price paths and simulate daily delta hedging of a long call option. The experiments demonstrate:

(i) how the sign and magnitude of gamma PnL depend on $\sigma _ { \mathsf { r e a l } } \mathsf { v s . } \sigma _ { \mathsf { h e d g e } }$   
(ii) how transaction costs erode hedging gains, and   
(iii) how a regime-switching volatility schedule (same average, different timing) produces dramatically different outcomes.

All code and figures are generated by delta hedge all.py.

# 6 Gamma PnL: Formal Derivation

# 6.1 The Black–Scholes PDE and Greeks

Under the Black–Scholes model, a European option price $V ( S , t )$ satisfies:

$$
\underbrace {\frac {\partial V}{\partial t}} _ {\Theta} + r S \underbrace {\frac {\partial V}{\partial S}} _ {\Delta} + \frac {1}{2} \sigma^ {2} S ^ {2} \underbrace {\frac {\partial^ {2} V}{\partial S ^ {2}}} _ {\Gamma} = r V. \tag {11}
$$

# 6.2 The Delta-Hedged Portfolio

A trader who is long one call option and delta hedges by shorting ∆ shares holds:

$$
\Pi_ {t} = C (S _ {t}, t) - \Delta_ {t} \cdot S _ {t} + \mathsf {C a s h} _ {t},
$$

where the cash account finances the share position and accrues interest at rate r.

# 6.3 Instantaneous Gamma PnL

Over a small time interval dt, the change in the hedged portfolio (with r = 0 for simplicity) is:

$$
d \Pi = \Theta d t + \frac {1}{2} \Gamma (\delta S) ^ {2} = \frac {1}{2} \Gamma \left[ (\delta S) ^ {2} - \sigma_ {\text { hedge }} ^ {2} S ^ {2} d t \right], \tag {12}
$$

where we used $\begin{array} { r } { \Theta = - \frac { 1 } { 2 } \sigma _ { \mathsf { h e d g e } } ^ { 2 } S ^ { 2 } \Gamma } \end{array}$ from the BSM PDE at $r = 0$

# Key Result: Total Gamma PnL

The total PnL of a delta-hedged long option position is:

$$
\boxed {\mathsf {P n L} = \int_ {0} ^ {T} \frac {1}{2} \left(\sigma_ {\text { real }} ^ {2} - \sigma_ {\text { hedge }} ^ {2}\right) S _ {t} ^ {2} \Gamma_ {t} d t.} \tag {13}
$$

• If $\sigma _ { \mathsf { r e a l } } > \sigma _ { \mathsf { h e d g e } } \mathrm { : }$ the trader profits (bought volatility cheaply).   
• If $\sigma _ { \mathsf { r e a l } } < \sigma _ { \mathsf { h e d g e } } \mathrm { : }$ the trader loses (overpaid for volatility).

# 6.4 Expected PnL

The expected PnL is approximately:

$$
\mathbb {E} [ \mathrm{PnL} ] \approx C _ {\mathrm{BS}} (\sigma_ {\text { real }}) - C _ {\mathrm{BS}} (\sigma_ {\text { hedge }}). \tag {14}
$$

This is the difference between the “true” option value (at realised vol) and the price actually paid.

# 7 Simulation Setup

# 7.1 Parameters

Table 4: Simulation parameters 

<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Initial stock price  $S_0$ </td><td>100</td></tr><tr><td>Strike K</td><td>100 (ATM)</td></tr><tr><td>Maturity T</td><td>1 year</td></tr><tr><td>Risk-free rate r</td><td>5%</td></tr><tr><td>Rebalancing frequency</td><td>Daily (252 steps)</td></tr><tr><td>Random seed</td><td>42 (reproducible)</td></tr></table>

# 7.2 Volatility Scenarios

Table 5: Volatility scenarios and hedging volatilities 

<table><tr><td>Scenario</td><td> $\sigma_{real}$ </td><td> $\sigma_{hedge}$ </td><td> $\sigma^{2}_{real} - \sigma^{2}_{hedge}$ </td><td>Expected sign of PnL</td></tr><tr><td rowspan="2">Constant  $\sigma=50\%$ </td><td>50%</td><td>30%</td><td>+0.16</td><td>Profit</td></tr><tr><td>50%</td><td>60%</td><td>-0.11</td><td>Loss</td></tr><tr><td rowspan="2">Regime: 40%→60%</td><td>40%/60%</td><td>30%</td><td>+0.07/ + 0.27</td><td>Profit</td></tr><tr><td>40%/60%</td><td>60%</td><td>-0.20/ 0.00</td><td>Loss</td></tr></table>

# 7.3 Black–Scholes Call Prices

Table 6: BS call prices at different volatilities $( S _ { 0 } = 1 0 0 , K = 1 0 0 , T = 1 , r = 5 \% )$ 

<table><tr><td>σ</td><td> $C_{BS}$ </td><td>Theoretical PnL vs  $σ_{real}=50\%$ </td><td>Interpretation</td></tr><tr><td>30%</td><td>14.23</td><td>+7.56</td><td>Bought cheap → profit</td></tr><tr><td>50%</td><td>21.79</td><td>0</td><td>Fair value</td></tr><tr><td>51% (RMS)</td><td>22.16</td><td>—</td><td>True avg for regime case</td></tr><tr><td>60%</td><td>25.52</td><td>-3.73</td><td>Bought expensive → loss</td></tr></table>

# 8 Experiment 1: Constant Realised Volatility $( \sigma _ { \mathbf { r e a l } } = 5 0 \% )$

# 8.1 Sample Path

We generate a single GBM sample path with $\sigma = 5 0 \%$ . The stock starts at 100, drops significantly, and finishes at $S _ { T } \approx 9 0 . 0$ , so the call expires out of the money with zero payoff.

![](images/9e05d87faabe36115b5af7d941e4dd5b23cfc238df6b61ccc8bbcf0d42171c46.jpg)

<details>
<summary>line</summary>

| Trading Day | Stock Price |
| ----------- | ----------- |
| 0           | 100         |
| 50          | 70          |
| 100         | 65          |
| 150         | 68          |
| 200         | 75          |
| 250         | 85          |
</details>

Figure 1: GBM sample path with constant $\sigma _ { \mathsf { r e a l } } = 5 0 \%$ . Green/red shading indicates in/out of the money relative to the strike.

# 8.2 Delta-Hedged PnL

Figure 2 shows the mark-to-market PnL of the hedged portfolio and the evolving hedge ratio ∆ over time.

![](images/f23ebad1208fb453f29c5a1352e1c23ad8fed4426bb8b540fa9cb781b6499c5f.jpg)

<details>
<summary>line</summary>

| Trading Day | σ_hedge=30% PnL | σ_hedge=60% PnL |
| ----------- | --------------- | --------------- |
| 0           | 0.0             | 0.0             |
| 50          | ~1.5            | ~-1.0           |
| 100         | ~2.5            | ~-2.0           |
| 150         | ~3.0            | ~-2.5           |
| 200         | ~4.0            | ~-3.5           |
| 250         | ~8.0            | ~-5.0           |
</details>

![](images/7c563c815962c2595262bc549d50f4092d37827d6014fc536076ab6f7596d8d9.jpg)

<details>
<summary>line</summary>

| Trading Day | σ_hedge=30% | σ_hedge=60% |
| ----------- | ----------- | ----------- |
| 0           | 0.7         | 0.7         |
| 50          | 0.1         | 0.4         |
| 100         | 0.05        | 0.3         |
| 150         | 0.03        | 0.2         |
| 200         | 0.02        | 0.15        |
| 250         | 0.0         | 0.0         |
</details>

Figure 2: Left: Hedged portfolio PnL (no transaction costs). Green: $\sigma _ { \mathsf { h e d g e } }$ = 30% (bought cheap vol ⇒ profit). Red: $\sigma _ { \mathsf { h e d g e } } = 6 0 \%$ (bought expensive vol ⇒ loss). Right: The hedge ratio $\Delta$ over time; the lower $\sigma _ { \mathsf { h e d g e } }$ produces a more “binary” delta near expiry.

# 8.3 Cumulative Gamma PnL

The cumulative gamma PnL $\begin{array} { r } { \sum _ { i } \frac { 1 } { 2 } \Gamma _ { i } [ ( \Delta S _ { i } ) ^ { 2 } - \sigma _ { \mathsf { h e d g e } } ^ { 2 } S _ { i } ^ { 2 } \Delta t ] } \end{array}$ shows how profit or loss accumulates day by day.

Cumulative Gamma PnL- Constant grea/=50%   
![](images/946e56ac221b319062c0624076f523195f52fd045284cb881057d4a967ea16af.jpg)

<details>
<summary>line</summary>

| Trading Day | Cumulative F-PnL |
| ----------- | ---------------- |
| 0           | 0.0              |
| 50          | 1.5              |
| 100         | 2.5              |
| 150         | 3.0              |
| 200         | 3.5              |
| 250         | 7.5              |
</details>

![](images/840b729a74f42529ae208e6eddeaee63f7c6d034214d77f87ce19e7eab6a9f16.jpg)

<details>
<summary>line</summary>

| Trading Day | Cumulative F-PnL |
| ----------- | ---------------- |
| 0           | 0                |
| 50          | -1               |
| 100         | -2               |
| 150         | -3               |
| 200         | -4               |
| 250         | -5               |
</details>

Figure 3: Cumulative gamma PnL. Left: $\sigma _ { \mathsf { h e d g e } } = 3 0 \% -$ realised moves exceed the “budgeted” volatility, so gamma scalping generates persistent gains. Right: $\sigma _ { \mathsf { h e d g e } } = 6 0 \% -$ theta decay exceeds gamma gains, leading to persistent losses.

# 8.4 Daily Gamma PnL Decomposition

Each bar represents one day’s contribution to the total gamma PnL.

$$
\text {Daily Gamma PnL} = \frac {1}{2} \Gamma [ (\Delta S) ^ {2} - \sigma_ {\text {hedge}} ^ {2} S ^ {2} \Delta t ] - \text {Constant} \sigma = 50 \%
$$

![](images/6a899be02a3edb82e3e71c649bd018e432acc1abe1ea426bc77b586183761544.jpg)

<details>
<summary>line</summary>

| Trading Day | Gain | Loss |
| ----------- | ---- | ---- |
| 0           | 0.15 | 0.01 |
| 10          | 0.18 | 0.01 |
| 20          | 0.12 | 0.01 |
| 30          | 0.16 | 0.01 |
| 40          | 0.19 | 0.01 |
| 50          | 0.14 | 0.01 |
| 60          | 0.17 | 0.01 |
| 70          | 0.33 | 0.01 |
| 80          | 0.15 | 0.01 |
| 90          | 0.18 | 0.01 |
| 100         | 0.12 | 0.01 |
| 110         | 0.16 | 0.01 |
| 120         | 0.14 | 0.01 |
| 130         | 0.17 | 0.01 |
| 140         | 0.13 | 0.01 |
| 150         | 0.15 | 0.01 |
| 160         | 0.24 | 0.01 |
| 170         | 0.12 | 0.01 |
| 180         | 0.16 | 0.01 |
| 190         | 0.14 | 0.01 |
| 200         | 0.37 | 0.01 |
| 210         | 0.55 | -0.05 |
| 220         | 0.85 | -0.15 |
| 230         | 0.82 | -0.12 |
| 240         | 0.83 | -0.18 |
| 250         | 0.15 | -0.12 |
</details>

![](images/bc5804dd84a3c88833ba4700e73e2db67213aca63dc516a80abce497171c46ce.jpg)

<details>
<summary>line</summary>

| Trading Day | Gain | Loss |
| ----------- | ---- | ---- |
| 0           | 0.0  | 0.0  |
| 50          | 0.0  | 0.0  |
| 100         | 0.0  | 0.0  |
| 150         | 0.0  | 0.0  |
| 200         | 0.0  | 0.0  |
| 250         | 0.0  | 0.0  |
</details>

Figure 4: Daily gamma PnL. For $\sigma _ { \mathsf { h e d g e } } = 3 0 \%$ , almost every day is green (gain) because realised moves consistently exceed what 30% vol would predict. For $\sigma _ { \mathsf { h e d g e } } = 6 0 \%$ , most days are red (loss) because realised moves fall short of the 60% “budget.”

# 8.5 Summary: Constant Volatility

Table 7: Hedging PnL with constant $\sigma _ { \mathsf { r e a l } } = 5 0 \%$ (no transaction costs) 

<table><tr><td> $\sigma_{\text{hedge}}$ </td><td> $C_0$  (price paid)</td><td> $C(\sigma_{\text{real}})$ </td><td>Theoretical PnL</td><td>Simulated PnL</td><td>Interpretation</td></tr><tr><td>30%</td><td>14.23</td><td>21.79</td><td>+7.56</td><td>+7.98</td><td>Bought cheap vol</td></tr><tr><td>60%</td><td>25.52</td><td>21.79</td><td>-3.73</td><td>-4.68</td><td>Overpaid for vol</td></tr></table>

The simulated PnL is close to (but not equal to) the theoretical value because the PnL integral (13) is path-dependent: it depends on the specific path of $S _ { t } ^ { 2 } \Gamma _ { t }$ , not just the average.

# 9 Experiment 2: Transaction Costs

In practice, every rebalance incurs a cost. We model proportional transaction costs:

$$
\text { TC   per   rebalance } = | \Delta_ {\text { new }} - \Delta_ {\text { old }} | \times S \times c,
$$

where c is the cost rate $( \mathsf { e . g . } c = 0 . 1 \% )$ .

![](images/226d8b0e02383a6be3eb21be920769f21370e2c9b8538f18ae01f92fad0c0fbe.jpg)

<details>
<summary>line</summary>

| Trading Day | TC=0% PnL=+7.98 (tc=0.0) | TC=0.1% PnL=+7.37 (tc=0.6) | TC=0.3% PnL=+6.14 (tc=1.8) | TC=0.5% PnL=+4.92 (tc=3.0) |
| ----------- | ------------------------ | -------------------------- | --------------------------- | --------------------------- |
| 0           | 0                        | 0                          | 0                           | 0                           |
| 50          | ~1.5                     | ~1.4                       | ~1.2                        | ~0.8                        |
| 100         | ~2.5                     | ~2.3                       | ~1.8                        | ~1.2                        |
| 150         | ~3.0                     | ~2.8                       | ~2.2                        | ~1.5                        |
| 200         | ~4.0                     | ~3.5                       | ~3.0                        | ~2.0                        |
| 250         | ~8.0                     | ~7.5                       | ~6.0                        | ~5.0                        |
</details>

![](images/3a8c48a7aeeae3f4743630f2ad83cbc5185206019607fc0a6ef8baa3ca5b6205.jpg)

<details>
<summary>line</summary>

| Trading Day | TC=0% PnL=-4.68 (tc=0.0) | TC=0.1% PnL=-5.19 (tc=0.5) | TC=0.3% PnL=-6.20 (tc=1.5) | TC=0.5% PnL=-7.22 (tc=2.5) |
| ----------- | ------------------------ | -------------------------- | --------------------------- | --------------------------- |
| 0           | 0                        | 0                          | 0                           | 0                           |
| 50          | -1.0                     | -1.2                       | -1.4                        | -1.6                        |
| 100         | -2.0                     | -2.2                       | -2.4                        | -2.6                        |
| 150         | -3.0                     | -3.2                       | -3.4                        | -3.6                        |
| 200         | -4.0                     | -4.2                       | -4.4                        | -4.6                        |
| 250         | -5.0                     | -5.2                       | -5.4                        | -5.6                        |
</details>

Figure 5: Impact of transaction costs on the hedged PnL. Each line style represents a different TC rate. Transaction costs uniformly erode PnL: profits shrink, losses deepen.

Table 8: Transaction cost impact — constant $\sigma _ { \mathsf { r e a l } } = 5 0 \%$ 

<table><tr><td rowspan="2">TC Rate</td><td colspan="2"> $\sigma_{\text{hedge}} = 30\%$ </td><td colspan="2"> $\sigma_{\text{hedge}} = 60\%$ </td></tr><tr><td>Final PnL</td><td>TC Paid</td><td>Final PnL</td><td>TC Paid</td></tr><tr><td>0%</td><td>+7.98</td><td>0.00</td><td>-4.68</td><td>0.00</td></tr><tr><td>0.1%</td><td>+7.37</td><td>0.60</td><td>-5.19</td><td>0.50</td></tr><tr><td>0.3%</td><td>+6.14</td><td>1.80</td><td>-6.20</td><td>1.50</td></tr><tr><td>0.5%</td><td>+4.92</td><td>3.00</td><td>-7.22</td><td>2.50</td></tr></table>

# Observation: Break-Even Transaction Cost

For the σhedge = 30% case, the trader still profits at TC= 0.5% (PnL = +4.92), but the profit has been reduced by 38%. There exists a break-even TC rate at which the gamma scalping gains are entirely consumed by transaction costs. This is why high-frequency delta hedging is not always optimal in practice—and why the Whalley–Wilmott hedging band (Section 4) is valuable.

# 10 Experiment 3: Regime-Switching Volatility

# 10.1 Motivation

Real markets do not have constant volatility. We now test a scenario where:

$$
\sigma_{\text{real}}(t) = \left\{ \begin{array}{ll}40\% & t\in [0,T / 2]\\ 60\% & t\in (T / 2,T] \end{array} \right.
$$

The arithmetic average is σ¯ = 50%, identical to the constant case. However, the RMS (varianceaverage) volatility is:

$$
\sigma_ {\mathrm{RMS}} = \sqrt {\frac {0 . 4 0 ^ {2} + 0 . 6 0 ^ {2}}{2}} = \sqrt {0 . 2 6} \approx 51.0 \%.
$$

Since the gamma PnL formula (13) depends on $\sigma ^ { 2 }$ (variance), the RMS vol is the correct measure, not the arithmetic average.

# 10.2 Sample Paths

Both paths use the same Brownian draws so that any difference in outcomes is purely due to the volatility schedule, not randomness.

![](images/3423cda3e0760b75f693289ca9e68ad1c708b4c59eff4461b72352965f7396e0.jpg)

<details>
<summary>line</summary>

| Trading Day | Stock Price (Regime σ 40%→60%) S_T=97.1 | Stock Price (Constant σ=50% S_T=90.0) | Stock Price (Strike K=100) | Stock Price (Regime switch day 126) |
| ----------- | ---------------------------------------- | ------------------------------------- | -------------------------- | ------------------------------------ |
| 0           | 100.0                                    | 100.0                                 | 100.0                      | 100.0                                |
| 50          | 80.0                                     | 75.0                                  | 78.0                       | 77.0                                 |
| 100         | 75.0                                     | 70.0                                  | 73.0                       | 72.0                                 |
| 150         | 65.0                                     | 60.0                                  | 63.0                       | 62.0                                 |
| 200         | 85.0                                     | 80.0                                  | 83.0                       | 82.0                                 |
| 250         | 95.0                                     | 90.0                                  | 93.0                       | 92.0                                 |
</details>

Figure 6: Top: Two sample paths generated from the same random draws. The regime-switch path (blue) is less volatile in the first half and more volatile in the second half. Bottom: The volatility regime, showing the switch at day 126.

# 10.3 PnL Comparison: Regime vs. Constant

PnL: Regime-Switch vs Constant Vol (no TC,same Brownian draws)   
![](images/c7a717e3e435432bf38ff663816373b02d2549c9323603f8327c8e30020a99d8.jpg)

<details>
<summary>line</summary>

| Trading Day | Regime (40% → 60%) PnL=+14.23 | Constant 50% PnL=+7.98 | Regime switch |
| ----------- | ------------------------------ | ------------------------ | ------------- |
| 0           | 0                              | 0                        | -             |
| 50          | ~1                             | ~1.5                     | -             |
| 100         | ~1.5                           | ~2.5                     | -             |
| 150         | ~2                             | ~3                       | -             |
| 200         | ~4                             | ~4                       | -             |
| 250         | ~14                            | ~8                       | -             |
</details>

![](images/cdc0f4a9b036318b76c6ce566a57e5d93ab92a1c357bbd4552f28ea9983be805.jpg)

<details>
<summary>line</summary>

| Trading Day | Regime (40% → 60%) PnL | Constant 50% PnL | Regime switch |
| ----------- | ---------------------- | ----------------- | ------------- |
| 0           | 0.0                    | 0.0               | 0.0           |
| 50          | -1.5                   | -1.2              | -1.8          |
| 100         | -2.8                   | -2.0              | -2.5          |
| 150         | -3.5                   | -2.8              | -3.2          |
| 200         | -4.0                   | -3.5              | -3.8          |
| 250         | -3.5                   | -4.6              | -4.8          |
</details>

Figure 7: Head-to-head PnL comparison. Solid lines: regime-switching vol path. Dashed lines: constant-vol path. The purple dotted line marks the regime switch at day 126. Note how the regime path’s PnL accelerates in the second half when $\sigma _ { \mathsf { r e a l } }$ jumps to 60%.

Table 9: PnL comparison: Regime-switch vs. Constant (no TC) 

<table><tr><td> $\sigma_{\text{hedge}}$ </td><td>PnL (Regime)</td><td>PnL (Constant)</td><td>Difference</td></tr><tr><td>30%</td><td>+14.23</td><td>+7.98</td><td>+6.25</td></tr><tr><td>60%</td><td>-3.51</td><td>-4.68</td><td>+1.16</td></tr></table>

# 10.4 Why Is the Regime PnL So Different?

Even though the arithmetic average $\sigma = 5 0 \%$ in both cases, the gamma PnL differs dramatically:

1. Variance matters, not volatility. The daily gamma PnL involves $\sigma _ { \mathsf { r e a l } } ^ { 2 } ,$ so the correct average is $\sigma _ { \mathsf { R M S } } ^ { 2 } = 0 . 2 6 > 0 . 2 5 = \sigma _ { \mathsf { c o n s t } } ^ { 2 }$ . The regime path has slightly higher effective variance.   
2. Gamma is path-dependent. The weighting $\textstyle { \frac { 1 } { 2 } } S _ { t } ^ { 2 } \Gamma _ { t }$ in (13) varies with the stock price. Different paths produce different weightings.   
3. Gamma increases near expiry and near the money. In the second half, when $\sigma _ { \mathsf { r e a l } } = 6 0 \%$ , the gamma is naturally larger (closer to expiry), amplifying the impact of the higher volatility regime.

# 10.5 Cumulative Gamma PnL

Cumulative Gamma PnL- Regime vs Constant   
![](images/e43ac0aa59d56caba03cb5391c41e22f218128fab586bac3bd1d36f13f68a152.jpg)

<details>
<summary>line</summary>

| Trading Day | Regime (40% → 60%) | Constant 50% |
| ----------- | ------------------ | ------------ |
| 0           | 0.0                | 0.0          |
| 50          | 0.5                | 1.0          |
| 100         | 1.0                | 2.0          |
| 150         | 2.0                | 3.0          |
| 200         | 4.0                | 4.5          |
| 250         | 13.0               | 7.5          |
</details>

![](images/0e6362933c7e467bf61d13ca6947ed46c75e827018a464075bf0a42abc46fb5f.jpg)

<details>
<summary>line</summary>

| Trading Day | Regime (40% → 60%) | Constant 50% |
| ----------- | ------------------ | ------------ |
| 0           | 0                  | 0            |
| 50          | -1.5               | -1.2         |
| 100         | -2.8               | -2.5         |
| 150         | -3.5               | -3.2         |
| 200         | -4.0               | -3.8         |
| 250         | -3.8               | -4.5         |
</details>

Figure 8: Cumulative gamma PnL for regime (solid) vs. constant (dashed). For $\sigma _ { \mathsf { h e d g e } } = 3 0 \%$ , the regime path shows a dramatic acceleration after the regime switch. For $\sigma _ { \mathsf { h e d g e } } = 6 0 \%$ , the regime path stops losing in the second half (where $\sigma _ { \mathsf { r e a l } } = \sigma _ { \mathsf { h e d g e } } = 6 0 \% )$ .

# 10.6 Daily Gamma PnL

Daily Gamma PnL- Regime g(40% → 60%)   
![](images/f0b7fce63d4dc7a72141a98c64a97f83037dc05213e1168640fec545d5730417.jpg)

<details>
<summary>line</summary>

| Trading Day | Gain | Loss |
| ----------- | ---- | ---- |
| 0           | 0.00 | 0.00 |
| 50          | 0.00 | 0.00 |
| 100         | 0.00 | 0.00 |
| 150         | 0.00 | 0.00 |
| 200         | 0.00 | 0.00 |
| 250         | 1.25 | 0.00 |
</details>

![](images/654af6e1622a2c202eff007011979684e0065a0f52f5cfd4301bfb847810c082.jpg)

<details>
<summary>line</summary>

| Trading Day | Gain | Loss |
| ----------- | ---- | ---- |
| 0           | 0.00 | 0.00 |
| 50          | 0.00 | 0.00 |
| 100         | 0.00 | 0.00 |
| 150         | 0.00 | 0.00 |
| 200         | 1.25 | -0.25 |
| 250         | 0.375| -0.25 |
</details>

Figure 9: Daily gamma PnL bars. The purple line marks the regime switch. Left $( \sigma _ { \mathsf { h e d g e } } = 3 0 \% ) \colon$ gains are larger in the second half (60% vol ≫ 30% hedge). Right $( \sigma _ { \mathbf { h e d g e } } = 6 0 \% )$ : losses concentrate in the first half (40% vol < 60% hedge), while the second half is approximately break-even.

# 10.7 Transaction Costs: Regime Path

Transaction Cost Impact - Regime g(40%→60%)   
![](images/014a0ba0d7c2465074a092077a9e619a3cb512e2af1d639561b70dc4904f93b2.jpg)

<details>
<summary>line</summary>

| Trading Day | TC=0% PnL=+14.23 (tc=0.0) | TC=0.1% PnL=+13.26 (tc=1.0) | TC=0.3% PnL=+11.31 (tc=2.9) | TC=0.5% PnL=+9.36 (tc=4.8) |
| ----------- | ------------------------ | -------------------------- | -------------------------- | -------------------------- |
| 0           | 0                        | 0                          | 0                          | 0                          |
| 50          | ~0.5                     | ~0.5                       | ~0.5                       | ~0.5                       |
| 100         | ~1.0                     | ~1.0                       | ~1.0                       | ~1.0                       |
| 150         | ~2.0                     | ~2.0                       | ~2.0                       | ~2.0                       |
| 200         | ~6.0                     | ~6.0                       | ~6.0                       | ~6.0                       |
| 250         | ~14.23                   | ~13.26                     | ~11.31                     | ~9.36                      |
</details>

![](images/0e49bff745b27071fff4f0a7f7daec6820261c4953c0f8870f449e83f6904b1d.jpg)

<details>
<summary>line</summary>

| Trading Day | TC=0% PnL=-3.51 (tc=0.0) | TC=0.1% PnL=-4.19 (tc=0.7) | TC=0.3% PnL=-5.55 (tc=2.0) | TC=0.5% PnL=-6.91 (tc=3.4) |
| ----------- | ------------------------ | -------------------------- | -------------------------- | -------------------------- |
| 0           | 0                        | 0                          | 0                          | 0                          |
| 50          | -1.5                     | -1.8                       | -2.0                       | -2.5                       |
| 100         | -2.5                     | -2.8                       | -3.0                       | -3.5                       |
| 150         | -3.5                     | -3.8                       | -4.0                       | -4.5                       |
| 200         | -4.5                     | -4.8                       | -5.0                       | -5.5                       |
| 250         | -5.5                     | -5.8                       | -6.0                       | -6.5                       |
</details>

Figure 10: Transaction cost impact on the regime-switching path. Higher vol in the second half causes larger delta adjustments, increasing cumulative TC.

Table 10: Full results: Regime-switching vs. Constant volatility 

<table><tr><td rowspan="2">TC Rate</td><td rowspan="2">Scenario</td><td colspan="2"> $\sigma_{\text{hedge}} = 30\%$ </td><td colspan="2"> $\sigma_{\text{hedge}} = 60\%$ </td></tr><tr><td>Final PnL</td><td>TC Paid</td><td>Final PnL</td><td>TC Paid</td></tr><tr><td rowspan="2">0%</td><td>Constant</td><td>+7.98</td><td>0.0</td><td>-4.68</td><td>0.0</td></tr><tr><td>Regime</td><td>+14.23</td><td>0.0</td><td>-3.51</td><td>0.0</td></tr><tr><td rowspan="2">0.1%</td><td>Constant</td><td>+7.37</td><td>0.6</td><td>-5.19</td><td>0.5</td></tr><tr><td>Regime</td><td>+13.26</td><td>1.0</td><td>-4.19</td><td>0.7</td></tr><tr><td rowspan="2">0.3%</td><td>Constant</td><td>+6.14</td><td>1.8</td><td>-6.20</td><td>1.5</td></tr><tr><td>Regime</td><td>+11.31</td><td>2.9</td><td>-5.55</td><td>2.0</td></tr><tr><td rowspan="2">0.5%</td><td>Constant</td><td>+4.92</td><td>3.0</td><td>-7.22</td><td>2.5</td></tr><tr><td>Regime</td><td>+9.36</td><td>4.8</td><td>-6.91</td><td>3.4</td></tr></table>

# 11 Key Takeaways

# Summary of Main Lessons

1. Gamma PnL $\mathbf { \beta } = { \frac { 1 } { 2 } } \Gamma ( \sigma _ { \mathbf { r e a l } } ^ { 2 } - \sigma _ { \mathbf { h e d g e } } ^ { 2 } ) S ^ { 2 } d t$ . The sign of the PnL is determined by whether realised vol exceeds or falls short of the hedging vol.   
2. Long gamma profits from high realised vol. A trader who buys options and delta hedges will profit if the underlying moves more than the implied vol suggests (“gamma scalping”).   
3. Short gamma profits from low realised vol. A trader who sells options and delta hedges profits when the market is quieter than implied. This is the basis of the variance risk premium strategy.   
4. PnL is path-dependent. The same average volatility can produce very different PnL outcomes depending on when the high and low vol periods occur, because the weighting $S _ { t } ^ { 2 } \Gamma _ { t }$ varies over time.   
5. Variance, not volatility, is the correct average. For hedging PnL, $\sigma _ { \mathsf { R M S } } = { \sqrt { \overline { { \sigma ^ { 2 } } } } }$ matters, not σ¯. A regime with 40% and 60% has RMS vol of 51.0%, not 50%.   
6. Transaction costs erode PnL. Every delta rebalance incurs a cost. Higher realised vol ⇒ larger delta changes ⇒ higher TC. There is a break-even TC rate beyond which hedging is unprofitable.   
7. Hedging frequency is a trade-off. More frequent hedging reduces discretisation error but increases TC. In practice, traders optimise the hedging frequency or use bandwidth triggers (hedge only when $\begin{array} { r } { | \Delta _ { \sf n e w } - \Delta _ { \sf o l d } | > } \end{array}$ threshold).