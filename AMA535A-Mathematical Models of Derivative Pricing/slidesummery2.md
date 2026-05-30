# AMA535: Mathematics of Derivative Pricing AMA535A: Mathematical Models of Derivative Pricing

XU, Zuo Quan

The Hong Kong Polytechnic University

# Summary

• Financial assets include debt, equity, and derivatives.   
Financial markets provide platforms for trading these assets and for price discovery.   
Derivatives play a crucial role in risk management, speculation, and market efficiency.

# Why and How to Use Derivatives?

• Hedging: Reduce or eliminate risk exposure.   
Speculation: Take positions to profit from expected market movements.   
• Arbitrage: Lock in risk-free profits by exploiting price discrepancies.   
Asset transformation: Change the risk/return profile of a portfolio without buying or selling the underlying assets.

# Portfolio: Definition & Value

# Portfolio

A portfolio is any (static or dynamic) collection of financial assets, such as stocks, bonds, and cash, held in long or short positions.

# Value of a Portfolio

The value of a portfolio is the amount of money required to transfer its ownership to a third party. This value can be positive, negative, or zero.

# Simple and Compound Interests

# Interests

Simple Interest: It is equal to principal ∗ interest rate ∗ number of periods.

Discretely Compounding: The process of discrete compounding is utilized at specific finite periods of time, such as daily, monthly, or annually.

Continuously Compounding: Calculating the compounding period infinitesimally small.

# Bootstrap Method to Calculate Zero Rates

Example 3.1 (Market Data) 

<table><tr><td>Face value</td><td>Time to maturity (years)</td><td>Semi-annual coupon</td><td>Price</td></tr><tr><td>100</td><td>0.25</td><td>0</td><td>97.5</td></tr><tr><td>100</td><td>0.50</td><td>0</td><td>94.9</td></tr><tr><td>100</td><td>1.00</td><td>0</td><td>90.0</td></tr><tr><td>100</td><td>1.50</td><td>4</td><td>96.0</td></tr><tr><td>100</td><td>2.00</td><td>6</td><td>101.6</td></tr></table>

One coupon has just been paid if today is a payment date.

# Zero Curve

![](images/a187a666c3c5ec9525fe3e9639f7324c4ba00ad5add4e272ef0570ee71885963.jpg)

<details>
<summary>line</summary>

| Time to maturity (years) | Value |
| :--- | :--- |
| 0.25 | 10.1 |
| 0.5 | 10.45 |
| 1.0 | 10.55 |
| 1.5 | 10.65 |
| 2.0 | 10.85 |
| 2.5 | 10.85 |
</details>

# Bond Yield Measures

When a bond is purchased at a price different from its face value, three common yield measures are used:

Coupon Rate: Annual coupon payment as a percentage of face value.

Current Yield: Annual coupon payment divided by current market price.

Yield-to-Maturity (YTM): The annualized return if the bond is held to maturity, accounting for all coupons and price difference, also called bond yield.

# Forward Rate and Short Rate

# Theorem

The continuously compounded zero and forward rates satisfy

$$
\boxed {R _ {s, t} = \frac {t R _ {t} - s R _ {s}}{t - s}}
$$

# Short Rate

The instantaneous forward rate or short rate at time t is:

$$
r _ {t} = \lim _ {s \to t} R _ {s, t} = R _ {t} + t R _ {t} ^ {\prime},
$$

where $R _ { t }$ is the continuously compounded t-year zero rate. It represents the instantaneous annualized return at time t.

# Short Rate (Instantaneous Forward Rate):

# Theorem 3.1

$$
r _ {t} = R _ {t} + t R _ {t} ^ {\prime} = - (\ln P _ {t}) ^ {\prime} = - \frac {P _ {t} ^ {\prime}}{P _ {t}},
$$

$$
R _ {t} = \frac {1}{t} \int_ {0} ^ {t} r _ {s} \mathrm{d} s,
$$

$$
P _ {t} = e ^ {- \int_ {0} ^ {t} r _ {s} \mathrm{d} s}.
$$

# Theorem 3.2

If the short rate $r _ { s }$ or the zero rate $R _ { s }$ is random, then

$$
P _ {t} = \mathbb {E} ^ {Q} [ e ^ {- R _ {t} t} ] = \mathbb {E} ^ {Q} [ e ^ {- \int_ {0} ^ {t} r _ {s} \mathrm{d} s} ].
$$

# Forward Price Formula (with Dividends)

# Forward Price Formula (with Dividends)

If a stock pays total dividends worth D (value at time t) over [0, t], then the t-year forward price of the stock is:

$$
\boxed {F = S e ^ {r t} - D.}
$$

Because dividends before maturity will not be delivered to the long position, their value shall be removed from the forward price.

# Value of a Forward Contract

• At initiation, the value of a forward contract is zero.   
• When there are t-years to maturity, the value to the long is:

$$
\boxed {f = (F - K) e ^ {- r t} = S - K e ^ {- r t},}
$$

where S is the spot price, F is the current forward price, K is the delivery price, and r is the risk-free rate.

For a dividend-paying stock:

$$
f = S - D e ^ {- r t} - K e ^ {- r t}.
$$

# Moneyness of an Option

In-the-money (ITM): Option has positive intrinsic value. Call: $S > K ; \mathsf { P u t } ; \ S < K$ .   
Out-of-the-money (OTM): Option would have zero payoff if exercised now. Call: $S < K ; \mathsf { P u t } ; \ S > K$ .   
At-the-money (ATM): Strike price equals current spot price (S = K). ATM and OTM options have zero intrinsic value, only time value.

# What is Arbitrage?

# Arbitrage Opportunity

An arbitrage opportunity is a trading strategy on some [t, T ] that:

• Requires zero initial investment: $\Pi ( t ) = 0 $ ;   
• Guarantees non-negative payoff: $\Pi ( T ) \geqslant 0 ;$   
Has a strictly positive probability of gain: $\mathbb { P } ( \Pi ( T ) > 0 ) > 0 ;$ where Π(s) is the portfolio value at time s.

# Summery

Arbitrage: Make money out of nothing, without risk.

# Put-Call Parity (with Dividend)

# Theorem 1 (Put-Call Parity)

If the stock pays dividend D (valued at T ), then

$$
C _ {E} (t, K) + K e ^ {- r (T - t)} = S _ {t} - D e ^ {- r (T - t)} + P _ {E} (t, K).
$$

# Theorem 2 (Merton’s Theorem)

If the underlying stock pays no dividends, one has

$$
C _ {A} (t) = C _ {E} (t).
$$

# Multi-Step Binomial Tree: European Option

For an n-step binomial tree (step size $\Delta t = T / n )$ :

Risk-neutral probability:

$$
p = \frac {e ^ {r \Delta t} - d}{u - d}.
$$

Option price at time 0:

$$
f = e ^ {- r T} \sum_ {k = 0} ^ {n} {\binom {n} {k}} p ^ {k} (1 - p) ^ {n - k} f _ {u ^ {k} d ^ {n - k}}
$$

where:

$f _ { u ^ { k } d ^ { n - k } }$ is the payoff at the node reached by k up moves and n − k down moves;   
• $\binom { n } { k }$ is the binomial coefficient (number of paths to that node).

# Backward Induction for American Option

Let $\alpha = e ^ { - r \Delta t } p , \beta = e ^ { - r \Delta t } ( 1 - p )$ , then

$$
f _ {u} = \max \left\{\varphi (S u), \alpha f _ {u u} + \beta f _ {u d} \right\},
$$

$$
f _ {d} = \max \left\{\varphi (S d), \alpha f _ {u d} + \beta f _ {d d} \right\},
$$

$$
f = \max \left\{\varphi (S), \alpha f _ {u} + \beta f _ {d} \right\}.
$$

# Matching Volatility in Binomial Models

• To match volatility, we often set $u d = 1$ and for small $\Delta t .$ :

$$
u = e ^ {\sigma \sqrt {\Delta t}}, d = e ^ {- \sigma \sqrt {\Delta t}}.
$$

• The risk-neutral probability then becomes:

$$
p = \frac {e ^ {r \Delta t} - e ^ {- \sigma \sqrt {\Delta t}}}{e ^ {\sigma \sqrt {\Delta t}} - e ^ {- \sigma \sqrt {\Delta t}}}.
$$

# Definition: Brownian Motion

A stochastic process $B : [ 0 , \infty ) \times \Omega  \mathbb { R }$ is called a standard Brownian motion (or Wiener process) on a probability space $( \Omega , \mathcal { F } , \mathbb { P } )$ if

(a) $B _ { 0 } = 0$   
(b) The sample paths $t \mapsto B _ { t }$ are continuous;   
(c) Stationary increments: For any $t \ > \ s \ \geqslant \ 0 , \ B _ { t } \ - \ B _ { s } \ \sim$ $\mathcal { N } ( 0 , t - s )$ ;   
(d) Independent increments: For any $0 \leqslant t _ { 0 } < t _ { 1 } < \cdot \cdot \cdot < t _ { n } <$ $t _ { n + 1 }$ and $n \geqslant 1$ , the random variables

$$
B _ {t _ {0}}, B _ {t _ {1}} - B _ {t _ {0}}, B _ {t _ {2}} - B _ {t _ {1}}, \ldots , B _ {t _ {n + 1}} - B _ {t _ {n}}
$$

are independent.

# Doob’s Optional Stopping Theorem

# Theorem 8.1 (Doob’s Optional Stopping Theorem)

Suppose $\{ X _ { t } , t \geqslant 0 \}$ is a martingale and τ is a stopping time. If one of the following conditions holds:

• τ is a bounded random variable, i.e., $\tau \leqslant T$ for some constant   
• The stopped process $\{ X _ { t \wedge \tau } , t \geqslant 0 \}$ is bounded and $\tau < \infty$   
Then

$$
\mathbb {E} [ X _ {\tau} ] = X _ {0}.
$$

# Itô Isometry

# Theorem 8.2 (Itô Isometry)

For any processes $f \in { \mathcal { L } } ^ { 2 } ( [ 0 , T ] )$ , we have

$$
\mathbb {E} \left[ \left(\int_ {0} ^ {T} f (t) \mathrm{d} B _ {t}\right) ^ {2} \right] = \int_ {0} ^ {T} \mathbb {E} \left[ f ^ {2} (t) \right] \mathrm{d} t.
$$

# Theorem 8.3

For any two processes f, $g \in \mathcal L ^ { 2 } ( [ 0 , T ] )$ , we have

$$
\mathbb {E} \left[ \int_ {u} ^ {T} f (s) \mathrm{d} B _ {s} \mid \mathcal {F} _ {u} \right] = 0,
$$

$$
\mathbb {E} \left[ \int_ {u} ^ {T} f (s) \mathrm{d} B _ {s} \int_ {u} ^ {T} g (s) \mathrm{d} B _ {s} \Bigg | \mathcal {F} _ {u} \right] = \int_ {u} ^ {T} \mathbb {E} \left[ f (s) g (s) \mid \mathcal {F} _ {u} \right] \mathrm{d} s.
$$

# Definition: Itô Process

Itô process:

$$
X _ {t} = X _ {0} + \int_ {0} ^ {t} b (s) \mathrm{d} s + \int_ {0} ^ {t} \sigma (s) \mathrm{d} B _ {s}, \quad t \geqslant 0,
$$

Its differential form:

$$
\mathrm{d} X _ {t} = b (t) \mathrm{d} t + \sigma (t) \mathrm{d} B _ {t}.
$$

The quadratic variation process:

$$
\mathrm{d} \left<   X \right> _ {t} = | \sigma (t) | ^ {2} \mathrm{d} t.
$$

# Mean & Martingale

# Theorem 8.4

$$
I f \mathrm{d} X _ {t} = b (t) \mathrm{d} t + \sigma (t) \mathrm{d} B _ {t}. T h e n
$$

$$
\mathrm{d} \left(\mathbb {E} [ X _ {t} ]\right) = \mathbb {E} [ b (t) ] \mathrm{d} t.
$$

# Theorem 8.5

An Itô process is a martingale if and only if its drift is always zero, $i . e . , b ( t ) \equiv 0$ .

# Itô’s Lemma for General Itô Process

# Theorem 8.6 (Itô’s Lemma)

Let $\varphi ( t , x )$ be a deterministic smooth function and $X _ { t }$ be an Itô process. Then the process $\varphi ( t , X _ { t } )$ is also an Itô process. Moreover,

$$
\mathrm{d} \varphi (t, X _ {t}) = \varphi_ {t} (t, X _ {t}) \mathrm{d} t + \varphi_ {x} (t, X _ {t}) \mathrm{d} X _ {t} + \frac {1}{2} \varphi_ {x x} (t, X _ {t}) \mathrm{d} \langle X \rangle_ {t}.
$$

# Corollary 8.7

Let $\varphi ( x )$ be a deterministic smooth function and $X _ { t }$ be an Itô process. Then

$$
\mathrm{d} \varphi (X _ {t}) = \varphi_ {x} (X _ {t}) \mathrm{d} X _ {t} + \frac {1}{2} \varphi_ {x x} (X _ {t}) \mathrm{d} \langle X \rangle_ {t}.
$$

# Covariation Process

If $X _ { t }$ and $Y _ { t }$ are given by

$$
\mathrm{d} X _ {t} = b _ {1} (t) \mathrm{d} t + \sigma_ {1} (t) \mathrm{d} B _ {t},
$$

$$
\mathrm{d} Y _ {t} = b _ {2} (t) \mathrm{d} t + \sigma_ {2} (t) \mathrm{d} \overline {{B}} _ {t},
$$

where $\{ B _ { t } , t \geqslant 0 \}$ and $\{ \overline { { B } } _ { t } , t \geqslant 0 \}$ are two Brownian motions with a correlation $\rho _ { t }$ , i.e. $\mathrm { d } \langle B , \overline { { B } } \rangle _ { t } = \rho _ { t }$ dt. Then

$$
\langle X, Y \rangle_ {t} = \int_ {0} ^ {t} \rho (s) \sigma_ {1} (s) \sigma_ {2} (s) \mathrm{d} s, \quad t \geqslant 0.
$$

If one of $X _ { t }$ or $Y _ { t }$ is deterministic, then $\langle X , Y \rangle _ { t } = 0$ .

# Corollary 8.8 (Product Process)

For two Itô processes $X _ { t }$ and $Y _ { t }$ , we have

$$
\mathrm{d} (X _ {t} Y _ {t}) = Y _ {t} \mathrm{d} X _ {t} + X _ {t} \mathrm{d} Y _ {t} + \mathrm{d} \langle X, Y \rangle_ {t}.
$$

In particular, if one of $X _ { t }$ or $Y _ { t }$ has no volatility term (i.e., is deterministic), then

$$
\mathrm{d} (X _ {t} Y _ {t}) = Y _ {t} \mathrm{d} X _ {t} + X _ {t} \mathrm{d} Y _ {t}.
$$

# Multidimensional Itô’s Lemma

# Theorem 8.9 (Multidimensional Itô’s Lemma)

Let $\varphi ( t , x _ { 1 } , \cdots , x _ { n } )$ be a determinist smooth function and $X ^ { i } , i =$ 1, 2, · · · , n, are Itô processes. Then the process $\varphi ( t , X _ { t } ^ { 1 } , \cdots , X _ { t } ^ { n } )$ is also an Itô process. Moreover,

$$
\mathrm{d} \varphi (t, X _ {t} ^ {1}, \dots , X _ {t} ^ {n})
$$

$$
= \varphi_ {t} (t, X _ {t} ^ {1}, \dots , X _ {t} ^ {n}) \mathrm{d} t
$$

$$
+ \sum_ {i = 1} ^ {n} \varphi_ {x _ {i}} (t, X _ {t} ^ {1}, \dots , X _ {t} ^ {n}) \mathrm{d} X _ {t} ^ {i} + \frac {1}{2} \varphi_ {x _ {i} ^ {2}} (t, X _ {t} ^ {1}, \dots , X _ {t} ^ {n}) \mathrm{d} \langle X ^ {i} \rangle_ {t}
$$

$$
+ \sum_ {1 \leqslant i <   j \leqslant n} \varphi_ {x _ {i} x _ {j}} (t, X _ {t} ^ {1}, \dots , X _ {t} ^ {n}) \mathrm{d} \langle X ^ {i}, X ^ {j} \rangle_ {t}.
$$

# Black-Scholes PDE

For European options:

$$
V _ {t} (t, x) + \frac {1}{2} \sigma^ {2} x ^ {2} V _ {x x} (t, x) + r x V _ {x} (t, x) - r V (t, x) = 0, x > 0.
$$

For American options:

$$
\left\{ \begin{array}{l} \max \left\{\frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} x ^ {2} \frac {\partial^ {2} V}{\partial x ^ {2}} + r x \frac {\partial V}{\partial x} - r V, \varphi - V \right\} = 0, \\ V (T, x) = \varphi (x). \end{array} \right.
$$

# Black-Scholes Formulae

# Theorem 9.1 (Black-Scholes Formulae)

The price at time t of the vanilla European call option with strike K and maturity T is

$$
C _ {E} (t, x) = x N (d _ {1}) - K e ^ {- r (T - t)} N (d _ {2}),
$$

where x is the spot price of the (non-dividend-paying) stock, $N ( y ) =$ √12π R y−∞ e− s22 ds, and $\frac { 1 } { \sqrt { 2 \pi } } \int _ { - \infty } ^ { y } e ^ { - \frac { s ^ { 2 } } { 2 } }$ 2

$$
d _ {1, 2} = \frac {\ln (x) - \ln (K e ^ {- r (T - t)})}{\sigma \sqrt {T - t}} \pm \frac {1}{2} \sigma \sqrt {T - t}.
$$

The price of the corresponding European put option is

$$
P _ {E} (t, x) = K e ^ {- r (T - t)} N (- d _ {2}) - x N (- d _ {1}).
$$

# Greek Letters

# Definition 9.1 (Greek Letters)

The Greek Letters are defined as follows:

• Delta $( \Delta )$ : $\Delta ( t , x ) = V _ { x } ( t , x )$   
• Gamma (Γ): $\Gamma ( t , x ) = V _ { x x } ( t , x )$   
• Theta (Θ): $\Theta ( t , x ) = V _ { t } ( t , x )$   
• Rho (ρ): $\rho ( t , x ) = V _ { r } ( t , x )$   
• Vega (V): $\mathcal { V } ( t , x ) = V _ { \sigma } ( t , x )$

# Multiple Underlying Assets

Greek Letters are matrices if there are multiple underlying assets.

# Remarks on Greek Letters

Every derivative or portfolio has its own Greek letters, which depend on time and the underlying asset price.   
The letters Delta $\Delta ( t , x )$ and Gamma $\Gamma ( t , x )$ reflect the sensitivity of the value V of a derivative or portfolio with respect to the change of the underlying stock price x. Approximately,

$$
V (t, x + \epsilon) - V (t, x) \approx \epsilon \Delta (t, x) + \frac {1}{2} \epsilon^ {2} \Gamma (t, x).
$$

The other Greek letters have similar meanings.

The values of Greek letters are updated every day in practice. Their values are linear in the number of shares, and the sign will change for short positions.

# Greek Letter Hedging

# Example 9.1

Suppose we have a portfolio whose Delta is $\Delta _ { P } = - 4$ and Gamma is $\Gamma _ { P } = 3$ at present. We want to make it both $\Delta$ and Γ neutral by trading assets. Two assets A and B are available with the following Greek letters:

<table><tr><td>assets</td><td>A</td><td>B</td></tr><tr><td>Δ</td><td>0.5</td><td>0.2</td></tr><tr><td>Γ</td><td>0.3</td><td>0.3</td></tr></table>

# Continuous-Time Risk-Neutral Valuation

# Risk-Neutral World

The stock price in the risk-neutral world follows

$$
\mathrm{d} S _ {t} = r S _ {t} \mathrm{d} t + \sigma S _ {t} \mathrm{d} B _ {t} ^ {Q},
$$

where $\{ B _ { t } ^ { Q } , t \geqslant 0 \}$ is a standard Brownian motion in the risk-neutral world. Given that the stock price is $S _ { t } = x$ at time t, the price of an asset at time t is given by

$$
V (t, x) = e ^ {- r (T - t)} \mathbb {E} ^ {Q} \left[ \varphi (S _ {T}) \mid S _ {t} = x \right],
$$

where φ is the payoff function of the asset at time T , and $\mathbb { E } ^ { Q }$ means the expectation is taken in the risk-neutral world.

# Value of Perpetual American Put Option

# Theorem 9.2

When the spot stock price is S, the vanilla perpetual American put option has the value

$$
P _ {A} ^ {\infty} (S) = \frac {\sigma^ {2}}{2 r} \left(\frac {2 r K}{2 r + \sigma^ {2}}\right) ^ {2 r / \sigma^ {2} + 1} S ^ {- 2 r / \sigma^ {2}}.
$$

The option should be exercised when the stock price is lower than or equal to

$$
S _ {e} ^ {*} = \frac {2 r K}{2 r + \sigma^ {2}}.
$$

# PDE for Path-Dependent Options

# PDE for Path-Dependent Options

$$
\begin{array}{l} \frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} x ^ {2} \frac {\partial^ {2} V}{\partial x ^ {2}} + r x \frac {\partial V}{\partial x} - r V + \frac {\partial V}{\partial I} f (t, x) = 0, \\ (t, x, I) \in [ 0, T ] \times (0, \infty) \times (0, \infty). \\ \end{array}
$$

# Reflection Principle for Brownian Motion

• Mathematically,

$$
\mathbb {P} (B _ {T} \geqslant x, m _ {T} > y) = \mathbb {P} (x \leqslant B _ {T} \leqslant x - 2 y), y <   0, y \leqslant x;
$$

and

$$
\mathbb {P} (m _ {T} \geqslant y) = \mathbb {P} (- | B _ {T} | \geqslant y), y <   0.
$$

For any function $\varphi _ { i }$ , we have

$$
\begin{array}{l} \mathbb {E} [ \varphi (B _ {T}) \mathbb {1} _ {\mathcal {A}} ] = \mathbb {E} [ \varphi (2 y - B _ {T}) \mathbb {1} _ {\mathcal {B}} ] \\ = \mathbb {E} [ \varphi (2 y - B _ {T}) \mathbb {1} _ {B _ {T} \leqslant 2 y - x} ] \\ = \int_ {- \infty} ^ {2 y - x} \varphi (2 y - z) \frac {1}{\sqrt {2 \pi T}} e ^ {- \frac {z ^ {2}}{2 T}} d z. \\ \end{array}
$$

# Black-Scholes PDE for Down-and-Out Barrier Option

$$
\left\{ \begin{array}{l l} V _ {t} (t, x) + \frac {1}{2} \sigma^ {2} x ^ {2} V _ {x x} (t, x) + r x V _ {x} (t, x) - r V (t, x) = 0, \\ \qquad \qquad \qquad \qquad \qquad (t, x) \in [ 0, T ] \times (B, \infty), \\ V (T, x) = \varphi (x), & x > B. \end{array} \right.
$$