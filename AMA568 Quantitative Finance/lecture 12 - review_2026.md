# AMA568 — Advanced Topics in Quantitative Finance

Course Review: Key Knowledge Points

Semester 2, 2025/26

Department of Applied Mathematics The Hong Kong Polytechnic University

# Exam Information:

• Date: 23 April 2026, 19:00–22:00 (3 hours)   
• 6 Questions, 100 marks total   
• All questions are compulsory   
• Open-book; normal distribution table provided

This document summarizes the key knowledge points covered in the course. It is intended as a study reference, not as a practice exam.

# Contents

# 1 Stochastic Calculus Toolkit 4

1.1 Brownian Motion 4   
1.2 Ito’s Lemma — One Dimension .ˆ 4   
1.3 Ito’s Lemma — Two Dimensionsˆ 4   
1.4 Feynman–Kac Theorem 5   
1.5 Geometric Brownian Motion . . 5

# 2 The Black–Scholes–Merton Framework 6

2.1 Black–Scholes PDE 6   
2.2 Black–Scholes Pricing Formulas 6   
2.3 The Greeks . . . 7   
2.4 BS PDE in Greek Notation . . . 7

# 3 Delta Hedging and PnL Analysis 9

3.1 Discrete Delta Hedging 9   
3.2 Continuous Delta Hedging PnL . 9   
3.3 Expected PnL with Continuous Hedging . . 10   
3.4 The General Case (r = 0 ̸ ) . . 10   
3.5 Transaction Costs 10

# 4 Characteristic Functions and Affine Models 11

4.1 Characteristic Function 11   
4.2 PDE for the Characteristic Function . . 11   
4.3 Affine Structure . . . 11   
4.4 Catalog of Mean-Reverting Processes . 12

# 5 Stochastic Volatility Models 13

5.1 Why Stochastic Volatility? 13   
5.2 General Two-Factor Framework . . . 13   
5.3 PDE for Option Price V (S, v, t) 13   
5.4 Key Models . . 14

# 6 Structured Products 15

6.1 Payoff Decomposition Principle . . . 15   
6.2 Useful Payoff Identities . . 15   
6.3 Principal-Protected Notes 15   
6.4 Autocallable (Snowball) Products . . 16   
6.5 Greeks of Structured Products 16

# 7 Monte Carlo Simulation 17

7.1 General Framework 17   
7.2 Simulating GBM 17   
7.3 Simulating Stochastic Volatility 17   
7.4 Path-Dependent Products . . 17   
7.5 Euler vs Exact Discretization 18

# 8 Implied Volatility Surface 19

8.1 Implied Volatility 19   
8.2 Smile and Skew 19   
8.3 Log-Moneyness and Total Implied Variance 19   
8.4 The SVI Parameterization . . 20   
8.5 Role of Each Parameter 20   
8.6 SVI Calibration 21

# 9 Volatility Measurement and Forecasting 22

9.1 Historical (Realized) Volatility . . . 22   
9.2 Parkinson Estimator 22   
9.3 EWMA (Exponentially Weighted Moving Average) 22   
9.4 GARCH(1,1) 22

# 10 Quick Reference: Key Formulas 24

# 1 Stochastic Calculus Toolkit

# 1.1 Brownian Motion

A standard Brownian motion $W _ { t }$ has the properties:

• $W _ { 0 } = 0 ,$   
• Independent increments: $W _ { t } - W _ { s }$ is independent of $\mathcal { F } _ { s }$ for $t > s ,$   
• Gaussian increments: $W _ { t } - W _ { s } \sim { \mathcal { N } } ( 0 , t - s )$ ,   
• $( d W _ { t } ) ^ { 2 } = d t ,$ dWt dt = 0, (dt)2 = 0.

# 1.2 Ito’s Lemma — One Dimension ˆ

# 1D Ito’s Lemmaˆ

If $d X _ { t } = \mu d t + \sigma d W _ { t }$ and $f ( X _ { t } , t )$ is a smooth function, then:

$$
d f = \frac {\partial f}{\partial t} d t + \frac {\partial f}{\partial X} d X + \frac {1}{2} \frac {\partial^ {2} f}{\partial X ^ {2}} (d X) ^ {2},
$$

where $( d X ) ^ { 2 } = \sigma ^ { 2 } d t$

# 1.3 Ito’s Lemma — Two Dimensionsˆ

# 2D Ito’s Lemma ˆ

If $d X = \mu _ { X } d t + \sigma _ { X } d W ^ { 1 }$ and $d Y = \mu _ { Y } d t + \sigma _ { Y } d W ^ { 2 }$ with $d W ^ { 1 } d W ^ { 2 } = \rho d t$ , then for $f ( X , Y , t )$ :

$$
d f = \frac {\partial f}{\partial t} d t + \frac {\partial f}{\partial X} d X + \frac {\partial f}{\partial Y} d Y + \frac {1}{2} \frac {\partial^ {2} f}{\partial X ^ {2}} (d X) ^ {2} + \frac {1}{2} \frac {\partial^ {2} f}{\partial Y ^ {2}} (d Y) ^ {2} + \frac {\partial^ {2} f}{\partial X \partial Y} d X d Y.
$$

The quadratic variations are:

$$
(d X) ^ {2} = \sigma_ {X} ^ {2} d t, \qquad (d Y) ^ {2} = \sigma_ {Y} ^ {2} d t, \qquad d X d Y = \rho \sigma_ {X} \sigma_ {Y} d t.
$$

# Common Pitfall

When computing $( d X ) ^ { 2 }$ , only the $d W$ term survives (all $d t \times d t$ and $d t \times d W$ terms vanish). For example, if $d S = r S d t + \sigma S d W$ , then $( d S ) ^ { 2 } = \sigma ^ { 2 } S ^ { 2 } d t$ .

# 1.4 Feynman–Kac Theorem

# Feynman–Kac Connection

If $X _ { t }$ satisfies $d X = \mu ( X ) d t + \sigma ( X )$ dW and we define

$$
g (x, t) = \mathbb {E} [ h (X _ {T}) \mid X _ {t} = x ],
$$

then g satisfies the PDE:

$$
\frac {\partial g}{\partial t} + \mu (x) \frac {\partial g}{\partial x} + \frac {1}{2} \sigma^ {2} (x) \frac {\partial^ {2} g}{\partial x ^ {2}} = 0,
$$

with terminal condition $g ( x , T ) = h ( x ) .$

This connects conditional expectations (probability) to PDEs (analysis), and is the foundation for derivatives pricing.

# 1.5 Geometric Brownian Motion

# GBM and its solution

$$
d S _ {t} = \mu S _ {t} d t + \sigma S _ {t} d W _ {t} \quad \Longrightarrow \quad S _ {T} = S _ {0} \exp \left[ \left(\mu - \frac {1}{2} \sigma^ {2}\right) T + \sigma \sqrt {T} Z \right],
$$

where $Z \sim \mathcal { N } ( 0 , 1 )$ . Under the risk-neutral measure, replace $\mu$ with r (risk-free rate).

# Why the $= \frac { 1 1 } { 9 } \textcircled { \div } \frac { 1 } { 9 }$ correction?

Applying Ito’s lemma to ˆ ln S:

$$
d (\ln S) = \frac {1}{S} d S - \frac {1}{2} \frac {1}{S ^ {2}} (d S) ^ {2} = \left(\mu - \frac {1}{2} \sigma^ {2}\right) d t + \sigma d W.
$$

The $- { \textstyle { \frac { 1 } { 2 } } } \sigma ^ { 2 }$ is the Ito correction from the second-order term. ˆ

# 2 The Black–Scholes–Merton Framework

# 2.1 Black–Scholes PDE

# Derivation of the BS PDE

Consider a portfolio Π = $V - \Delta S$ (long option, short ∆ shares). Applying Ito’sˆ lemma to $V ( S , t )$ and choosing $\begin{array} { r } { \Delta = { \frac { \partial V } { \partial S } } } \end{array}$ to eliminate dW , we require dΠ = rΠ dt (no-arbitrage):

$$
\boxed {\frac {\partial V}{\partial t} + r S \frac {\partial V}{\partial S} + \frac {1}{2} \sigma^ {2} S ^ {2} \frac {\partial^ {2} V}{\partial S ^ {2}} = r V.}
$$

# Key Features of the BS PDE

• The drift $\mu$ of the stock does not appear — only r and $\sigma .$   
• The PDE is the same for calls, puts, and any European derivative on S.   
• The terminal condition distinguishes different payoffs: $V ( S , T ) = ( S { - } K ) ^ { + }$ + for a call, $( K - S ) ^ { + }$ for a put, etc.

# 2.2 Black–Scholes Pricing Formulas

# European Call and Put (no dividend)

$$
C = S _ {0} \Phi (d _ {1}) - K e ^ {- r T} \Phi (d _ {2}), \tag {1}
$$

$$
P = K e ^ {- r T} \Phi (- d _ {2}) - S _ {0} \Phi (- d _ {1}), \tag {2}
$$

where

$$
d _ {1} = \frac {\ln (S _ {0} / K) + (r + \sigma^ {2} / 2) T}{\sigma \sqrt {T}}, \qquad d _ {2} = d _ {1} - \sigma \sqrt {T},
$$

Φ(·) = standard normal CDF, $\begin{array} { r } { \phi ( \cdot ) = \Phi ^ { \prime } ( \cdot ) = \frac { 1 } { \sqrt { 2 \pi } } e ^ { - x ^ { 2 } / 2 } = } \end{array}$ standard normal PDF.

Put-Call Parity: $C - P = S _ { 0 } - K e ^ { - r T }$

# 2.3 The Greeks

Greeks Summary Table (European Call without dividend) 

<table><tr><td>Greek</td><td>Definition</td><td>BS Call Formula</td><td>Meaning</td></tr><tr><td> $\Delta$ </td><td> $\frac{\partial V}{\partial S}$ </td><td> $\Phi(d_1)$ </td><td>Sensitivity to spot</td></tr><tr><td> $\Gamma$ </td><td> $\frac{\partial^2V}{\partial S^2}$ </td><td> $\frac{\phi(d_1)}{S\sigma\sqrt{T-t}}$ </td><td>Curvature / convexity</td></tr><tr><td> $\Theta$ </td><td> $\frac{\partial V}{\partial t}$ </td><td> $-\frac{S\sigma\phi(d_1)}{2\sqrt{T-t}} - rKe^{-r\tau}\Phi(d_2)$ </td><td>Time decay</td></tr><tr><td>Vega</td><td> $\frac{\partial V}{\partial \sigma}$ </td><td> $S\sqrt{T-t}\phi(d_1)$ </td><td>Sensitivity to vol</td></tr><tr><td> $\varrho$ </td><td> $\frac{\partial V}{\partial r}$ </td><td> $K\tau e^{-r\tau}\Phi(d_2)$ </td><td>Sensitivity to rate</td></tr></table>

# Important Relationships

• $\Gamma _ { \mathsf { c a l l } } = \Gamma _ { \mathsf { p u t } } > 0$ (put-call parity: $C - P = S - K e ^ { - r \tau }$ , second derivative identical).   
• $\mathsf { V e g a } _ { \mathsf { c a l l } } = \mathsf { V e g a } _ { \mathsf { p u t } } > 0 .$ .   
$\bullet \Delta _ { \sf p u t } = \Delta _ { \sf c a l l } - 1 = \Phi ( d _ { 1 } ) - 1 < 0 .$

# 2.4 BS PDE in Greek Notation

# Greek Form of BS PDE

$$
\Theta + r S \Delta + \frac {1}{2} \sigma^ {2} S ^ {2} \Gamma = r V.
$$

For a delta-neutral portfolio $( \Delta = 0 )$ :

$$
\Theta + \frac {1}{2} \sigma^ {2} S ^ {2} \Gamma = r V.
$$

# Theta–Gamma Trade-off

• Long Γ (bought options): You benefit from large moves but pay Θ (time decay).   
• Short Γ (sold options): You collect Θ but are hurt by large moves.   
• The BS PDE says these must balance (after accounting for the financing cost rV ).

# 3 Delta Hedging and PnL Analysis

# 3.1 Discrete Delta Hedging

At each rebalancing time, the hedge portfolio holds $\begin{array} { r } { \Delta _ { t } = \frac { \partial V } { \partial S } } \end{array}$ shares. Between rebalances, the portfolio P&L depends on the realized stock move.

# 3.2 Continuous Delta Hedging PnL

# Instantaneous Hedged PnL

For a delta-hedged option position with the option priced at implied vol $\sigma _ { i v }$ and the stock realizing vol $\sigma _ { r v }$ :

$$
d \Pi = \Theta d t + \frac {1}{2} \Gamma \sigma_ {r v} ^ {2} S ^ {2} d t.
$$

Using the BS PDE $\begin{array} { r } { ( r = 0 \mathsf { c a s e } \colon \Theta = - \frac { 1 } { 2 } \sigma _ { i v } ^ { 2 } S ^ { 2 } \Gamma ) } \end{array}$ :

$$
\boxed {d \Pi = \frac {1}{2} \Gamma S ^ {2} (\sigma_ {r v} ^ {2} - \sigma_ {i v} ^ {2}) d t.}
$$

Total PnL:

$$
\mathsf {P n L} = \int_ {0} ^ {T} \frac {1}{2} \Gamma_ {t} S _ {t} ^ {2} \left(\sigma_ {r v} ^ {2} - \sigma_ {i v} ^ {2}\right) d t.
$$

# Interpretation

• Bought option $( \Gamma > 0 )$ : profit when $\sigma _ { r v } > \sigma _ { i v }$ , lose when $\sigma _ { r v } < \sigma _ { i v }$   
• Sold option $( \Gamma < 0 )$ : opposite.   
• PnL is path-dependent: it depends on $S _ { t }$ along the path (via $\Gamma _ { t } S _ { t } ^ { 2 } )$ . Even if $\sigma _ { r v } > \sigma _ { i v }$ on average, you can still lose on an unlucky path.   
• This formula holds for both calls and puts (since $\Gamma > 0$ for both).

# 3.3 Expected PnL with Continuous Hedging

# Key Result

With continuous delta hedging and no transaction costs, the replication cost of an option equals the Black–Scholes price evaluated at the realized volatility. Therefore:

$$
\mathbb {E} [ \text { PnL   of   buying   option   and   hedging } ] = V (\sigma_ {r v}) - V (\sigma_ {i v}).
$$

• If $\sigma _ { r v } > \sigma _ { i v }$ : expected profit (bought vol cheap).   
• If $\sigma _ { r v } < \sigma _ { i v } :$ expected loss (overpaid for vol).

# 3.4 The General Case $( r \neq 0 )$

When $r \neq 0$ , the hedged PnL includes a financing term:

$$
d \Pi = \left[ \Theta + \frac {1}{2} \Gamma \sigma_ {r v} ^ {2} S ^ {2} \right] d t - r \Pi d t.
$$

Using the BS PDE: $\begin{array} { r } { \Theta = r V - r S \Delta - { \frac { 1 } { 2 } } \sigma _ { i v } ^ { 2 } S ^ { 2 } \Gamma } \end{array}$ , so:

$$
d \Pi = \frac {1}{2} \Gamma S ^ {2} (\sigma_ {r v} ^ {2} - \sigma_ {i v} ^ {2}) d t + r (V - S \Delta - \Pi) d t.
$$

# 3.5 Transaction Costs

In practice, each rebalance incurs a cost proportional to the traded notional:

$$
\text { TC   per   rebalance } \approx c \cdot S \cdot | \Delta \Gamma | \cdot | d S |,
$$

where c is the cost rate (e.g., bid-ask spread). Higher rebalancing frequency reduces hedging error but increases total TC.

# 4 Characteristic Functions and Affine Models

# 4.1 Characteristic Function

# Definition

The characteristic function of a random variable X is:

$$
\varphi_ {X} (\phi) = \mathbb {E} \left[ e ^ {i \phi X} \right], \quad i = \sqrt {- 1}.
$$

It uniquely determines the probability distribution of X and is the Fourier transform of its density:

$$
f _ {X} (x) = \frac {1}{2 \pi} \int_ {- \infty} ^ {\infty} e ^ {- i \phi x} \varphi_ {X} (\phi) d \phi .
$$

# Why Characteristic Functions?

Many stochastic models (Heston, CIR, Variance Gamma, etc.) do not have closed-form densities but do have closed-form characteristic functions. Option prices can then be recovered via Fourier inversion.

# 4.2 PDE for the Characteristic Function

Given an SDE $d X = \mu ( X ) d t + \sigma ( X )$ dW and defining $f ( \phi , t , x ) = \mathbb { E } [ e ^ { i \phi X _ { T } } \mid X _ { t } = x ]$ , the Feynman–Kac theorem gives:

$$
\frac {\partial f}{\partial t} + \mu (x) \frac {\partial f}{\partial x} + \frac {1}{2} \sigma^ {2} (x) \frac {\partial^ {2} f}{\partial x ^ {2}} = 0, \quad f (\phi , T, x) = e ^ {i \phi x}.
$$

# 4.3 Affine Structure

# The Affine Ansatz

For processes where the drift is linear in x and the diffusion squared is linear (or constant) in x, the characteristic function has the form:

$$
f (\phi , t, x) = \exp [ A (\phi , \tau) + B (\phi , \tau)   x ]  , \quad \tau = T - t.
$$

Substituting into the PDE and separating by powers of x yields ODEs for $A ( \tau )$ and $B ( \tau )$ with initial conditions $A ( 0 ) = 0 , B ( 0 ) = i \phi .$ .

# 4.4 Catalog of Mean-Reverting Processes

<table><tr><td>Model</td><td>SDE</td><td>Diffusion Type</td></tr><tr><td>Vasicek (OU)</td><td> $dX = \kappa(\theta - X) dt + \sigma dW$ </td><td>Constant</td></tr><tr><td>CIR</td><td> $dX = \kappa(\theta - X) dt + \xi\sqrt{X} dW$ </td><td> $\propto \sqrt{X}$ </td></tr><tr><td>Geometric OU</td><td> $dX = \kappa(\theta - X) X dt + \sigma X dW$ </td><td> $\propto X$ </td></tr></table>

# How the Diffusion Affects the ODEs

Constant diffusion (e.g., Vasicek): the $B ^ { 2 }$ term from ${ \scriptstyle { \frac { 1 } { 2 } } } \sigma ^ { 2 } B ^ { 2 }$ goes into the ODE for A. The ODE for B is linear: $B ^ { \prime } = - \kappa B$ (solvable in closed form).   
• State-dependent diffusion $\propto \sqrt { X }$ (e.g., CIR): the $\scriptstyle { \frac { 1 } { 2 } } \xi ^ { 2 } X B ^ { 2 }$ term goes into the ODE for B. The ODE for B is a Riccati equation: $\begin{array} { r } { B ^ { \prime } = - \kappa B + \frac { 1 } { 2 } \xi ^ { 2 } B ^ { 2 } } \end{array}$ .

In both cases, $A ( \tau )$ is obtained by integrating the constant terms once $B ( \tau )$ is known.

# Sign Convention

With $\begin{array} { r } { \tau = T - t \colon \frac { \partial f } { \partial t } = - \frac { d A } { d \tau } - \frac { d B } { d \tau } x } \end{array}$ . The negative sign is crucial when substituting.

# 5 Stochastic Volatility Models

# 5.1 Why Stochastic Volatility?

The Black–Scholes model assumes constant σ. In reality:

• The implied volatility varies across strikes (smile/skew) and maturities (term structure).   
• Volatility itself is random and exhibits mean reversion, clustering, and correlation with the underlying.

# 5.2 General Two-Factor Framework

Most stochastic vol models take the form:

$$
d S _ {t} = \mu_ {S} (S, v, t) d t + \sigma_ {S} (S, v) d W _ {t} ^ {1}, \tag {3}
$$

$$
d v _ {t} = \mu_ {v} (v, t) d t + \sigma_ {v} (v) d W _ {t} ^ {2}, \tag {4}
$$

$$
d W _ {t} ^ {1} d W _ {t} ^ {2} = \rho d t, \tag {5}
$$

where $v _ { t }$ is the stochastic variance (or volatility) and $\rho$ captures leverage effect.

# 5.3 PDE for Option Price $V ( S , v , t )$

# General Stochastic Vol PDE

Applying 2D Ito’s lemma to ˆ $V ( S , v , t )$ and requiring no-arbitrage:

$$
\frac {\partial V}{\partial t} + \mu_ {S} \frac {\partial V}{\partial S} + \mu_ {v} ^ {*} \frac {\partial V}{\partial v} + \frac {1}{2} \sigma_ {S} ^ {2} \frac {\partial^ {2} V}{\partial S ^ {2}} + \rho \sigma_ {S} \sigma_ {v} \frac {\partial^ {2} V}{\partial S \partial v} + \frac {1}{2} \sigma_ {v} ^ {2} \frac {\partial^ {2} V}{\partial v ^ {2}} = r V,
$$

where $\mu _ { v } ^ { * }$ is the risk-neutral drift of v (may differ from the physical drift by a market price of vol risk).

# 5.4 Key Models

<table><tr><td>Model</td><td>Asset Dynamics</td><td>Vol/Variance Dynamics</td></tr><tr><td>Heston</td><td> $dS = rS dt + \sqrt{v} S dW^{1}$ </td><td> $dv = \kappa(\theta - v) dt + \xi \sqrt{v} dW^{2}$ </td></tr><tr><td>SABR ( $\beta = 1$ )</td><td> $dF = \alpha F dW^{1}$  (fwd measure)</td><td> $d\alpha = \nu\alpha dW^{2}$ </td></tr><tr><td>Local Vol</td><td> $dS = rS dt + \sigma(S, t)S dW$ </td><td>Deterministic  $\sigma(S, t)$ </td></tr><tr><td>CEV</td><td> $dS = rS dt + \sigma S^{\beta} dW$ </td><td>Deterministic, level-dependent</td></tr></table>

# Deriving the PDE: The Recipe

For any specific stochastic vol model:

1. Write down the two SDEs.   
2. Apply 2D Ito’s lemma to ˆ $V ( S , v , t ) \left( \mathsf { o r } V ( F , \alpha , t ) \right) .$   
3. Compute the three quadratic variations: $( d S ) ^ { 2 } , ( d v ) ^ { 2 } , d S d v .$   
4. Collect all dt terms and apply the pricing condition (no-arbitrage or martingale).   
5. The terminal condition depends on the payoff: e.g., $V ( S , v , T ) = ( S - K ) ^ { + }$ for a call.

# Forward Measure vs Risk-Neutral Measure

• Under the risk-neutral measure: S has drift rS, PDE has $r S \frac { \partial V } { \partial S }$ and RHS = rV .   
• Under the forward measure: F is a martingale (no drift), PDE has no $\frac { \partial V } { \partial F }$ term and RHS = 0.

# 6 Structured Products

# 6.1 Payoff Decomposition Principle

# Fundamental Idea

Any structured product payoff can be decomposed into a portfolio of vanilla instruments (bonds, forwards, calls, puts). Once decomposed, each component is priced separately using Black–Scholes or other models.

# 6.2 Useful Payoff Identities

# Standard Decompositions

$$
\max (X, 0) = \text { Call   payoff   with   strike } 0. \tag {6}
$$

$$
\min (\max (X, 0), C) = \max (X, 0) - \max (X - C, 0) \quad (\text { capped   payoff } = \text { call   spread }). \tag {7}
$$

$$
\max (X, 0) = \frac {1}{S _ {0}} \max (S _ {T} - K, 0) \quad \text { if } X = \frac {S _ {T}}{S _ {0}} - 1 \text { and } K = S _ {0}. \tag {8}
$$

# 6.3 Principal-Protected Notes (PPN)

# PPN Structure

• Bond component: guarantees return of principal N at maturity.   
• Option component: provides upside participation.   
• Typical payoff: $N \times ( 1 + \alpha \times g ( S _ { T } ) )$ ) where g is a function of the terminal price.   
• Pricing: PV = discounted principal (zero-coupon bond) + scaled option component.

# Capped Participation

If the PPN has capped return $C _ { \mathsf { c a p } } { \mathrm { i } }$

$$
\text { Option   payoff } = \min \left(\max \left(\frac {S _ {T}}{S _ {0}} - 1, 0\right), C _ {\text { cap }}\right) = \frac {1}{S _ {0}} \left[ (S _ {T} - K _ {1}) ^ {+} - (S _ {T} - K _ {2}) ^ {+} \right],
$$

where $K _ { 1 } = S _ { 0 }$ and $K _ { 2 } = S _ { 0 } ( 1 + C _ { \mathsf { c a p } } )$ . This is a bull call spread.

# 6.4 Autocallable (Snowball) Products

# Product Mechanics

Autocallable products have path-dependent payoffs with two barriers:

• Knock-Out barrier (upper): if the asset touches this level at an observation date, the product terminates early with a coupon payment.   
• Knock-In barrier (lower): if the asset touches this level, downside protection is removed.

Three Possible Outcomes 

<table><tr><td>Scenario</td><td>Payoff</td></tr><tr><td>KO triggered</td><td>Early termination; principal + coupon accrued to KO date.</td></tr><tr><td>KI triggered, no KO</td><td>At maturity: RoR = min(0,  $S_T/S_0 - 1$ ).Downside loss.</td></tr><tr><td>Neither KI nor KO</td><td>At maturity: principal + full coupon. Best outcome.</td></tr></table>

# Check Order

When evaluating scenarios: always check knock-out first, then knock-in. If KO is triggered, the product terminates regardless of KI.

# 6.5 Greeks of Structured Products

Once a structured product is decomposed into vanilla components, its Greeks follow by linearity:

$$
\Delta_ {\text { product }} = \sum_ {i} w _ {i} \Delta_ {i}, \quad \mathbf {V e g a} _ {\text { product }} = \sum_ {i} w _ {i} \mathbf {V e g a} _ {i},
$$

where $w _ { i }$ are the weights/quantities of each component and $\Delta _ { i }$ , Vega are the Greeks of each component.

# 7 Monte Carlo Simulation

# 7.1 General Framework

# Monte Carlo Pricing Recipe

1. Discretize time: $\Delta t = T / n .$   
2. Generate random numbers: $Z _ { j } \sim \mathcal { N } ( 0 , 1 )$ .   
3. Simulate the path step by step.   
4. Evaluate the payoff (may involve path-dependent conditions).   
5. Repeat for N paths and compute:

$$
\text { Price } = e ^ {- r T} \times \frac {1}{N} \sum_ {j = 1} ^ {N} \text { Payoff } ^ {(j)}.
$$

# 7.2 Simulating GBM

For $d S = r S d t + \sigma S d W$ , the exact update is:

$$
S _ {t + \Delta t} = S _ {t} \exp \left[ \left(r - \frac {1}{2} \sigma^ {2}\right) \Delta t + \sigma \sqrt {\Delta t} Z \right], \quad Z \sim \mathcal {N} (0, 1).
$$

# 7.3 Simulating Stochastic Volatility

For two-factor models (Heston, SABR, etc.):

1. Generate correlated normals via Cholesky: $\widetilde { Z } _ { 1 } = Z _ { 1 } , \widetilde { Z } _ { 2 } = \rho Z _ { 1 } + \sqrt { 1 - \rho ^ { 2 } } Z _ { 2 }$   
2. Update the volatility/variance process first.   
3. Update the asset price using the current vol.

# When $[ \pmb { \mathscr { n } } ] = \pmb { \mathscr { n } }$

The two Brownian motions are independent. Cholesky reduces to using $Z _ { 1 }$ and $Z _ { 2 }$ directly.

# 7.4 Path-Dependent Products

For barrier products (autocallables, knock-in/out options):

• At each time step, check whether the barrier condition is met.

• Record the first time a barrier is hit (for knock-out) or whether any hit occurred (for knock-in).   
• Apply the correct payoff formula depending on which scenario materialized.

# 7.5 Euler vs Exact Discretization

<table><tr><td></td><td>Euler Scheme</td><td>Exact (Log-Normal)</td></tr><tr><td>Formula</td><td> $X_{t+\Delta t} = X_t + \mu \Delta t + \sigma \sqrt{\Delta t} Z$ </td><td> $X_{t+\Delta t} = X_t \exp[(\mu - \frac{1}{2}\sigma^2)\Delta t + \sigma \sqrt{\Delta t} Z]$ </td></tr><tr><td>Applicable to</td><td>Any SDE (approximate)</td><td>GBM, geometric processes (exact)</td></tr><tr><td>Positivity</td><td>Not guaranteed</td><td>Guaranteed (exponential)</td></tr></table>

# 8 Implied Volatility Surface

# 8.1 Implied Volatility

# Definition

The implied volatility $\sigma _ { \mathsf { B S } } ( K , T )$ is the value of σ that, when plugged into the Black–Scholes formula, reproduces the observed market price of the option. It is the market’s consensus forecast of future volatility, embedded in option prices.

# 8.2 Smile and Skew

• Volatility smile: implied vol is higher for deep OTM puts and deep OTM calls than for ATM options (U-shaped curve). Common in FX markets.   
• Volatility skew: implied vol is monotonically decreasing with strike. OTM puts are more expensive than OTM calls. Common in equity markets.   
• Term structure: implied vol varies with maturity T .

# 8.3 Log-Moneyness and Total Implied Variance

# Key Definitions

• Forward price: $F = S _ { 0 } e ^ { r T }$ (or given directly for futures).   
• Log-moneyness: $k = \ln ( K / F )$ .

– $k < 0 \colon$ OTM put (strike below forward).   
– k = 0: ATM forward (strike equals forward).   
– $k > 0 \colon$ OTM call (strike above forward).

• Total implied variance: $w ( k ) = \sigma _ { \mathsf { B } \mathsf { S } } ^ { 2 } ( k ) \cdot T$

• Recovery: $\sigma _ { { \mathsf { B } } { \mathsf { S } } } ( k ) = \sqrt { w ( k ) / T } .$

# 8.4 The SVI Parameterization

SVI Formula (Gatheral 2004)

$$
w (k) = a + b \left[ \rho (k - m) + \sqrt {(k - m) ^ {2} + \sigma^ {2}} \right].
$$

<table><tr><td>Param</td><td>Constraint</td><td>Role</td></tr><tr><td>a</td><td>a ∈ R</td><td>Overall variance level (vertical shift)</td></tr><tr><td>b</td><td>b ≥ 0</td><td>Slope of the wings</td></tr><tr><td>ρ</td><td>-1 ≤ ρ ≤ 1</td><td>Tilt / skew (left-right asymmetry)</td></tr><tr><td>m</td><td>m ∈ R</td><td>Horizontal translation of the vertex</td></tr><tr><td>σ</td><td>σ &gt; 0</td><td>Smoothness / curvature at the vertex</td></tr></table>

Additional constraint for no-arbitrage: $a + b \sigma \geq 0$ (minimum variance nonnegative).

# 8.5 Role of Each Parameter

# Understanding SVI Parameters

• At-the-money $( k = m ) \colon w ( m ) = a + b \sigma$ . Only $a , b , \sigma$ affect the ATM level; $\rho$ and m do not.   
• Symmetry: when $\rho = 0$ and $m = 0 , w ( k ) = a + b \sqrt { k ^ { 2 } + \sigma ^ { 2 } }$ depends only on $k ^ { 2 } ,$ , giving a symmetric smile.   
• Skew: $\rho < 0$ tilts the smile so that OTM puts $( k < 0 )$ have higher vol than OTM calls $( k > 0 )$ . This is the typical equity/crypto skew.   
• Wings: for large $| k | , w ( k ) \approx a + b ( 1 \pm \rho ) | k |$ (linear asymptotes). The slopes are $b ( 1 + \rho )$ (left wing) and $b ( 1 - \rho )$ (right wing).

# 8.6 SVI Calibration

# Least-Squares Calibration

Given market data $\{ ( k _ { i } , \sigma _ { i } ^ { \mathsf { m k t } } ) \} _ { i = 1 } ^ { N }$ , find $\pmb \theta = ( a , b , \rho , m , \sigma )$ minimizing:

$$
\min _ {\boldsymbol {\theta}} \sum_ {i = 1} ^ {N} \left[ w ^ {\mathsf {S V I}} (k _ {i}; \boldsymbol {\theta}) - w _ {i} ^ {\mathsf {m k t}} \right] ^ {2},
$$

where $w _ { i } ^ { \mathsf { m k t } } = ( \sigma _ { i } ^ { \mathsf { m k t } } ) ^ { 2 } \times T$ , subject to: $b \geq 0 , | \rho | \leq 1 , \sigma > 0 , a + b \sigma \geq 0 ,$

# 9 Volatility Measurement and Forecasting

# 9.1 Historical (Realized) Volatility

# Close-to-Close Estimator

Given n daily log-returns $r _ { i } = \ln ( S _ { i } / S _ { i - 1 } ) \colon$

$$
\hat {\sigma} _ {\mathrm{daily}} ^ {2} = \frac {1}{n - 1} \sum_ {i = 1} ^ {n} (r _ {i} - \bar {r}) ^ {2}, \qquad \hat {\sigma} _ {\mathrm{annual}} = \hat {\sigma} _ {\mathrm{daily}} \times \sqrt {2 5 2}.
$$

# 9.2 Parkinson Estimator

# Parkinson (1980)

Uses high–low prices for more efficient estimation:

$$
\hat {\sigma} _ {P} ^ {2} = \frac {1}{4 n \ln 2} \sum_ {i = 1} ^ {n} \left[ \ln \left(\frac {H _ {i}}{L _ {i}}\right) \right] ^ {2},
$$

where $H _ { i }$ and $L _ { i }$ are the high and low prices on day i. This estimator is about 5 times more efficient than close-to-close.

# 9.3 EWMA (Exponentially Weighted Moving Average)

# EWMA Variance

$$
\hat {\sigma} _ {t} ^ {2} = \lambda \hat {\sigma} _ {t - 1} ^ {2} + (1 - \lambda) r _ {t} ^ {2},
$$

where $\lambda \in ( 0 , 1 )$ is the decay factor (RiskMetrics uses λ = 0.94 for daily data).

• Gives more weight to recent observations.   
• Simple recursive formula; no optimization needed.

# 9.4 GARCH(1,1)

# GARCH(1,1) Model

$$
\sigma_ {t} ^ {2} = \omega + \alpha r _ {t - 1} ^ {2} + \beta \sigma_ {t - 1} ^ {2},
$$

where $\omega > 0 , \alpha \ge 0 , \beta \ge 0 , \alpha + \beta < 1 .$ .

Long-run variance: $\bar { \sigma } ^ { 2 } = \frac { \omega } { 1 - \alpha - \beta }$ .

EWMA is the special case $\omega = 0 , \alpha = 1 - \lambda , \beta = \lambda$ (no mean reversion).

# 10 Quick Reference: Key Formulas

# Ito’s Lemma (1D) ˆ

$$
d f = f _ {t} d t + f _ {X} d X + \frac {1}{2} f _ {X X} (d X) ^ {2}.
$$

# Black–Scholes Formulas

$$
C = S _ {0} \Phi (d _ {1}) - K e ^ {- r T} \Phi (d _ {2}), \quad P = K e ^ {- r T} \Phi (- d _ {2}) - S _ {0} \Phi (- d _ {1}), \tag {9}
$$

$$
d _ {1} = \frac {\ln (S _ {0} / K) + (r + \sigma^ {2} / 2) T}{\sigma \sqrt {T}}, \quad d _ {2} = d _ {1} - \sigma \sqrt {T}. \tag {10}
$$

# Put-Call Parity

$$
C - P = S _ {0} - K e ^ {- r T}.
$$

# BS PDE (Greek form)

$$
\Theta + r S \Delta + \frac {1}{2} \sigma^ {2} S ^ {2} \Gamma = r V.
$$

# Delta-Hedged PnL (r = 0)

$$
d \Pi = \frac {1}{2} \Gamma S ^ {2} (\sigma_ {r v} ^ {2} - \sigma_ {i v} ^ {2}) d t.
$$

# Feynman–Kac PDE

$$
g _ {t} + \mu (x) g _ {x} + \frac {1}{2} \sigma^ {2} (x) g _ {x x} = 0, \quad g (x, T) = h (x).
$$

# Affine Characteristic Function

$f = e ^ { A ( \tau ) + B ( \tau ) x }$ ; substitute and match powers of x to get ODEs for A and B.

# GBM Simulation

$$
S _ {t + \Delta t} = S _ {t} \exp [ (r - \frac {1}{2} \sigma^ {2}) \Delta t + \sigma \sqrt {\Delta t} Z ].
$$

# Cholesky (correlated normals)

$$
\widetilde {Z} _ {2} = \rho Z _ {1} + \sqrt {1 - \rho^ {2}}   Z _ {2}   \text { gives }   \mathsf {C o r r} (\widetilde {Z} _ {1}, \widetilde {Z} _ {2}) = \rho .
$$

# SVI Model

$$
w (k) = a + b [ \rho (k - m) + \sqrt {(k - m) ^ {2} + \sigma^ {2}} ], \quad \sigma_ {\mathsf {B S}} (k) = \sqrt {w (k) / T}.
$$

# PPN Decomposition

$$
\min (\max (R _ {T}, 0), C) = \frac {1}{S _ {0}} [ (S _ {T} - K _ {1}) ^ {+} - (S _ {T} - K _ {2}) ^ {+} ], \quad K _ {1} = S _ {0}, K _ {2} = S _ {0} (1 + C).
$$

# EWMA

$$
\hat {\sigma} _ {t} ^ {2} = \lambda \hat {\sigma} _ {t - 1} ^ {2} + (1 - \lambda) r _ {t} ^ {2}.
$$

# GARCH(1,1)

$$
\sigma_ {t} ^ {2} = \omega + \alpha r _ {t - 1} ^ {2} + \beta \sigma_ {t - 1} ^ {2}, \quad \text { long - run: } \bar {\sigma} ^ {2} = \omega / (1 - \alpha - \beta).
$$

# Normal Distribution Properties

$$
\Phi (- x) = 1 - \Phi (x), \quad \phi^ {\prime} (x) = - x \phi (x), \quad \phi (x) = \frac {1}{\sqrt {2 \pi}} e ^ {- x ^ {2} / 2}.
$$