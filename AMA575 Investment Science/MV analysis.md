# AMA575 Advanced Topics in Investment Science Lecture 1: Mean Variance Analysis

Lecturer: Selena QIAN

Hong Kong Polytechnic University

January 14, 2026

# Course Assessment & Grading Policy

# Assessment Components

Assignments: 2 assignments during the semester   
Midterm Exam: 1 midterm exam in Week 7   
Final Exam: 1 comprehensive final exam (covers all chapters in the semester)

Weighting 

<table><tr><td>Homework Assignments</td><td>20%</td></tr><tr><td>Midterm Exam</td><td>20%</td></tr><tr><td>Final Exam</td><td>60%</td></tr></table>

Rubric Grade Cut-off

<table><tr><td>Grade Band</td><td>Cut-off</td></tr><tr><td>A+, A, A-</td><td> $\geq 85$ </td></tr><tr><td>B+, B, B-</td><td> $\geq 65$ </td></tr><tr><td>C+, C, C-</td><td> $\geq 50$ </td></tr><tr><td>D+, D</td><td> $\geq 40$ </td></tr></table>

One period economy: $t = 0 , 1$

\- a riskfree bond with constant risk-free return $r > 0$ , i.e.,

\$1 at time 0 becomes \$1 + r at time 1

\- N risky assets

Let $S _ { n } ( t )$ be the price of the nth risky asset price at time t = 0, 1

\- Return of the nth risky asset: $R _ { n } = ( S _ { n } ( 1 ) - S _ { n } ( 0 ) ) / S _ { n } ( 0 )$

A portfolio or trading strategy: $\phi = ( \phi _ { 0 } , \phi _ { 1 } , . . . , \phi _ { N } )$

\- $\phi _ { 0 }$ : the number of shares invested in the bond (with initial price \$1).

\- $\phi _ { n }$ : the number of shares invested in the nth risky asset

Let V (t) be the value of the portfolio at time t = 0, 1.

$$
\begin{array}{l} R = \frac {V (1) - V (0)}{V (0)} = \frac {\phi_ {0} r + \sum_ {n = 1} ^ {N} \phi_ {n} \left(S _ {n} (1) - S _ {n} (0)\right)}{V (0)} \\ = \frac {\phi_ {0} r + \sum_ {n = 1} ^ {N} \phi_ {n} S _ {n} (0) (\frac {S _ {n} (1)}{S _ {n} (0)} - 1)}{V (0)} \\ = \frac {(V (0) - \sum_ {n = 1} ^ {N} \phi_ {n} S _ {n} (0)) r + V (0) \sum_ {n = 1} ^ {N} w _ {n} (\frac {S _ {n} (1)}{S _ {n} (0)} - 1)}{V (0)} \\ = (1 - \sum_ {n = 1} ^ {N} w _ {n}) r + \sum_ {n = 1} ^ {N} w _ {n} R _ {n}. \\ \end{array}
$$

where $\begin{array} { r } { w _ { n } = \frac { \phi _ { n } S _ { n } ( 0 ) } { V ( 0 ) } } \end{array}$ is the fraction of total wealth in asset n.

Return (random) and Risk (variance Var[R])   
An investor attempts to solve the following problem:

$$
\begin{array}{l l} & \underset {w} {\min} \operatorname{Var} [ R ] \\ \text { subject   to } & E [ R ] = \rho , \rho \geq r. \end{array}
$$

- The intuition: for the same return $\rho ,$ , the investor prefers a portfolio with a smaller variance.   
- $\rho$ reflects the investor’s risk appetite

A major drawback: ignoring other distribution properties (e.g. skewness, kurtosis, etc.)

# A counterexample (in-class exercise)

. Consider two portfolio returns $R _ { 1 }$ and $R _ { 2 }$ :

$$
R _ {1} = X _ {1}, \qquad R _ {2} = B X _ {2} + (1 - B) X _ {3},
$$

where B is a Bernoulli random variable with $p = \mathbb { P } ( B = 1 ) = 0 . 9 9$ .

Assume $X _ { 1 } , X _ { 2 } , X _ { 3 }$ , and B are independent, and

$$
X _ {1} \sim N (\mu_ {1}, \sigma_ {1} ^ {2}), X _ {2} \sim N (\mu_ {2}, \sigma_ {2} ^ {2}), X _ {3} \sim N (\mu_ {3}, \sigma_ {3} ^ {2}).
$$

Given parameters:

$$
\mu_ {1} = 5 \%, \sigma_ {1} = 20 \%, \quad \mu_ {2} = 6 \%, \sigma_ {2} = 10 \%.
$$

Your task: Choose $\mu _ { 3 }$ and $\sigma _ { 3 }$ such that $R _ { 1 }$ and $R _ { 2 }$ have the same mean and variance:

$$
\mathbb {E} [ R _ {1} ] = \mathbb {E} [ R _ {2} ], \qquad \operatorname{Var} (R _ {1}) = \operatorname{Var} (R _ {2}).
$$

Use the law of total variance when solving for $\sigma _ { 3 }$ :

$$
\operatorname{Var} \left(R _ {2}\right) = \mathbb {E} \left[ \operatorname{Var} \left(R _ {2} \mid B\right) \right] + \operatorname{Var} \left(\mathbb {E} \left[ R _ {2} \mid B \right]\right)
$$

Check: After you find $\mu _ { 3 } , \sigma _ { 3 }$ , verify your answers by plugging them back into the two equalities.

Portfolio one: an average return of 5% (volatility 20%)   
Portfolio two:

- An average return of 6% (volatility 10%) during the normal time   
- An average return of −94% (volatility 142.13%) during the financial crisis that happens with probability 1%.

But from the mean-variance viewpoint, the two are the same.

- Portfolio two has a larger kurtosis.   
- In reality, which one shall you choose?

Keep selling a deep out-of-money put option on a major index, e.g., SPX or SPY

- Shorting a put option is equivalent to selling an insurance.   
- Most time you will have a stable return: option premium.   
- One day you may lose almost all money.

# Example: Repeatedly Selling a Deep OTM Put (“Selling Insurance” SPY

# Setup (one contract).

Current price: ${ \mathsf { S P Y } } \approx { \mathfrak { S 6 } } 9 4$ .   
Sell 1 deep out-of-the-money put: strike K = \$580, maturity ≈ 1 month.   
Option premium: $c = \$ 0.62$ per share.   
Contract multiplier: 100 shares per contract.

# Premium received upfront:

$$
\text { Premium } = c \times 1 0 0 = 0. 6 2 \times 1 0 0 = 6 2.
$$

Payoff / Profit at expiry. Let $S _ { T }$ be SPY price at expiry.

$$
\text { Short   put   payoff } = - 1 0 0 \max (K - S _ {T}, 0),
$$

$$
\Pi (S _ {T}) = \text { Profit } = \underbrace {1 0 0 c} _ {\text { premium }} - \underbrace {1 0 0 \max (K - S _ {T} , 0)} _ {\text { put   payoff }}.
$$

# Example continued: Repeatedly Selling a Deep OTM Put (“Selling Insurance”) — SPY

Case 1 (most of the time): $S _ { T } \geq K$ .

$$
\Pi (S _ {T}) = 1 0 0 c = \mathbb {S} 6 2.
$$

Case 2 (crash): $S _ { T } = 5 0 0$ .

$$
\Pi (5 0 0) = 1 0 0 (0. 6 2) - 1 0 0 (5 8 0 - 5 0 0) = 6 2 - 8 0 0 0 = -   \mathbb {S} 7, 9 3 8.
$$

Case 3 (extreme crash): $S _ { T } = 3 5 0$ .

$$
\Pi (3 5 0) = 6 2 - 1 0 0 (5 8 0 - 3 5 0) = 6 2 - 2 3 0 0 0 = -   \mathbb {S} 2 2, 9 3 8.
$$

Takeaway. Selling deep OTM puts often generates many small gains (collecting premiums), but a rare large drop can cause a huge loss (insurance payout), especially if using margin or selling many contracts.

WLOG, assume $\rho > r$

Find a portfolio such that its expected return $E ( R ) = \rho$   
Assumption: At least one stock’s expected return is not r , e.g.

$$
E [ R _ {n} ] \neq r
$$

. Consider a strategy putting α fractional amount of money in the bond and the rest in $S _ { n }$ .

\- To make the expected return $\alpha r + ( 1 - \alpha ) E [ R _ { n } ]$ equal to $\rho ,$ one has

$$
\alpha = \frac {E [ R _ {n} ] - \rho}{E [ R _ {n} ] - r}
$$

\- The set of admissible strategies is non-empty.

# MV analysis: a convex optimization problem

$\textsf { o } R = ( 1 - \sum _ { n = 1 } ^ { N } w _ { n } ) r + \sum _ { n = 1 } ^ { N } w _ { n } R _ { n } . \mathsf { T h e n }$ X

$$
{ V a r [ R ] } { = } { V a r [ \sum _ { n = 1 } ^ { N } w _ { n } R _ { n } ] = \sum _ { 1 \leq j , k \leq N } w _ { j } w _ { k } C o v ( R _ { j } , R _ { k } ) = w ^ { \top } \mathbf { C } w , }
$$

where

$\mathbf { \Psi } - \mathbf { \Psi } w = ( w _ { 1 } , . . . , w _ { N } ) ^ { \top } ,$   
- $\mathbf { C } = ( C _ { i j } ) _ { N \times N } \mathrm { ; }$ : the variance-covariance matrix, i.e., $C _ { i j } = C o v ( R _ { i } , R _ { j } )$

A constrained convex optimization problem:

$$
\min _ {w} \frac {1}{2} w ^ {\top} \mathbf {C} w
$$

subject to

$$
(1 - \sum_ {n = 1} ^ {N} w _ {n}) r + \sum_ {n = 1} ^ {N} w _ {n} E [ R _ {n} ] = \rho
$$

# Solution procedure: A dual problem

. Consider a dual problem using a Lagrangean,

$$
\min _ {w, \lambda} L (w, \lambda)
$$

where

$$
L (w, \lambda) = \frac {1}{2} w ^ {\top} \mathbf {C} w + \lambda \left\{\rho - (1 - \sum_ {n = 1} ^ {N} w _ {n}) r - \sum_ {n = 1} ^ {N} w _ {n} E [ R _ {n} ] \right\}
$$

$$
= \frac {1}{2} w ^ {\top} \mathbf {C} w + \lambda \left\{\rho - r - w ^ {\top} (\bar {\mathbf {R}} - r \mathbf {1}) \right\}
$$

$\mathrm { w i t h } \ \bar { \mathsf { R } } = ( E [ R _ { 1 } ] , . . . , E [ R _ { N } ] ) ^ { \top } \ \mathrm { a n d } \ \mathbf { 1 } = ( 1 , . . . , 1 ) ^ { \top }$

N equations:

$$
\mathbf {0} = \frac {\partial L}{\partial w} = \mathbf {C} w - \lambda (\bar {\mathbf {R}} - r \mathbf {1}),
$$

where $\mathbf { 0 } = ( 0 , . . . , 0 ) ^ { \top }$ and $\begin{array} { r } { \frac { \partial \cal { L } } { \partial w } = ( \frac { \partial \cal { L } } { \partial w _ { 1 } } , . . . , \frac { \partial \cal { L } } { \partial w _ { n } } ) ^ { \top } } \end{array}$ .

This yields the optimal weights

$$
w ^ {*} = \lambda \mathbf {C} ^ {- 1} (\bar {\mathbf {R}} - r \mathbf {1}).
$$

Another equation:

$$
0 = \frac {\partial L}{\partial \lambda} = \rho - r - w ^ {\top} (\bar {\mathbf {R}} - r \mathbf {1}).
$$

Plugging the optimal weights into the last equation,

$$
\rho - r = w ^ {* \top} (\bar {\mathbf {R}} - r \mathbf {1}) = \lambda (\bar {\mathbf {R}} - r \mathbf {1}) ^ {\top} \mathbf {C} ^ {- 1} (\bar {\mathbf {R}} - r \mathbf {1}) =: \lambda H,
$$

where $H > 0$ .

# Optimal weights and variance

The optimal portfolio weights

$$
w ^ {*} = \mathbf {C} ^ {- 1} (\bar {\mathbf {R}} - r \mathbf {1}) \frac {\rho - r}{H}.
$$

The resulting optimal variance

$$
\sigma_ {*} ^ {2} = w ^ {* \top} \mathbf {C} w ^ {*} = \left\{\mathbf {C} ^ {- 1} (\bar {\mathbf {R}} - r \mathbf {1}) \frac {\rho - r}{H} \right\} ^ {\top} \cdot \mathbf {C} \cdot \mathbf {C} ^ {- 1} (\bar {\mathbf {R}} - r \mathbf {1}) \frac {\rho - r}{H}
$$

$$
= \left(\bar {\mathbf {R}} - r \mathbf {1}\right) ^ {\top} \mathbf {C} ^ {- 1} (\bar {\mathbf {R}} - r \mathbf {1}) \left(\frac {\rho - r}{H}\right) ^ {2}
$$

$$
= H \left(\frac {\rho - r}{H}\right) ^ {2} = \frac {(\rho - r) ^ {2}}{H},
$$

$$
\rho = r + \sigma_ {*} \sqrt {H}.
$$

How to compute

$$
\xi =: \frac {\rho - r}{H} = \frac {\sigma_ {*} ^ {2}}{\rho - r}
$$

In theory, individual investors’ preference $( \rho )$ is involved.   
In practice, to estimate ξ, people typically use the market excess return and market variance.   
- S&P500: take the historical excess returns $\boldsymbol \rho - \boldsymbol r$ (after adjustment for inflation) has a mean of 6% and standard deviation of 16%, then

$$
\xi = \frac {0 . 1 6 ^ {2}}{0 . 0 6} = 0. 4 2 6 6 7.
$$

Consider two stocks and 3 states. Suppose $V ( 0 ) = v$ . The returns of the stocks are given in the following table.

$$
\begin{array}{c c c c} & \omega_ {1} & \omega_ {2} & \omega_ {3} \\ R _ {1} (\omega) & 0. 2 & - 0. 2 & 0. 0 5 \\ R _ {2} (\omega) & 0. 1 5 & 0 & - 0. 1 \\ P (\omega) & 1 / 3 & 1 / 3 & 1 / 3 \end{array}
$$

Now assume $r = 0 .$

(1) Compute the matrix C.   
(2) Compute H.   
(3) Compute the optimal weights w .

Compare two strategies: average annual return 20% vs 10%   
A good performance measure is the Sharpe ratio defined as

$$
\frac {\mu - r}{\sigma},
$$

where µ is the portfolio return, r is the risk-free rate, and σ is the standard deviation of the return.

The MV analysis indicates that the larger the Sharpe ratio, the better the portfolio.

Consider two trading strategies with two Sharpe ratios

$$
\lambda_ {1} = \frac {\mu_ {1} - r}{\sigma_ {1}}, \lambda_ {2} = \frac {\mu_ {2} - r}{\sigma_ {2}}, \lambda_ {1} <   \lambda_ {2}.
$$

。 Two fund managers (FMs) starting with zero money implement strategy one and two, respectively.

- FM one will borrow \$1 for investment, and her expected return is $\mu _ { 1 } - r$ , with the standard deviation of $\sigma _ { 1 }$ .   
- FM two will borrow $\$ 1$ σ2 for investment. Then the standard deviation for his return is still $\begin{array} { r } { \sigma _ { 1 } = \frac { \sigma _ { 1 } } { \sigma _ { 2 } } \sigma _ { 2 } } \end{array}$ σ1 σ . σ   
2- The expected return for FM two is

$$
\frac {\sigma_ {1}}{\sigma_ {2}} (\mu_ {2} - r) = \lambda_ {2} \sigma_ {1} > \lambda_ {1} \sigma_ {1} = \mu_ {1} - r.
$$

The Sharpe ratio of an optimal MV portfolio is given by

$$
\frac {\rho - r}{\sigma_ {*}} = \sqrt {H},
$$

where H is independent of $\rho$ and $\sigma _ { * }$ . This implies

- Any MV efficient portfolio has the same Sharpe ratio (i.e. $\sqrt { H } )$ .   
- The Sharpe ratio of any portfolio is bounded from above by $\sqrt { H }$ .

. Limitation: The investor does not care about any other statistics, such as skewness and kurtosis.

Without the risk-free asset, the new problem becomes

$$
\min _ {w} \frac {1}{2} w ^ {\top} \mathbf {C} w
$$

subject to

$$
w ^ {\top} \bar {\mathbf {R}} = \rho , w ^ {\top} \mathbf {1} = 1.
$$

Now the Lagrangian is

$$
L (w, \lambda) = \frac {1}{2} w ^ {\top} \mathbf {C} w + \lambda \left\{\rho - w ^ {\top} \bar {\mathbf {R}} \right\} + \gamma \left\{1 - w ^ {\top} \mathbf {1} \right\}.
$$