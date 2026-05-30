# Capital Asset Pricing Model

Lecturer: Selena QIAN

Hong Kong Polytechnic University

January 21, 2026

Theorem: Assume there is a risk-free asset.

Consider any mean variance efficient portfolio with a return $R ^ { * }$ , i.e.

$$
R ^ {*} = (1 - \sum_ {n = 1} ^ {N} w _ {n} ^ {*}) r + \sum_ {n = 1} ^ {N} w _ {n} ^ {*} R _ {n}.
$$

(i) For any portfolio (not necessarily MV efficient) with return R

$$
E [ R ] - r = \frac {C o v (R , R ^ {*})}{V a r (R ^ {*})} (E [ R ^ {*} ] - r) \quad \text { or } \quad \frac {E [ R ] - r}{\sigma (R)} = \rho (R, R ^ {*}) \frac {E [ R ^ {*} ] - r}{\sigma (R ^ {*})},
$$

where $\rho ( R , R ^ { * } )$ is the correlation between R and $R ^ { * }$ .

(ii) Let R˜∗ = PNn=1 w ∗ n Rn $\begin{array} { r } { \tilde { R } ^ { * } = \frac { \sum _ { n = 1 } ^ { N } w _ { n } ^ { * } R _ { n } } { \sum _ { n = 1 } ^ { N } w _ { n } ^ { * } } } \end{array}$ to be the risky part return of an MV efficient portfolio PNn=1 w ∗n $\big ( w _ { 1 } ^ { * } , . . . , w _ { N } ^ { * } \big )$ . Then

$$
E [ R ] - r = \frac {C o v (R , \tilde {R} ^ {*})}{V a r (\tilde {R} ^ {*})} (E [ \tilde {R} ^ {*} ] - r) \quad \text {or} \quad \frac {E [ R ] - r}{\sigma (R)} = \rho (R, \tilde {R} ^ {*}) \frac {E [ \tilde {R} ^ {*} ] - r}{\sigma (\tilde {R} ^ {*})}.
$$

$$
\operatorname{Cov} \left(R, R ^ {*}\right) = \operatorname{Cov} \left(\left(1 - \sum_ {n = 1} ^ {N} w _ {n}\right) r + \sum_ {n = 1} ^ {N} w _ {n} R _ {n}, \left(1 - \sum_ {n = 1} ^ {N} w _ {n} ^ {*}\right) r + \sum_ {n = 1} ^ {N} w _ {n} ^ {*} R _ {n}\right)
$$

$$
= \quad C o v \left(\sum_ {n = 1} ^ {N} w _ {n} R _ {n}, \sum_ {n = 1} ^ {N} w _ {n} ^ {*} R _ {n}\right) = w ^ {T} \mathbf {C} w ^ {*}.
$$

Since the optimal weights $\begin{array} { r } { w ^ { * } = { \bf C } ^ { - 1 } ( \bar { \pmb { \mathsf { R } } } - { \pmb { r } } { \pmb { 1 } } ) \frac { \rho - r } { H } } \end{array}$ , we have

$$
C o v (R, R ^ {*}) = w ^ {T} \mathbf {C C} ^ {- 1} (\bar {\mathbf {R}} - r \mathbf {1}) \frac {\rho - r}{H} = \frac {\rho - r}{H} \cdot w ^ {T} (\bar {\mathbf {R}} - r \mathbf {1})
$$

$$
= \frac {\rho - r}{H} \cdot \sum_ {n = 1} ^ {N} w _ {n} (E [ R _ {n} ] - r) = \frac {\rho - r}{H} \cdot \left\{\sum_ {n = 1} ^ {N} w _ {n} E [ R _ {n} ] + \left(1 - \sum_ {n = 1} ^ {N} w _ {n}\right) r - r \right\}
$$

$$
= \frac {\rho - r}{H} (E [ R ] - r).
$$

Therefore,

$$
\frac {\operatorname{Cov} (R , R ^ {*})}{\operatorname{Var} (R ^ {*})} = \frac {E [ R ] - r}{E [ R ^ {*} ] - r}
$$

# In-Class Exercise: Proof of Part (ii) (try it yourself without the help of AI!)

# Linear Combination of Efficient Portfolios

With or without the risk-free asset, the optimal weight is linear in $\rho$

$$
w ^ {*} = w ^ {*} (\rho) = c + \rho b,
$$

for some vectors c and b.

Lemma 1. Let $w ^ { * } ( \rho _ { 1 } )$ and $w ^ { * } ( \rho _ { 2 } )$ be the optimal MV portfolio weights for $\rho _ { 1 } \geq r$ and $\rho _ { 2 } \geq r .$ . Then for any $\rho \geq r$ , the optimal MV weight for $\rho$ is

$$
w ^ {*} (\rho) = \alpha w ^ {*} (\rho_ {1}) + (1 - \alpha) w ^ {*} (\rho_ {2}), \tag {1}
$$

where α solves

$$
\rho = \alpha \rho_ {1} + (1 - \alpha) \rho_ {2}. \tag {2}
$$

Conversely, for any $\alpha > 0$ satisfying $\alpha \rho _ { 1 } + ( 1 - \alpha ) \rho _ { 2 } \geq r $ , the portfolio weights in (1) lead to an optimal MV portfolio with $\rho$ in (2).

If we have a collection of MV portfolios $w ^ { * } ( \rho _ { i } ) , i = 1 , . . . , M$ , then the linear combination $\sum _ { i = 1 } ^ { I } \alpha _ { i } w ^ { \ast } ( \rho _ { i } )$ is again MV efficient portfolio’s weights, as long as

$$
\sum_ {i = 1} \alpha_ {i} \rho_ {i} \geq r.
$$

Setup. Suppose we already solved the mean–variance (MV) problem and obtained two efficient portfolios:

Target return $\rho _ { 1 } = 8 \%$ gives

$$
w^{*}(\rho_{1}) = \left[ \begin{array}{c}0.70\\ 0.30 \end{array} \right]\quad (70\% \text{in Asset 1,} 30\% \text{in Asset 2}).
$$

Target return $\rho _ { 2 } = 1 2 \%$ gives

$$
w ^ {*} (\rho_ {2}) = \left[ \begin{array}{c} 0. 2 0 \\ 0. 8 0 \end{array} \right] \quad (20 \% \text { in Asset 1 }, 80 \% \text { in Asset 2 }).
$$

Goal. We want a target return $\rho = 1 0 \%$ .

# Tasks.

1 Solve for α   
2 Compute the final asset weights

The market setting:

- there are I investors in total   
- the total value of the risky asset n: $W _ { n } , \ n = 1 , . . . , N$   
- the total value of the risk-free asset: $W _ { 0 }$

Hence, the weight of the nth asset:

$$
w _ {n} ^ {(M)} = \frac {W _ {n}}{\sum_ {j = 1} ^ {N} W _ {j} + W _ {0}}
$$

# Definitions:

A total market portfolio is a portfolio with weights $w _ { n } ^ { ( M ) } , \ : n = 0 , 1 , . . . , N .$   
A market portfolio is the risky part of the total market portfolio, i.e. with weights

$$
\frac {w _ {n} ^ {(M)}}{\sum_ {j = 1} ^ {N} w _ {j} ^ {(M)}}, \quad n = 1, 2,..., N.
$$

Lemma 2. If demand equals supply, then the weights $w _ { n } ^ { ( M ) }$ (M) is a linear combination of investors’ individual weights. More precisely,

$$
w _ {n} ^ {(M)} = \sum_ {i = 1} ^ {I} \alpha_ {i} w _ {n} ^ {(i)}, n = 0, 1, 2,, N,
$$

where $w _ { n } ^ { ( i ) }$ is the weight of the nth risky asset in the i th investor’s portfolio, and $\alpha _ { i }$ is the market share held by the i th investor,

$$
\alpha_ {i} = \frac {V ^ {(i)} (0)}{\sum_ {n = 1} ^ {N} W _ {n} + W _ {0}},
$$

with $V ^ { ( i ) } ( 0 )$ being the initial wealth of the i th investor.

# In-Class Exercise: Proof of Lemma 2 (try it yourself without the help of AI!)

Assumption: $V ^ { ( i ) } ( 0 ) > 0 , i = 1 , . . . , I ; W _ { n } > 0 , n = 1 , . . . , N ; W _ { 0 } > 0 .$   
Under the assumption, $0 \leq \alpha _ { i } \leq 1$ . Hence, if $\rho _ { i } \geq r$ , then

$$
\sum_ {i = 1} ^ {I} \alpha_ {i} \rho_ {i} \geq r.
$$

Theorem (CAPM for the Market Portfolio). Assume each investor holds an MV efficient portfolio, then the total market portfolio must be MV efficient.

Consequently, for any portfolio return R, we must have

$$
E [ R ] - r = \frac {C o v (R , R _ {M})}{V a r (R _ {M})} (E [ R _ {M} ] - r), \quad \frac {E [ R ] - r}{\sigma (R)} = \rho (R, R _ {M}) \cdot \frac {E [ R _ {M} ] - r}{\sigma (R _ {M})},
$$

where $R _ { M }$ is the market portfolio’s return (without the risk-free asset).

# . Corollary

(i) The market portfolio always has the best Sharpe ratio and is MV efficient.   
(ii) Any MV efficient portfolio can be obtained by investing in only two assets: the market portfolio and the risk-free asset.

# Implications

- If every investor uses an MV efficient portfolio, then the total market also behaves as if it maximized a quadratic utility function.   
- The critical step is that the total market portfolio is MV efficient.   
- In practice, the return of various stock indices, such as the S&P 500 index, is typically used as a proxy of the market portfolio.   
- The coefficient $\begin{array} { r } { \frac { C o v ( R , R _ { M } ) } { V a r ( R _ { M } ) } = : \beta } \end{array}$ Var (RM ) is called the beta of the portfolio.

\* The yahoo finance reports the beta for all stocks based on monthly returns data within the last 3 years (by choosing r = 0)

\- Treynor ratio: reward per unit of systematic risk

$$
\frac {\mu - r}{\beta}
$$

If the CAPM holds, then

$$
E [ R ] - r = \frac {C o v (R , R _ {M})}{V a r (R _ {M})} (E [ R _ {M} ] - r),
$$

where $R _ { M }$ is the market portfolio (e.g., the ${ \mathsf S } \& { { \mathsf P } }$ 500).

The CAPM has at least two implications.

(i) For any asset, $E [ R ] - r = \alpha + \beta ( E [ R _ { M } ] - r )$ , or

$$
R - r = \alpha + \beta (R _ {M} - r) + \varepsilon , E [ \varepsilon ] = 0.
$$

(ii) Furthermore, $\alpha = 0$

If either fails empirically, then CAPM would be statistically rejected.   
Alpha strategy: Many hedge funds attempt to invent trading strategies that generate a positive α.

# The Efficient Market Hypothesis (EMH)

The EMH states that market prices reflect available information (fully or to some degree).   
Statistical interpretation: Market efficiency implies stock prices follow a random walk.   
Price changes are random and independent of past price history.   
Only new information moves stock prices.   
Since new information arrives randomly, price changes are also random.

# Three forms of EMH

Weak form: Current price reflects historical public trading data, such as past prices and trading volume.   
Semi-strong form: Current price reflects all public information about a   
Strong form: Current prices reflect all available information, including information that is not public.

# Implications of EMH: Can we beat the market?

。 According to EMH, trading strategies based on current information should not be profitable (in expectation).

# Examples of trading strategies and EMH violations

Technical analysis: Using stock price patterns (past trading data) to predict future returns.

If investors can generate abnormal returns using technical analysis, the weak-form EMH is violated.

2 Fundamental analysis: Using publicly available data (e.g., income statements, balance sheets, cash flow statements) to analyze firm fundamentals.

If investors can generate abnormal returns using fundamental analysis, the semi-strong form EMH is violated.

Insider trading: Using non-public information to gain an informational advantage.

If investors can generate abnormal returns using inside information, the strong-form EMH is violated.