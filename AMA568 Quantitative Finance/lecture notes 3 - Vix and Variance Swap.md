# VIX and Variance Swap

Min Dai https://sites.google.com/view/mindai

The Hong Kong Polytechnic University

# Contents

1 Estimate of Historical Volatility 2   
2 Variance Swap 2

2.1 Realized Volatility and Volatility Products . . 2   
2.2 Continuous-Time Approximation to Realized Volatility 3   
2.3 Variance Swap Rate 3

3 VIX 5

3.1 Definition of (New) VIX 5   
3.2 Linkage between VIX and Variance Swap Rate . . . 6   
3.3 How to Use VIX or Variance/Volatility Swaps? 6

Volatility is a measure of variation in the price of a financial instrument over time.

# 1 Estimate of Historical Volatility

Recall the price process of an underlying asset in the Black-Scholes model:

$$
\frac {d S _ {t}}{S _ {t}} = \mu d t + \sigma d B _ {t}. \tag {1}
$$

A historical (constant) volatility is derived from time series of past market prices of the underlying under the assumption of (1), which can be rewritten as

$$
d \ln S _ {t} = \left(\mu - \frac {\sigma^ {2}}{2}\right) d t + \sigma d B _ {t}.
$$

Denote $t _ { i } = i \delta t , i = 0 , 1 , \ldots , N$ and $S _ { i } : = S _ { t _ { i } }$ . Consider the discretization of the above SDE:

$$
\ln {\frac {S _ {i}}{S _ {i - 1}}} = \ln S _ {i} - \ln S _ {i - 1} \approx \left(\mu - \frac {\sigma^ {2}}{2}\right) \delta t + \sigma \phi \sqrt {\delta t}, i = 1, 2, \ldots , N,
$$

where $\mathbb { E } ( \phi ) = 0 , \operatorname { V a r } ( \phi ) = \mathbb { E } ( \phi ^ { 2 } ) = 1$ . It follows that

$$
\left(\ln \frac {S _ {i}}{S _ {i - 1}}\right) ^ {2} = \left[ \left(\mu - \frac {\sigma^ {2}}{2}\right) \delta t + \sigma \phi \sqrt {\delta t} \right] ^ {2} \approx \sigma^ {2} \phi^ {2} \delta t,
$$

namely,

$$
\mathbb {E} \left[ \left(\ln \frac {S _ {i}}{S _ {i - 1}}\right) ^ {2} \right] \approx \sigma^ {2} \delta t.
$$

Then we can estimate the historical volatility by

$$
\sigma = \sqrt {\frac {1}{\delta t} \frac {1}{N} \sum_ {i = 1} ^ {N} \left(\ln \frac {S _ {i}}{S _ {i - 1}}\right) ^ {2}}. \tag {2}
$$

# 2 Variance Swap

# 2.1 Realized Volatility and Volatility Products

Equation (2) motivates us to define the realized volatility from time 0 to $T = N \delta t$ :

$$
\mathrm{RealizedVolatility} = \sqrt {\frac {2 5 2}{N} \sum_ {i = 1} ^ {N} \left(\ln \frac {S _ {i}}{S _ {i - 1}}\right) ^ {2}},
$$

where we use daily prices $S _ { i }$ (so $\delta t = 1 / 2 5 2 )$ , and N is the number of business days from and including the effective date to the maturity date.

In terms of the realized volatility, we can define the payoff of

• Variance swap:

$$
\text { Notional   Amount } \times \left(\text { Realized   Volatility } ^ {2} - \text { Fixed   Vol } ^ {2}\right)
$$

$$
= \text {Notional Amount} \times \left(\frac {2 5 2}{N} \sum_ {i = 1} ^ {N} \left(\ln \frac {S _ {i}}{S _ {i - 1}}\right) ^ {2} - X _ {v a r}\right).
$$

• Volatility swap:

$$
\text { Notional   Amount } \times (\text { Realized   Volatility } - \text { Fixed   Vol })
$$

$$
= \text {Notional Amount} \times \left(\sqrt {\frac {2 5 2}{N} \sum_ {i = 1} ^ {N} \left(\ln \frac {S _ {i}}{S _ {i - 1}}\right) ^ {2}} - X _ {v o l}\right).
$$

Without loss of generality, we will assume that the notional amount is 1.

# 2.2 Continuous-Time Approximation to Realized Volatility

In reality, volatility is not constant. In what follows, we always assume

$$
\frac {d S _ {t}}{S _ {t}} = \mu_ {t} d t + \sigma_ {t} d B _ {t},
$$

where $\sigma _ { t }$ is an adapted process. Again,

$$
d \ln S _ {t} = \left(\mu_ {t} - \frac {\sigma_ {t} ^ {2}}{2}\right) d t + \sigma_ {t} d B _ {t}.
$$

Then

$$
\frac {2 5 2}{N} \sum_ {i = 1} ^ {N} \left(\ln \frac {S _ {i}}{S _ {i - 1}}\right) ^ {2} \approx \frac {1}{N \delta t} \sum_ {i = 1} ^ {N} \sigma_ {t _ {i - 1}} ^ {2} \delta t \rightarrow \frac {1}{T} \int_ {0} ^ {T} \sigma_ {t} ^ {2} d t
$$

as $N \to + \infty .$

Recall the payoff of a variance swap

$$
\frac {2 5 2}{N} \sum_ {i = 1} ^ {N} \left(\ln \frac {S _ {i}}{S _ {i - 1}}\right) ^ {2} - X _ {v a r},
$$

whose continuous-time limit is

$$
\frac {1}{T} \int_ {0} ^ {T} \sigma_ {t} ^ {2} d t - X _ {v a r}.
$$

# 2.3 Variance Swap Rate

Now let us examine the variance swap rate, which is the fair value of $X _ { v a r }$ such that the variance swap has zero value at time 0:

$$
e ^ {- r T} \widehat {\mathbb {E}} \left[ \frac {1}{T} \int_ {0} ^ {T} \sigma_ {t} ^ {2} d t - X _ {v a r} \right] = 0,
$$

namely,

$$
X _ {v a r} = \widehat {\mathbb {E}} \left[ \frac {1}{T} \int_ {0} ^ {T} \sigma_ {t} ^ {2} d t \right]. \tag {3}
$$

In the risk-neutral world,

$$
d \ln S _ {t} = \left(r - \frac {\sigma_ {t} ^ {2}}{2}\right) d t + \sigma_ {t} d \widehat {B} _ {t}.
$$

It follows that

$$
\begin{array}{l} \int_ {0} ^ {T} \frac {\sigma_ {t} ^ {2}}{2} d t = \int_ {0} ^ {T} r d t + \int_ {0} ^ {T} \sigma_ {t} d \widehat {B} _ {t} - \int_ {0} ^ {T} d \ln S _ {t} \\ = r T - \ln \frac {S _ {T}}{S _ {0}} + \int_ {0} ^ {T} \sigma_ {t} d \widehat {B} _ {t} \\ = - \ln \frac {S _ {T}}{S _ {0} e ^ {r T}} + \int_ {0} ^ {T} \sigma_ {t} d \widehat {B} _ {t} =: - \ln \frac {S _ {T}}{F} + \int_ {0} ^ {T} \sigma_ {t} d \widehat {B} _ {t}, \\ \end{array}
$$

where $F = S _ { 0 } e ^ { r T }$ is the forward price.

Therefore, we can rewrite the payoff of the variance swap as

$$
\frac {1}{T} \int_ {0} ^ {T} \sigma_ {t} ^ {2} d t = \frac {2}{T} \left[ - \ln \frac {S _ {T}}{F} + \int_ {0} ^ {T} \sigma_ {t} d \widehat {B} _ {t} \right]. (4)
$$

Since $\int _ { 0 } ^ { T } \sigma _ { t } d \widehat { B } _ { t }$ is a martingale in the risk-neutral world, the payoff of the variance swap is equivalent to a log payoff

$$
- \ln {\frac {S _ {T}}{F}}.
$$

The log payoff has the following decomposition:

$$
\begin{array}{l} - \ln \frac {S _ {T}}{F} = - \frac {S _ {T} - F}{F} \quad (\text { forward   contract }) \\ + \int_ {F} ^ {+ \infty} \frac {1}{K ^ {2}} (S _ {T} - K) ^ {+} d K \quad (\mathrm{out-of-the-moneycall}) \\ + \int_ {0} ^ {F} \frac {1}{K ^ {2}} (K - S _ {T}) ^ {+} d K \quad (\text { out   -   of   -   the   -   money   put }). \tag {5} \\ \end{array}
$$

Proof of Identity (5): For any smooth function f(x), one has

$$
\begin{array}{l} f (x) = f (a) + f ^ {\prime} (a) (x - a) + \int_ {a} ^ {x} f ^ {\prime \prime} (K) (x - K) d K \\ = f (a) + f ^ {\prime} (a) (x - a) + \int_ {a} ^ {x} f ^ {\prime \prime} (K) \left[ (x - K) ^ {+} - (K - x) ^ {+} \right] d K \\ = f (a) + f ^ {\prime} (a) (x - a) + \int_ {a} ^ {x} f ^ {\prime \prime} (K) (x - K) ^ {+} d K + \int_ {x} ^ {a} f ^ {\prime \prime} (K) (K - x) ^ {+} d K \\ = f (a) + f ^ {\prime} (a) (x - a) + \int_ {a} ^ {+ \infty} f ^ {\prime \prime} (K) (x - K) ^ {+} d K + \int_ {0} ^ {a} f ^ {\prime \prime} (K) (K - x) ^ {+} d K. \\ \end{array}
$$

The desired result follows by choosing $\begin{array} { r } { f ( x ) = - \ln { \frac { x } { F } } , a = F } \end{array}$ , and $x = S _ { T }$ . This completes the proof.

Remark: The above result implies that a variance swap can be replicated by vanilla options.

The combination of (3)–(5) yields

$$
\begin{array}{l} K _ {v a r} = \frac {2}{T} \left[ \int_ {F} ^ {+ \infty} \frac {1}{K ^ {2}} \widehat {\mathbb {E}} (S _ {T} - K) ^ {+} d K + \int_ {0} ^ {F} \frac {1}{K ^ {2}} \widehat {\mathbb {E}} (K - S _ {T}) ^ {+} d K \right] \\ = \frac {2}{T} \left[ \int_ {F} ^ {+ \infty} \frac {1}{K ^ {2}} e ^ {r T} C (S _ {0}, 0; K, T) d K + \int_ {0} ^ {F} \frac {1}{K ^ {2}} e ^ {r T} P (S _ {0}, 0; K, T) d K \right], \tag {6} \\ \end{array}
$$

where C and P are the prices of European call and put options, respectively.

# 3 VIX

The definition of the old VIX is based on the implied volatility of at-the-money options on the S&P 100. The new VIX is linked to the variance swap, which is a volatility product.

# 3.1 Definition of (New) VIX

The (new) VIX index is a volatility index for the S&P 500, defined as

$$
V I X = 1 0 0 \sqrt {\frac {3 6 5}{3 0} \left[ T _ {1} V _ {T _ {1}} \frac {N _ {2} - 3 0}{N _ {2} - N _ {1}} + T _ {2} V _ {T _ {2}} \frac {3 0 - N _ {1}}{N _ {2} - N _ {1}} \right]},
$$

where

$$
V _ {T} = \frac {2}{T} \sum_ {i} \frac {\Delta K _ {i}}{K _ {i} ^ {2}} e ^ {r T} Q (K _ {i}) - \frac {1}{T} \left(\frac {F}{K _ {0}} - 1\right) ^ {2}, \tag {7}
$$

and

(i) $N _ { 1 }$ and $N _ { 2 }$ denote the number of actual days to expiration for the two nearest maturities. (When the nearest time to maturity is 8 days or fewer, the CBOE switches to the next-nearest maturity to avoid microstructure effects.)   
(ii) $Q ( K _ { i } )$ : The midpoint of the bid-ask spread for each out-of-the-money option with strike $K _ { i }$ .   
(iii) F : the forward S&P 500 index level $( \boldsymbol { F } = S _ { 0 } e ^ { r T }$ assuming constant interest rate). In reality, we use

$$
F = e ^ {r T} [ C (K) - P (K) ] + K,
$$

where we choose a pair of put and call options with prices closest to each other.

(iv) $K _ { 0 } { \mathrm { : } }$ the first strike below F , namely $K _ { 0 } \leq F$ .   
(v) $K _ { i } \colon$ strike price of the ith out-of-the-money option; a call if $K _ { i } > K _ { 0 }$ , a put if $K _ { i } < K _ { 0 }$ , and both put and call if $K _ { i } = K _ { 0 }$ . That is, $Q ( K _ { 0 } )$ represents the average of the call and put option prices at this strike.

(vi) $\Delta K _ { i } = ( K _ { i + 1 } - K _ { i - 1 } ) / 2 \colon$ ; ∆K for the lowest strike is simply the difference between the lowest strike and the next higher strike. Likewise, $\Delta K$ for the highest strike is the difference between the highest strike and the next lower strike.

# 3.2 Linkage between VIX and Variance Swap Rate

If $K _ { 0 } = F$ , then Equation (7) is a straightforward discretization of (6). If $K _ { 0 } < F$ , then replacing F with $K _ { 0 }$ in Equation (5) gives

$$
- \ln {\frac {S _ {T}}{K _ {0}}} = - \frac {S _ {T} - K _ {0}}{K _ {0}} + \int_ {K _ {0}} ^ {+ \infty} \frac {1}{K ^ {2}} (S _ {T} - K) ^ {+} d K + \int_ {0} ^ {K _ {0}} \frac {1}{K ^ {2}} (K - S _ {T}) ^ {+} d K.
$$

Then

$$
\begin{array}{l} K _ {v a r} = \frac {2}{T} \widehat {\mathbb {E}} \left[ - \ln \frac {S _ {T}}{F} \right] = \frac {2}{T} \widehat {\mathbb {E}} \left[ - \ln \frac {S _ {T}}{K _ {0}} + \ln \frac {F}{K _ {0}} \right] \\ = \frac {2}{T} \widehat {\mathbb {E}} \left[ - \frac {S _ {T} - K _ {0}}{K _ {0}} + \ln \frac {F}{K _ {0}} \right] \\ + \frac {2}{T} \left[ \int_ {K _ {0}} ^ {+ \infty} \frac {1}{K ^ {2}} e ^ {r T} C (S _ {0}, 0; K, T) d K + \int_ {0} ^ {K _ {0}} \frac {1}{K ^ {2}} e ^ {r T} P (S _ {0}, 0; K, T) d K \right]. \\ \end{array}
$$

Note that

$$
\begin{array}{l} \widehat {\mathbb {E}} \left[ - \frac {S _ {T} - K _ {0}}{K _ {0}} + \ln \frac {F}{K _ {0}} \right] = - \frac {F - K _ {0}}{K _ {0}} + \ln \frac {F}{K _ {0}} \\ = - \frac {F - K _ {0}}{K _ {0}} + \left(\frac {F}{K _ {0}} - 1\right) - \frac {1}{2} \left(\frac {F}{K _ {0}} - 1\right) ^ {2} + O \left(\left(\frac {F}{K _ {0}} - 1\right) ^ {3}\right) \\ = - \frac {1}{2} \left(\frac {F}{K _ {0}} - 1\right) ^ {2} + O \left(\left(\frac {F}{K _ {0}} - 1\right) ^ {3}\right), \\ \end{array}
$$

which leads to the desired result by omitting the cubic and higher order terms.

# 3.3 How to Use VIX or Variance/Volatility Swaps?

The presumption is that as equity markets fall, volatility tends to rise.

• Going long a variance/volatility swap or VIX futures can provide an offset for a longonly fund in falling market conditions.   
• Investors seeking to hedge against decreased liquidity, since liquidity tends to decrease during increased levels of volatility.   
• Insurance companies that might like to hedge some of their underlying business exposures to volatility in the marketplace.   
• Option trading firms may want to use VIX futures or variance/volatility swaps to offset their exposure to market fluctuations. Additionally, option trading firms typically benefit from higher volatility since it correlates to increased trading activity.