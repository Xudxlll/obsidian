# Preliminaries

Min Dai

https://sites.google.com/view/mindai

The Hong Kong Polytechnic University

# Contents

1 Cox-Ross-Rubinstein Binomial Model 2

1.1 Single-period model . . 2   
1.2 Multi-period model 3

2 From the Binomial Model to the Black-Sholes Model 4   
3 Continuous-time Black-Scholes Model 5

3.1 Brownian Motion, Ito Integral, and Ito’s Lemma . 5   
3.2 Black-Scholes Model 8   
3.3 Risk-neutral pricing and theoretical basis of Monte Carlo simulation . . 9   
3.4 Continuous Dividend Payment . . 11

# 1 Cox-Ross-Rubinstein Binomial Model

# 1.1 Single-period model

Consider an option with a current value denoted by $V _ { 0 }$ at time $t = 0$ , which depends on the underlying stock price $S _ { 0 }$ . Let the expiration date of the option be T. Assume that during the life of the option, the stock price $S _ { 0 }$ can either move up to $S _ { 0 } u$ with probability $p ^ { \prime } .$ , or move down to $S _ { 0 } d$ with probability $1 - p ^ { \prime }$ . The no arbitrage condition requires that $u > e ^ { r T } > d$ and $0 < p ^ { \prime } < 1$ . Correspondingly, the payoff from the option will be either $V _ { u }$ (for an upward movement in the stock price) or $V _ { d }$ (for a downward movement).

∆−hedging analysis. We construct a portfolio consisting of a long position in the option and a short position in $\Delta$ shares. At time $t = 0$ , the portfolio has a value of

$$
V - \Delta S _ {0}.
$$

If there is an upward movement in the stock price, the value of the portfolio at $t = T$ is

$$
V _ {u} - \Delta S _ {0} u.
$$

If there is a downward movement in the stock price, the value becomes

$$
V _ {d} - \Delta S _ {0} d.
$$

To make the portfolio risk-free, we set these two values equal:

$$
V _ {u} - \Delta S _ {0} u = V _ {d} - \Delta S _ {0} d,
$$

which gives

$$
\Delta = \frac {V _ {u} - V _ {d}}{S _ {0} (u - d)}. \tag {1}
$$

According to the no-arbitrage principle, a risk-free portfolio must earn the risk-free interest rate. Therefore,

$$
V _ {u} - \Delta S _ {0} u = e ^ {r T} (V - \Delta S).
$$

Substituting equation (1) into the above formula, we obtain

$$
V = e ^ {- r T} \left[ p V _ {u} + (1 - p) V _ {d} \right],
$$

where

$$
p = \frac {e ^ {r T} - d}{u - d}.
$$

This is the single-period binomial model. Here, p is called the risk-neutral probability. Note that the objective probability $p ^ { \prime }$ does not appear in the binomial model. This is known as the risk-neutral pricing principle.

An alternative derivative approach: option replication. Given the initial option premium V, we invest $\Delta S _ { 0 }$ in stock and the remainder $V - \Delta S _ { 0 }$ in a bank account at $t = 0$ . At maturity $t = T$ ,

$$
\Delta S _ {0} u + e ^ {r T} \left(V - \Delta S _ {0}\right) \mathrm{foranupmovement};
$$

$$
\Delta S _ {0} d + e ^ {r T} \left(V - \Delta S _ {0}\right) \text { for   a   down   movement. }
$$

The fair value V is such that the option’s payoff can be exactly replicated:

$$
\Delta S _ {0} u + e ^ {r T} (V - \Delta S _ {0}) = V _ {u},
$$

$$
\Delta S _ {0} d + e ^ {r T} (V - \Delta S _ {0}) = V _ {d}.
$$

Solving these equations leads to the desired result.

# 1.2 Multi-period model

Let T be the expiration date, and [0, T ] be the lifetime of the option. If N is the number of discrete time points, we have time points $n \Delta t .$ , where $n = 0 , 1 , . . . , N .$ , with $\begin{array} { r } { \Delta t { } = \frac { T } { N } } \end{array}$ . At time $t = 0$ , the underlying stock price is known and denoted by $S _ { 0 }$ . At time $\Delta t .$ , there are two possible stock prices: $S _ { 0 } u$ and $S _ { 0 } d .$ . Without loss of generality, we assume

$$
u d = 1.
$$

At time $2 \Delta t$ , there are three possible stock prices, $S _ { 0 } u ^ { 2 } , S _ { 0 }$ , and $S _ { 0 } d ^ { 2 } = S _ { 0 } u ^ { - 2 }$ ; and so on. In general, at time $n \Delta t , n + 1$ stock prices are involved: $S _ { 0 } u ^ { - n } , S _ { 0 } u ^ { - n + 2 } , . . . , S _ { 0 } u ^ { n }$ . A complete tree is then constructed. Let $V _ { j } ^ { n }$ be the option price at time point $n \Delta t$ with stock price $\begin{array} { r } { S _ { j } = S _ { 0 } u ^ { j } } \end{array}$ . Note that $S _ { j }$ will jump either up to $S _ { j + 1 }$ or down to $S _ { j }$ −1 at time $( n + 1 ) \Delta t$ , and the value of the option at $( n + 1 ) \Delta t$ will become either $V _ { j + 1 } ^ { n + 1 }$ or $V _ { j - 1 } ^ { n + 1 }$ . Since the length of the time period is $\Delta t ,$ the discounting factor is $e ^ { - r \Delta t }$ . Then, similar to the arguments in the

single-period case, we have

$$
V _ {j} ^ {n} = e ^ {- r \Delta t} \left[ p V _ {j + 1} ^ {n + 1} + (1 - p) V _ {j - 1} \right] \tag {2}
$$

for $j = - n , - n + 2 , . . . , n$ and $n = 0 , 1 , . . . , N - 1$ , where

$$
p = \frac {e ^ {r \Delta t} - d}{u - d}.
$$

At expiry, the terminal condition is $V _ { j } ^ { N } = \operatorname* { m a x } ( \varphi _ { j } , 0 ) = : \varphi _ { j } ^ { + }$ for $j = - N , - N + 2 , . . . , N$ , where

$$
\varphi_ {j} = \left\{ \begin{array}{l l} (S _ {0} u ^ {j} - K) ^ {+} \text {for a call}, \\ (K - S _ {0} u ^ {j}) ^ {+} \text {for a put}, \end{array} \right.
$$

This is the multi-period binomial model for European options.

Suppose that the stock volatility is σ. Then we can choose

$$
u = e ^ {\sigma \sqrt {\Delta t}}, d = e ^ {- \sigma \sqrt {\Delta t}}.
$$

# 2 From the Binomial Model to the Black-Sholes Model

The binomial scheme (2) for European options can be rewritten as

$$
V (S, t - \Delta t) = e ^ {- r \Delta t} [ p V (S u, t) + (1 - p) V (S d, t) ].
$$

Here, for convenience, we take the current time to be $t - \Delta t .$ . Assuming sufficient smoothness of $V ( S , t )$ , we perform the Taylor series expansion of the binomial scheme at $( S , t )$ as follows:

$$
\begin{array}{l} 0 = - V (S, t - \Delta t) + e ^ {- r \Delta t} [ p V (S u, t) + (1 - p) V (S d, t) ] \\ = - V (S, t) + \frac {\partial V (S , t)}{\partial t} \Delta t + O (\Delta t ^ {2}) \\ + e ^ {- r \Delta t} V (S, t) + \frac {\partial V (S , t)}{\partial S} S e ^ {- r \Delta t} [ p (u - 1) + (1 - p) (d - 1) ] \\ + \frac {1}{2} \frac {\partial^ {2} V (S , t)}{\partial S ^ {2}} S ^ {2} e ^ {- r \Delta t} [ p (u - 1) ^ {2} + (1 - p) (d - 1) ^ {2} ] \\ + \frac {1}{6} \frac {\partial^ {3} V (S , t)}{\partial S ^ {3}} S ^ {3} e ^ {- r \Delta t} [ p (u - 1) ^ {3} + (1 - p) (d - 1) ^ {3} ] + O (\Delta t ^ {2}). \\ \end{array}
$$

Observe that

$$
e ^ {- r \Delta t} [ p (u - 1) + (1 - p) (d - 1) ] = r \Delta t + O (\Delta t ^ {2}),
$$

$$
e ^ {- r \Delta t} [ p (u - 1) ^ {2} + (1 - p) (d - 1) ^ {2} ] = \sigma^ {2} \Delta t + O (\Delta t ^ {2}),
$$

$$
e ^ {- r \Delta t} [ p (u - 1) ^ {3} + (1 - p) (d - 1) ^ {3} ] = O (\Delta t ^ {2}).
$$

We then get

$$
\begin{array}{l} 0 = - V (S, t - \Delta t) + e ^ {- r \Delta t} [ p V (S u, t) + (1 - p) V (S d, t) ] \\ = [ - r V (S, t) + \frac {\partial V (S , t)}{\partial t} + r S \frac {\partial V (S , t)}{\partial S} + \frac {1}{2} \sigma^ {2} S ^ {2} \frac {\partial^ {2} V (S , t)}{\partial S ^ {2}} ] \Delta t + O (\Delta t ^ {2}), \\ \end{array}
$$

namely,

$$
- r V (S, t) + \frac {\partial V (S , t)}{\partial t} + r S \frac {\partial V (S , t)}{\partial S} + \frac {1}{2} \sigma^ {2} S ^ {2} \frac {\partial^ {2} V (S , t)}{\partial S ^ {2}} = O (\Delta t).
$$

Sending $\Delta t$ to zero leads to the Black-Scholes equation:

$$
\frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} S ^ {2} \frac {\partial^ {2} V}{\partial S ^ {2}} + r S \frac {\partial V}{\partial S} - r V = 0.
$$

# 3 Continuous-time Black-Scholes Model

# 3.1 Brownian Motion, Ito Integral, and Ito’s Lemma

Brownian motion. A process $W _ { t }$ is a Brownian motion if $W _ { t }$ is continuous and:

(i) The change $\Delta W$ during any period of time $[ t , t + \Delta t ]$ is a random variable drawn from a normal distribution with zero mean and variance $\Delta t ,$ i.e.,

$$
\Delta W = \phi \sqrt {\Delta t}.
$$

where $\phi$ is a random variable drawn from a standard normal distribution, which has zero mean, unit variance and a density function given by

$$
\frac {1}{\sqrt {2 \pi}} e ^ {- \frac {x ^ {2}}{2}}, x \in (- \infty , \infty).
$$

(ii) The values of $\Delta W$ for any two non-overlapping intervals are independent.

Ito process and Ito integral. In most cases, we assume that the underlying stock price follows an Ito process,

$$
d S _ {t} = a _ {t} d t + b _ {t} d W _ {t}, \tag {3}
$$

where $W _ { t }$ is a standard Brownian motion, and $a _ { t }$ and $b _ { t }$ are adapted with respect to the filtration generated by $W _ { t }$ .

A precise expression of the stock price process is

$$
S _ {t} = S _ {0} + \int_ {0} ^ {t} a _ {\tau} d \tau + \int_ {0} ^ {t} b _ {\tau} d W _ {\tau},
$$

where the first integral is the Riemann or Lebesgue integral, and the second is the Ito integral.

For a rigorous definition of the Ito integral, see Oksendal (2003). Here, we only provide an intuitive interpretation. For any partition $0 = t _ { 1 } < t _ { 2 } < . . . < t _ { n } = t .$ the integral $\int _ { 0 } ^ { t } f _ { \tau } d W _ { \tau }$ is the limit of

$$
\sum_ {i = 0} ^ {n - 1} f _ {t _ {i}} \left(W _ {t _ {i + 1}} - W _ {t _ {i}}\right)
$$

as max $( { { t } _ { i + 1 } } - { { t } _ { i } } ) \mathrm { ~  ~ 0 ~ }$ (f is adapted with respect to the filtration generated by $W _ { t } )$ . We emphasize that f is evaluated at the left-hand side point of the interval $( t _ { i } , t _ { i + 1 } )$ . In contrast, the Riemann integral $\textstyle \int _ { 0 } ^ { t } f \left( \tau \right)$ dτ is defined as the limit of

$$
\sum_ {i = 0} ^ {n - 1} f (\xi_ {i}) (t _ {i + 1} - t _ {i}),
$$

as max $( t _ { i + 1 } - t _ { i } )  \ 0$ , where $\xi _ { i } \in [ t _ { i } , t _ { i + 1 } ]$ . Next, we show that the definition of the Ito integral aligns with investment decisions.

A self-financing weath process. Consider a self-financing procedure, which means that there is no withdrawal or infusion of funds during the investment period. Let $Z _ { t }$ be the value of a self-financing wealth process at time t. Consider an investment strategy for which transactions take place at discrete times $t _ { i } , i = 0 , . . . , t _ { n - 1 }$ . Assume that at time $t _ { i }$ , based on all information up to time $t _ { i \cdot }$ , the investor decides to hold $\Delta _ { t _ { i } }$ number of shares, and the remainder $Z _ { t _ { i } } - \Delta _ { t _ { i } } S _ { t _ { i } }$ in a bank account. During $( t _ { i } , t _ { i + 1 } )$ , the number of shares remains fixed. Then the profit/loss during $[ t _ { i } , t _ { i + 1 } ]$ is $r ( Z _ { t _ { i } } - \Delta _ { t _ { i } } S _ { t _ { i } } ) ( t _ { i + 1 } - t _ { i } ) + \Delta _ { t _ { i } } ( S _ { t _ { i + 1 } } - S _ { t _ { i } } )$ . The accumulative profit or loss during [0, t], $Z _ { t } - Z _ { 0 }$ , equals

$$
\begin{array}{l} \sum_ {i = 0} ^ {n - 1} \Big (r (Z _ {t _ {i}} - \Delta_ {t _ {i}} S _ {t _ {i}}) (t _ {i + 1} - t _ {i}) + \Delta_ {t _ {i}} (S _ {t _ {i + 1}} - S _ {t _ {i}}) \Big) \\ = \sum_ {i = 0} ^ {n - 1} \left(r (Z _ {t _ {i}} - \Delta_ {t _ {i}} S _ {t _ {i}}) (t _ {i + 1} - t _ {i}) + \Delta_ {t _ {i}} a _ {t _ {i}} (t _ {i + 1} - t _ {i}) + \Delta_ {t _ {i}} b _ {t _ {i}} (W _ {t _ {i + 1}} - W _ {t _ {i}})\right) \\ = \sum_ {i = 0} ^ {n - 1} \left(\left[ r (Z _ {t _ {i}} - \Delta_ {t _ {i}} S _ {t _ {i}}) + \Delta_ {t _ {i}} a _ {t _ {i}} \right] (t _ {i + 1} - t _ {i}) + \Delta_ {t _ {i}} b _ {t _ {i}} (W _ {t _ {i + 1}} - W _ {t _ {i}})\right) \\ \end{array}
$$

Sending max $( t _ { i + 1 } - t _ { i } )  0$ , we obtain i

$$
Z _ {t} - Z _ {0} = \int_ {0} ^ {t} [ r (Z _ {\tau} - \Delta_ {\tau} S _ {\tau}) + \Delta_ {\tau} a _ {\tau} ] d \tau + \int_ {0} ^ {t} \Delta_ {\tau} b _ {\tau} d W _ {\tau}. (4)
$$

Ito’s lemma. Ito’s Lemma is essentially the differential chain rule of a function involving random variables. First let us recall the standard differential chain rule of a function of deterministic variables. Let $V ( . , . )$ be a deterministic function of two state variables. Consider $V ( S _ { t } , t )$ , where

$$
d S _ {t} = a _ {t} d t.
$$

Then,

$$
\begin{array}{l} d V (S _ {t}, t) = \frac {\partial V (S _ {t} , t)}{\partial t} d t + \frac {\partial V (S _ {t} , t)}{\partial S} d S _ {t} = \frac {\partial V (S _ {t} , t)}{\partial t} d t + \frac {\partial V (S _ {t} , t)}{\partial S} a _ {t} d t \\ = \left[ \frac {\partial V (S _ {t} , t)}{\partial t} + a _ {t} \frac {\partial V (S _ {t} , t)}{\partial S} \right] d t. \\ \end{array}
$$

Now let us return to the stochastic process (3). Keep in mind that $d W _ { t } = \phi { \sqrt { d t } }$ and $( d W _ { t } ) ^ { 2 } = d t$ . So, formally we have

$$
{(d S _ {t}) ^ {2}} = {(a _ {t} d t + b _ {t} d W _ {t}) ^ {2} = a _ {t} ^ {2} d t ^ {2} + 2 a _ {t} b _ {t} d t d W _ {t} + b _ {t} ^ {2} (d W _ {t}) ^ {2} = b _ {t} ^ {2} d t + \dots .}
$$

As a result, when applying the Taylor series expansion to $V ( S _ { t } , t )$ , we need to retain the

second order term of dS. Thus,

$$
d V (S _ {t}, t) = \frac {\partial V (S _ {t} , t)}{\partial t} d t + \frac {\partial V (S _ {t} , t)}{\partial S} d S _ {t} + \frac {1}{2} \frac {\partial^ {2} V (S _ {t} , t)}{\partial S ^ {2}} (d S _ {t}) ^ {2}
$$

$$
{ = } { \frac { \partial V ( S _ { t } , t ) } { \partial t } d t + \frac { \partial V ( S _ { t } , t ) } { \partial S } d S _ { t } + \frac { 1 } { 2 } \frac { \partial ^ { 2 } V ( S _ { t } , t ) } { \partial S ^ { 2 } } b _ { t } ^ { 2 } d t }
$$

$$
{ = } { \left[ \frac { \partial V ( S _ { t } , t ) } { \partial t } + \frac { 1 } { 2 } b _ { t } ^ { 2 } \frac { \partial ^ { 2 } V ( S _ { t } , t ) } { \partial S ^ { 2 } } \right] d t + \frac { \partial V ( S _ { t } , t ) } { \partial S } d S _ { t } }
$$

$$
{ = } { \left[ \frac { \partial V ( S _ { t } , t ) } { \partial t } + a _ { t } \frac { \partial V ( S _ { t } , t ) } { \partial S } + \frac { 1 } { 2 } b _ { t } ^ { 2 } \frac { \partial ^ { 2 } V ( S _ { t } , t ) } { \partial S ^ { 2 } } \right] d t + b _ { t } \frac { \partial V ( S _ { t } , t ) } { \partial S } d W . }
$$

This is the Ito formula, the chain rule of stochastic calculus.

# 3.2 Black-Scholes Model

Consider a market where only two basic assets are traded. One is a bond (money-market account), whose price process is given by

$$
d P _ {t} = r P _ {t} d t,
$$

where $r$ is the risk-free rate. The other asset is a stock whose price process is governed by geometric Brownian motion:

$$
d S _ {t} = \mu S _ {t} d t + \sigma S _ {t} d W _ {t},
$$

where $\mu$ and $\sigma$ are the expected return rate and volatility of the underlying stock, and $W _ { t }$ is the Brownian motion. Assume that the risk-free rate r and the stock volatility σ are known constants over the life of the option.

While one can derive the Black-Scholes model using ∆-hedging, we instead adopt an option replication argument.

Continuous-time option replication. Without loss of generality, we focus on a European call option whose payoff is

$$
V _ {T} = (S _ {T} - K) ^ {+}.
$$

Our target is to replcate the option through a self-financing wealth process. According to equation (4), a self-financing wealth process $Z _ { t }$ is described by

$$
d Z _ {t} = \left[ r Z _ {t} + (\mu - r) \Delta_ {t} S _ {t} \right] d t + \sigma \Delta_ {t} S _ {t} d W _ {t}, \tag {5}
$$

where $\Delta _ { t }$ is the number of shares held at time t.

Consider the replication problem from the perspective of the option’s writer who sells the option at the price $V _ { 0 }$ at time $t = 0$ and attempts to replicate the option’s payoff $V _ { T }$ at expiry by selecting an appropriate strategy $\Delta _ { t }$ . More generally, suppose the option value $V = V ( S _ { t } , t )$ . We aim to have $Z _ { t } = V ( S _ { t } , t )$ for all $t \in [ 0 , T ]$ .

Applying Ito lemma,

$$
d V _ {t} = \left(\frac {\partial V (S _ {t} , t)}{\partial t} + \frac {1}{2} \sigma^ {2} S _ {t} ^ {2} \frac {\partial^ {2} V (S _ {t} , t)}{\partial S ^ {2}} + \mu S _ {t} \frac {\partial V (S _ {t} , t)}{\partial S}\right) d t + \sigma S _ {t} \frac {\partial V (S _ {t} , t)}{\partial S} d W _ {t}. \tag {6}
$$

Comparing this with the self-financing process given in (5), we get

$$
\Delta_ {t} = \frac {\partial V (S _ {t} , t)}{\partial S}
$$

and

$$
\frac {\partial V (S _ {t} , t)}{\partial t} + \frac {1}{2} \sigma^ {2} S _ {t} ^ {2} \frac {\partial^ {2} V (S _ {t} , t)}{\partial S ^ {2}} + \mu S _ {t} \frac {\partial V (S _ {t} , t)}{\partial S} = r V (S _ {t}, t) + (\mu - r) \Delta_ {t} S _ {t}.
$$

In the end, we derive the Black-Scholes equation:

$$
\frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} S ^ {2} \frac {\partial^ {2} V}{\partial S ^ {2}} + r S \frac {\partial V}{\partial S} - r V = 0 \tag {7}
$$

in $S > 0$ and $t \in [ 0 , T )$ . At maturity,

$$
V (S, T) = (S - K) ^ {+} \tag {8}
$$

The above derivation indicates the replication procedure is as follows:

• Solve the Black-Scholes equation (7) with the boundary condition (8) to obtain $V ( S , t )$ .   
• At time 0, sell the option at the price $V ( S _ { 0 } , 0 )$ .   
• At any time $t \in [ 0 , T )$ , hold $\begin{array} { r } { \Delta _ { t } = \frac { \partial V ( S _ { t } , t ) } { \partial S } } \end{array}$ shares of stock. ∂S

# 3.3 Risk-neutral pricing and theoretical basis of Monte Carlo simulation

The expected return rate $\mu$ of the underlying stock, which clearly depends on risk preference, does not appear in the Black-Scholes equation. All variables and parameters in the equation are independent of risk preference. Therefore, risk preferences do not affect the solution to the Black-Scholes equation.

In a risk-neutral world, all investors are risk-neutral, meaning the expected return on all securities equals the risk-free interest rate r. Thus, the present value of any cash flow in this world can be obtained by discounting its expected value at the risk-free rate. Specifically, the price of an option (a European call, for example) can be represented by

$$
V (S, t) = \widehat {\mathbb {E}} _ {t} \left[ e ^ {- r (T - t)} (S _ {T} - X) ^ {+} | S _ {t} = S \right]. \tag {9}
$$

Here, $\widehat { \mathbb { E } } _ { t }$ denotes the conditional expectation in a risk-neutral world under which the underlying stock price $S _ { t }$ follows

$$
\frac {d S _ {t}}{S _ {t}} = r d t + \sigma d W _ {t}. \tag {10}
$$

Note that in this situation, the expected return rate of the underlying stock is the risk-free rate of interest rr (assuming the underlying pays no dividends).

The equivalence between (7)-(8) and (9) follows from the Feynman-Kac formula; see Oksendal (2003).

Equation (9) forms the theoretical basis of Monte Carlo simulation for derivative pricing. The simulation can be carried out by the following procedure:

(i) Simulate the price movement of the underlying stock in a risk-neutral world according to (10);   
(ii) Calculate the expected terminal payoff of the derivative;   
(iii) Discount the expected payoff at the risk-free interest rate.

Applications to path-dependent options. It is worth highlighting that risk-neutral pricing applies to path-dependent options, such as Asian options and barrier options. Consider an up-out-call option whose terminal payoff can be written as

$$
(S _ {T} - X) ^ {+} \mathrm{I} _ {\{S _ {t} <   H, t \in [ 0, T ] \}},
$$

where H is the barrier level, and I is the indicator function, i.e.,

$$
\operatorname{I} _ {\{S _ {t} <   H, t \in [ 0, T ] \}} = \left\{ \begin{array}{l l} 1, \text {if} S _ {t} <   H \text {for all} t \in [ 0, T ], \\ 0, \text {otherwise.} \end{array} \right.
$$

By the risk-neutral pricing principle, the option value at time zero is

$$
e ^ {- r T} \widehat {\mathbb {E}} [ (S _ {T} - X) ^ {+} \mathrm{I} _ {\{S _ {t} <   H, t \in [ 0, T ] \}} ]
$$

Similarly, consider arithmetic Asian options, whose payoff is a function of the terminal stock price and the average $A _ { T }$ , based on either discretely or continuously sampled prices:

$$
A _ {T} = \left\{ \begin{array}{l l} \frac {1}{n} \sum_ {i = 1} ^ {n} S _ {t _ {i}}, \mathrm{discretelysampledarithmeticaverage} \\ \frac {1}{T} \int_ {0} ^ {T} S _ {\tau} d \tau , \mathrm{continuouslysampledarithmeticaverage} \end{array} \right.
$$

By the risk-neutral pricing principle, the option value at time zero is

$$
e ^ {- r T} \widehat {\mathbb {E}} [ f (S _ {T}, A _ {T}) ].
$$

Monte Carlo simulation can then be used to obtain approximate values of these options. Once the option prices are determined, the corresponding hedging strategies can be obtained.

# 3.4 Continuous Dividend Payment

Let q be the continuous dividend yield. This means that over a time interval $d t$ , the underlying stock pays a dividend of $q S _ { t } d t$ .

In the binomial model, the risk-neutral probability is adjusted as

$$
p = \frac {e ^ {(r - q) \Delta t} - d}{u - d}.
$$

In the continuous-time model, the corresponding Black-Scholes equation becomes

$$
\frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} S ^ {2} \frac {\partial^ {2} V}{\partial S ^ {2}} + (r - q) S \frac {\partial V}{\partial S} - r V = 0.
$$

The price of a European call option can be represented by

$$
V (S, t) = \widehat {\mathbb {E}} _ {t} \left[ e ^ {- r (T - t)} (S _ {T} - X) ^ {+} | S _ {t} = S \right],
$$

where $\widehat { \mathbb { E } } _ { t }$ denotes the conditional expectation in the risk-neutral world under which the underlying stock price $S _ { t }$ follows

$$
\frac {d S _ {t}}{S _ {t}} = (r - q) d t + \sigma d W _ {t}.
$$