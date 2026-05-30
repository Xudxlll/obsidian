# Structured Products 1: Dual Currency Deposits

Guanghua Lian

# 1 Introduce to DCD

A dual currency deposit (DCD) is a very popular and liquidly traded standard FX-linked investment, that works like a reverse convertible bond in the equity markets. Investors searching for higher yields are selling a vanilla call on the deposit currency, which is also a put on another currency, to receive a higher coupon and then hope that the option they sold will be out-of-the- money at maturity. Some banks also name it enhanced deposit or DCI.

The product works like this. An investor deposits an amount in say EUR for a fixed time horizon, usually from one day up to one year, and instead of the market interest rate she receives a higher coupon. For example, she invests 5 million EUR for 1 month (we take 30/360 years here), where the market rate is 3.00%, which would return 12,500 EUR interest payment. The higher and fully guaranteed coupon is then for example 5.00% = 20,833 EUR. For this can’t be a free lunch, the investor is taking the following risk. At a EUR-CHF spot reference of 1.4662 he chooses a strike of 1.4700. If at maturity the spot stays below 1.4700 (strong CHF), then the investor is paid back the full notional in EUR. Conversely, if the spot at maturity is above 1.4700 (weak CHF), then the notional is converted into CHF 7.35 Million. So the investor is always paid back the weaker currency. The interest rate with the enhanced coupon of 5.00%is paid in either case.

# 1.1 Examples of DCD

It is a short-term (1 week–12 months) product for yield enhancement that involves a base currency and an alternative currency. The investor of a DCI with initial investment in base currency believes that the alternative currency will not depreciate against the base currency and wants to monetize this view for an enhanced yield. At maturity of the DCI:

• if the FX spot fixing at maturity is equal or higher than Strike (expressed as units of alternative currency per base currency): the investor will receive the total amount of principal plus interest in base currency;   
• otherwise, the investor will receive the total amount of principal plus interest in alternative currency converted with Strike.

Table 31.13 Illustrative example Dual Currency Investment (DCI) 

<table><tr><td>Note tenor</td><td>2 months</td></tr><tr><td>Notional (N)</td><td>USD 100,000</td></tr><tr><td>Base currency</td><td>USD</td></tr><tr><td>Alternative currency</td><td>JPY</td></tr><tr><td>Spot reference (i.e., initial spot)</td><td>111.00</td></tr><tr><td>Strike (K)</td><td>1/113.01 (USD units per JPY)</td></tr><tr><td>Coupon (C)</td><td>1% (6% p.a.)</td></tr><tr><td>Final spot  $X_{T}$ </td><td>Expressed as USD units per JPY</td></tr><tr><td>Final redemption</td><td>If  $X_{T} \geq K$ ,  $N(1 + C) = 101,000$  in USD otherwise,  $N(1 + C)/K = 11,414,010$  in JPY</td></tr></table>

In a DCI, the investor’s exposure is short a put option on alternative currency at strike, which is shown by the final value measured in the same currency (that is USD in our example):

$$
\operatorname{Value} _ {T} = N (1 + C) \cdot \mathbf {1} _ {\{X _ {T} \geq K \}} + \left(\frac {X _ {T} \cdot N (1 + C)}{K}\right) \cdot \mathbf {1} _ {\{X _ {T} <   K \}}
$$

# 1.2 Advantages

• Guaranteed higher coupon than market   
• Liquid product, whence sales margins are comparatively small   
• An exporting company in the country of the other currency needs to buy the other currency anyway and can use the strike as a budget rate   
• Investor can take a short option position

# 1.3 Disadvantages

• No capital guarantee: if the other currency becomes worthless, then the investor can lose the entire capital   
• The investor receives a higher coupon at the cost of taking unlimited exchange rate risk, see Figure 2.10   
• Investor has to pay tax on the enhanced coupon, but cannot tax-deduct the risk on the upside

# 1.4 Discussions

The premium of the short option must be paid at delivery of the deposit. The DCD is an ideal way for a bank to buy options from their clients without taking any credit risk. Since the bank has the deposit amount, it can never get into a situation of a defaulting client. Conversely, the investor is taking the credit default risk of the issuer as in any other deposit. Surely, the better the rating of the issuer, the lower the coupon. This extends to the DCD. The exchange rate risk can be reduced by taking a strike sufficiently far away from the spot. However, selling such a far out-of-the-money option will not enhance the coupon significantly.

The investor is obviously taking risk on the upside. What if the investor believes in an upward trend and would rather take risk on the downside? One can then take the other currency. But if she wants to invest in the same currency, a similar structure as in the dual currency deposit does not work in a sellable way. Of course, the investor can always sell a put on the deposit currency. However, at maturity, the payoff of the put would have to be cash-settled in the deposit currency and this payoff then subtracted from the deposit amount.

# 2 Pricing DCD Using Black-Scholes Framework

# 2.1 Payoff Function at Expiration

The payoff of the derivative at maturity T is:

$$
\begin{array}{l} \mathrm{Value} _ {T} = N (1 + C) \cdot \mathbf {1} _ {\{X _ {T} \geq K \}} + \left(\frac {X _ {T} \cdot N (1 + C)}{K}\right) \cdot \mathbf {1} _ {\{X _ {T} <   K \}} \\ = N (1 + C) \left(1 - \frac {1}{K} \cdot (K - X _ {T}) \cdot \mathbf {1} _ {\{X _ {T} <   K \}}\right) \\ = N (1 + C) \left(1 - \frac {1}{K} \cdot \max \{0, K - X _ {T} \}\right) \\ \end{array}
$$

# 2.2 Decomposition of the Payoff

The derivative can be decomposed into two components:

$$
\mathrm{Value} _ {T} = \underbrace {N (1 + C)} _ {\mathrm{Risk-freebond}} - \underbrace {\frac {N (1 + C)}{K} \max \left\{0 , K - X _ {T} \right\}} _ {\mathrm{Shortputoption}}.
$$

# 2.3 Pricing Components

# 2.3.1 Risk-Free Bond

The present value of the bond component:

$$
\mathrm{PV} _ {\mathrm{Bond}} = N (1 + C) e ^ {- r T}
$$

# 2.3.2 Short Put Option

The Black-Scholes price of the put option:

$$
\mathrm{Put} = K e ^ {- r T} \Phi (- d _ {2}) - X _ {0} e ^ {- q T} \Phi (- d _ {1})
$$

where:

$$
d _ {1} = \frac {\ln (X _ {0} / K) + (r - q + \sigma^ {2} / 2) T}{\sigma \sqrt {T}}, d _ {2} = d _ {1} - \sigma \sqrt {T}
$$

The present value of the short put component:

$$
\mathrm{PV} _ {\mathrm{Put}} = \frac {N (1 + C)}{K} \left[ K e ^ {- r T} \Phi (- d _ {2}) - X _ {0} e ^ {- q T} \Phi (- d _ {1}) \right]
$$

# 2.4 Total Present Value

Combining both components:

$$
\begin{array}{l} \mathrm{PV} _ {\mathrm{DCD}} = \mathrm{PV} _ {\mathrm{Bond}} - \mathrm{PV} _ {\mathrm{Put}} \\ = N (1 + C) e ^ {- r T} - \frac {N (1 + C)}{K} \left[ K e ^ {- r T} \Phi (- d _ {2}) - X _ {0} e ^ {- q T} \Phi (- d _ {1}) \right] \\ = N (1 + C) \left[ e ^ {- r T} \Phi (d _ {2}) + \frac {X _ {0}}{K} e ^ {- q T} \Phi (- d _ {1}) \right] \\ \end{array}
$$

Final explicit formula:

$$
\boxed {\mathrm{PV} _ {\mathrm{DCD}} = N (1 + C) \left[ e ^ {- r T} \Phi (d _ {2}) + \frac {X _ {0}}{K} e ^ {- q T} \Phi (- d _ {1}) \right]}
$$

# 2.5 Example Calculation

Assume:

• $N = \ S 1 0 0 0 , C = 5 \% , K = 1 0 0 , X _ { 0 } = 1 0 5$   
• r = 3%, q = 1%, σ = 20%, T = 1 year

Compute:

$$
d _ {1} = \frac {\ln (1 0 5 / 1 0 0) + (0 . 0 3 - 0 . 0 1 + 0 . 2 ^ {2} / 2)}{0 . 2} \approx 0. 6 5, \quad d _ {2} = 0. 6 5 - 0. 2 \approx 0. 4 5
$$

$$
\Phi (d _ {2}) \approx 0. 6 7 3 6, \quad \Phi (- d _ {1}) \approx 0. 2 5 7 8
$$

$$
\mathrm{PV} = 1 0 0 0 \times 1. 0 5 \left[ e ^ {- 0. 0 3} \times 0. 6 7 3 6 + \frac {1 0 5}{1 0 0} e ^ {- 0. 0 1} \times 0. 2 5 7 8 \right] \approx   (1 0 7 5
$$

# 3 Extensions: Pricing DCD Using Heston Stochastic Volatility Model

# 3.1 Heston Physical Measure Dynamics

Under the physical measure P:

$$
d X _ {t} = \mu X _ {t} d t + \sqrt {v _ {t}} X _ {t} d W _ {t} ^ {X, \mathbb {P}},
$$

$$
d v _ {t} = \kappa (\theta - v _ {t}) d t + \sigma \sqrt {v _ {t}} d W _ {t} ^ {v, \mathbb {P}},
$$

$$
d W _ {t} ^ {X, \mathbb {P}} d W _ {t} ^ {v, \mathbb {P}} = \rho d t,
$$

where $\mu , \kappa , \theta , \sigma , \rho , v _ { 0 }$ are defined as in the text.

# 3.2 Risk-Neutral Measure Dynamics

Under the risk-neutral measure $\mathbb { Q } \mathrm { : }$

$$
d X _ {t} = (r - q) X _ {t} d t + \sqrt {v _ {t}} X _ {t} d W _ {t} ^ {X, \mathbb {Q}},
$$

$$
d v _ {t} = \kappa^ {*} (\theta^ {*} - v _ {t}) d t + \sigma \sqrt {v _ {t}} d W _ {t} ^ {v, \mathbb {Q}},
$$

$$
d W _ {t} ^ {X, \mathbb {Q}} d W _ {t} ^ {v, \mathbb {Q}} = \rho d t,
$$

with $\begin{array} { r } { \kappa ^ { * } = \kappa + \lambda , \theta ^ { * } = \frac { \kappa \theta } { \kappa + \lambda } } \end{array}$ .

# 3.3 Method 1: Risk-Neutral Valuation Approach

# 3.3.1 Heston Characteristic Function

The characteristic function $\phi ( u ) = \mathbb { E } ^ { \mathbb { Q } } [ e ^ { i u \ln X _ { T } } ]$ is:

$$
\phi (u) = e ^ {C (u, T) + D (u, T) v _ {0} + i u \ln X _ {0}},
$$

where $C ( u , T )$ and $D ( u , T )$ solve the Riccati equations.

# 3.3.2 Solving the Riccati Equations

The explicit solutions are:

$$
C (u, T) = (r - q) i u T + \frac {\kappa^ {*} \theta^ {*}}{\sigma^ {2}} \left[ (\beta - d) T - 2 \ln \left(\frac {1 - g e ^ {d T}}{1 - g}\right) \right],
$$

$$
D (u, T) = \frac {\beta - d}{\sigma^ {2}} \left(\frac {1 - e ^ {d T}}{1 - g e ^ {d T}}\right),
$$

$$
d = \sqrt {\beta^ {2} - \sigma^ {2} (2 \alpha i u - u ^ {2})},
$$

$$
g = \frac {\beta - d}{\beta + d},
$$

$$
\alpha = - \frac {u ^ {2} + i u}{2},
$$

$$
\beta = \kappa^ {*} - \rho \sigma i u.
$$

# 3.3.3 Fourier Inversion for Put Price

The put price requires computing:

$$
\mathrm{Put} = K e ^ {- r T} P _ {2} - X _ {0} e ^ {- q T} P _ {1},
$$

with probabilities:

$$
P _ {1} = \frac {1}{2} + \frac {1}{\pi} \int_ {0} ^ {\infty} \operatorname{Re} \left(\frac {e ^ {- i u \ln K} \phi (u - i)}{i u \phi (- i)}\right) d u,
$$

$$
P _ {2} = \frac {1}{2} + \frac {1}{\pi} \int_ {0} ^ {\infty} \mathrm{Re} \left(\frac {e ^ {- i u \ln K} \phi (u)}{i u}\right) d u.
$$

# 3.3.4 Final DCD Pricing Formula

$$
\boxed {\mathrm{PV} _ {\mathrm{DCD}} = N (1 + C) \left[ e ^ {- r T} - \frac {1}{K} \left(K e ^ {- r T} P _ {2} - X _ {0} e ^ {- q T} P _ {1}\right) \right].}
$$

# 3.4 Method 2: PDE Method

# 3.4.1 Deriving the Heston PDE

Applying Itˆo’s lemma to $V ( t , X , v )$ :

$$
\frac {\partial V}{\partial t} + (r - q) X \frac {\partial V}{\partial X} + \kappa^ {*} (\theta^ {*} - v) \frac {\partial V}{\partial v} + \frac {1}{2} v X ^ {2} \frac {\partial^ {2} V}{\partial X ^ {2}} + \frac {1}{2} \sigma^ {2} v \frac {\partial^ {2} V}{\partial v ^ {2}} + \rho \sigma v X \frac {\partial^ {2} V}{\partial X \partial v} - r V = 0.
$$

# 3.4.2 Boundary Conditions

• Terminal: $\begin{array} { r } { V ( T , X , v ) = N ( 1 + C ) \left( 1 - \frac { 1 } { K } \operatorname* { m a x } ( K - X , 0 ) \right) } \end{array}$ .   
• $X \to \infty \colon V ( t , X , v ) \to N ( 1 + C ) e ^ { - r ( T - t ) } .$   
• v = 0: Simplified PDE applies.

# 3.4.3 Feynman-Kac Representation

By the Feynman-Kac theorem:

$$
V (t, X, v) = e ^ {- r (T - t)} \mathbb {E} ^ {\mathbb {Q}} \left[ \mathrm{Value} _ {T} \mid X _ {t} = X, v _ {t} = v \right],
$$

confirming equivalence between PDE and risk-neutral approaches.

# 3.5 Method 3: COS Method for Fourier Inversion

# 3.5.1 Truncation Interval

The domain $[ a , b ]$ for $y = \ln X _ { T }$ is chosen as:

$$
a = \mathbb {E} ^ {\mathbb {Q}} [ y ] - L \sqrt {\mathbb {V} \mathrm{ar} ^ {\mathbb {Q}} [ y ]}, \quad b = \mathbb {E} ^ {\mathbb {Q}} [ y ] + L \sqrt {\mathbb {V} \mathrm{ar} ^ {\mathbb {Q}} [ y ]},
$$

where $\mathbb { E } ^ { \mathbb { Q } } [ y ]$ and $\mathbb { V } \mathrm { a r } ^ { \mathbb { Q } } [ y ]$ are derived from Heston cumulants.

# 3.5.2 Fourier-Cosine Series Expansion

Approximate the PDF $f ( y )$ :

$$
f (y) \approx \frac {2}{b - a} \sum_ {k = 0} ^ {N - 1} \operatorname{Re} \left(\phi \left(\frac {k \pi}{b - a}\right) e ^ {- i \frac {k \pi a}{b - a}}\right) \cos \left(\frac {k \pi (y - a)}{b - a}\right).
$$

# 3.5.3 Put Option Price via COS

The put price becomes:

$$
\mathrm{Put} \approx e ^ {- r T} \sum_ {k = 0} ^ {N - 1} \mathrm{Re} \left(\phi \left(\frac {k \pi}{b - a}\right) e ^ {- i \frac {k \pi a}{b - a}}\right) V _ {k},
$$

with payoff coefficients:

$$
V _ {k} = \left\{ \begin{array}{l l} \frac {2}{b - a} \left(e ^ {k} \chi_ {k} (0, c) - \psi_ {k} (0, c)\right), & k \neq 0, \\ \frac {2}{b - a} \left(e ^ {k} (c - a) - (e ^ {c} - e ^ {a})\right), & k = 0. \end{array} \right.
$$

# 3.5.4 Probabilities $P _ { 1 }$ and $P _ { 2 }$ via COS

$$
\begin{array}{l} P _ {1} \approx \sum_ {k = 0} ^ {N - 1} \operatorname{Re} \left(\phi \left(\frac {k \pi}{b - a} - i\right) e ^ {- i \frac {k \pi a}{b - a}}\right) U _ {k} ^ {(1)}, \\ P _ {2} \approx \sum_ {k = 0} ^ {N - 1} \operatorname{Re} \left(\phi \left(\frac {k \pi}{b - a}\right) e ^ {- i \frac {k \pi a}{b - a}}\right) U _ {k} ^ {(2)}. \\ \end{array}
$$

# 3.5.5 Example: COS Implementation

Assume:

• $N = 1 2 8 , L = 1 0 ,$   
• EQ[y] = ln X0 + (r − q − v0 )T ,   
• $\begin{array} { r } { \mathbb { V } \mathrm { a r } ^ { \mathbb Q } [ y ] = v _ { 0 } T + \frac { \theta ^ { * } \sigma ^ { 2 } T ^ { 2 } } { 2 \kappa ^ { * } } . } \end{array}$ θ∗σ2T 2

Compute $a = 3 . 0 , b = 5 . 0$ , and truncate the series at $N = 1 2 8$ . The error is $O ( e ^ { - N } )$ .