# Beyond the Black-Scholes World

Min Dai https://sites.google.com/view/mindai

The Hong Kong Polytechnic University

# Contents

1 Volatility Smile Phenomena and Defects in the Black-Scholes Model 2

1.1 Implied Volatility and Volatility Smiles . . 2   
1.2 Improved Models 3

2 Local Volatility Model and Dupire Equation 4

2.1 Local Volatility Model 4   
2.2 Dupire’s Equation (1993) . . 4   
2.3 Inverse Problem . . 6   
2.4 Pros and Cons . . 6

3 Stochastic Volatility Models 7

3.1 Random Volatility 7   
3.2 The Pricing Equation . . 7   
3.3 Named Models and Calibration 9

4 Jump-Diffusion Models 9

4.1 Jump-Diffusion Process . . 9   
4.2 Merton’s Model (1976) 10   
4.3 \*Wilmott et al.’s Model 11   
4.4 Summary 12

These lecture notes are based on Paul Wilmott’s book Paul Wilmott on Quantitative Finance.

Recommended reading: The chapter “Volatility Smile” in John Hull’s book Options, Futures, and Other Derivatives.

# 1 Volatility Smile Phenomena and Defects in the Black-Scholes Model

Before highlighting some of the flaws in the assumptions of the Black-Scholes model, it is important to emphasize its practical success, widespread use, and significant impact on financial markets. The model is employed by salespeople, traders, and quantitative analysts. The value of vanilla options is often quoted not in monetary terms but in terms of volatility, with the understanding that the price of a contract is its Black-Scholes value using the quoted volatility. The concepts of delta hedging and risk-neutral pricing have firmly captured the minds of both academics and practitioners. In many ways, especially regarding commercial success, the Black-Scholes model is remarkably robust.

Nevertheless, there is room for improvement.

# 1.1 Implied Volatility and Volatility Smiles

The only parameter in the Black-Scholes pricing formulas that cannot be directly observed is the volatility of the underlying asset price, which measures the uncertainty about the returns provided by the underlying asset. Typically, the volatility values of an underlying asset range from 10% to 40% per annum.

Volatility can be estimated from the historical prices of the underlying asset. However, it is more appropriate to mention an alternative approach involving what is termed implied volatility. This is the volatility implied by an option price observed in the market.

To illustrate the basic idea, suppose the market price of a call option on a non-dividendpaying underlying asset is \$1.875 when S0 = 21, X = 20, r = 0.1, and $T = 0 . 2 5$ . The implied volatility is the value of σ which, when substituted into the Black-Scholes formula, results in the observed market price of the option:

$$
S _ {0} N \left(\frac {\ln \frac {S _ {0}}{X} + \left(r + \frac {\sigma^ {2}}{2}\right) T}{\sigma \sqrt {T}}\right) - X e ^ {- r T} N \left(\frac {\ln \frac {S _ {0}}{X} + \left(r - \frac {\sigma^ {2}}{2}\right) T}{\sigma \sqrt {T}}\right) = c := 1. 8 7 5.
$$

In general, it is not possible to invert the formula to express σ as a function of $S _ { 0 } , X$ , r, T , and c. However, it is not difficult to use MATLAB or other software to find a numerical solution for σ because

$$
\frac {\partial c}{\partial \sigma} > 0.
$$

In this example, the implied volatility is 23.5%.

Implied volatilities can be used to monitor the market’s opinion about the volatility of a particular stock. Analysts often calculate implied volatilities from actively traded options on a certain stock and use them to determine the price of a less actively traded option on the same stock.

The Black-Scholes model assumes that volatility is a known constant. If this were true, the implied volatility should remain invariant with respect to different strike prices. However, in reality, the shape of the implied volatility versus strike price curve often resembles a “smile” rather than a flat line. This is known as the volatility smile phenomenon. In some markets, it shows considerable asymmetry, known as a skew, and sometimes it appears upside down as a frown. The general shape tends to persist for a long time for each underlying asset.

The volatility smile phenomenon implies that there are flaws in the Black-Scholes model.

# 1.2 Improved Models

There are several popular improved models.

Local Volatility Model: The Black-Scholes model assumes that volatility is a known constant. If volatility is not a simple constant, it might be a more complex function of time and the underlying asset.

Stochastic Volatility: The Black-Scholes formulas require the volatility of the underlying asset to be a constant (or a known deterministic function of time). The local volatility model requires the volatility to be a known function of time and asset value. Neither of these assumptions holds true in reality. All volatility time series show that volatility is a highly unstable quantity. It is very variable and unpredictable. Therefore, it is natural to represent volatility itself as a random variable. Stochastic volatility models are currently popular for pricing contracts that are very sensitive to the behavior of volatility.

Jump-Diffusion Model: The Black-Scholes model assumes that the underlying asset path is continuous. However, it is common experience that markets are discontinuous; from time to time, they “jump”, usually downwards. This behavior is not incorporated in the lognormal asset price model, where all paths are continuous.

Discrete Hedging: The Black-Scholes model assumes that delta hedging is continuous. When deriving the Black-Scholes equation, we used the continuous-time Itˆo’s lemma. The delta hedging necessary for risk elimination also had to occur continuously. If there is a finite time between rehedges, there is risk that has not been eliminated.

Transaction Costs: The Black-Scholes model assumes there are no costs in delta hedging. However, not only must we worry about hedging discretely, but we must also consider the costs of rehedging. The buying and selling of assets expose us to bid-offer spreads. In some markets, this is insignificant, allowing us to rehedge as often as possible. In other markets, the cost can be so great that we cannot afford to hedge as frequently as desired.

# 2 Local Volatility Model and Dupire Equation

# 2.1 Local Volatility Model

Assume that the stock price process follows

$$
\frac {d S _ {t}}{S _ {t}} = \mu d t + \sigma_ {t} d B _ {t},
$$

where $B _ { t }$ is Brownian motion, and $\sigma _ { t } = \sigma _ { \mathrm { l o c } } ( S _ { t } , t )$ is a deterministic function of $S _ { t }$ and t.

Using the Black-Scholes analysis, we can still obtain the Black-Scholes equation:

$$
\frac {\partial V}{\partial t} + \frac {1}{2} \sigma_ {\mathrm{loc}} ^ {2} (S, t) S ^ {2} \frac {\partial^ {2} V}{\partial S ^ {2}} + r S \frac {\partial V}{\partial S} - r V = 0,
$$

for $t < T , S > 0$ , with terminal and boundary conditions.

Calibration Problem. A natural question is how to calibrate the function $\sigma _ { \mathrm { l o c } } ( S , t )$ . In general, there are no closed form solutions to the pricing model when volatility is a function of S and t. To identify the volatility function, we need to exploit more information.

Market prices of vanilla options are directly observable. We denote by

$$
V ^ {*} (K _ {i}, T _ {j}), \quad i = 1, 2, \ldots ; \quad j = 1, 2, \ldots
$$

today’s market price of the vanilla option with strike price $K _ { i }$ and maturity $T _ { j }$ . We need to use this information to recover the local volatility function $\sigma _ { \mathrm { l o c } } ( \cdot , \cdot )$ such that our model output

$$
V (S ^ {*}, t ^ {*}; K _ {i}, T _ {j}) = V ^ {*} (K _ {i}, T _ {j}),
$$

where $t ^ { * }$ and $S ^ { * }$ represent the current time and the current stock price, respectively.

Once $\sigma _ { \mathrm { l o c } } ( \cdot , \cdot )$ is obtained, we can use it to price exotic options in the OTC market.

# 2.2 Dupire’s Equation (1993)

Dupire B. (1993) Pricing with a smile, Working paper.

The Black-Scholes formula for call options:

$$
\begin{array}{l} C (S, t; K, T) = e ^ {- r (T - t)} \int_ {0} ^ {\infty} (x - K) ^ {+} \phi (S, t; x, T) d x \\ = e ^ {- r (T - t)} \int_ {K} ^ {\infty} (x - K) \phi (S, t; x, T) d x, \\ \end{array}
$$

where $\phi ( S , t ; x , T )$ is the conditional density function at $T$ given $( S , t )$ in the risk-neutral world. Differentiating the equation twice with respect to $K$ , we have

$$
\frac {\partial^ {2} C}{\partial K ^ {2}} = e ^ {- r (T - t)} \phi (S, t; K, T).
$$

In the risk-neutral world,

$$
\frac {d S _ {t}}{S _ {t}} = r d t + \sigma_ {\mathrm{loc}} (S _ {t}, t) d \widehat {B} _ {t}.
$$

Then $\phi ( S , t ; K , T )$ , as a function of K and T , satisfies the Kolmogorov forward equation,

$$
\frac {\partial \phi}{\partial T} = - \frac {\partial}{\partial K} [ r K \phi ] + \frac {1}{2} \frac {\partial^ {2}}{\partial K ^ {2}} [ \sigma_ {\mathrm{loc}} ^ {2} (K, T) K ^ {2} \phi ].
$$

Noticing that ϕ = er(T −t) ∂2C , $\begin{array} { r } { \phi = e ^ { r ( T - t ) } \frac { \partial ^ { 2 } C } { \partial K ^ { 2 } } } \end{array}$ ∂K2 we infer

$$
\frac {\partial}{\partial T} \left[ \frac {\partial^ {2} C}{\partial K ^ {2}} \right] + r \frac {\partial^ {2} C}{\partial K ^ {2}} = - \frac {\partial}{\partial K} \left[ r K \frac {\partial^ {2} C}{\partial K ^ {2}} \right] + \frac {1}{2} \frac {\partial^ {2}}{\partial K ^ {2}} \left[ \sigma_ {\mathrm{loc}} ^ {2} (K, T) K ^ {2} \frac {\partial^ {2} C}{\partial K ^ {2}} \right].
$$

Integrating the above equation twice gives

$$
\begin{array}{l} \int_ {K} ^ {\infty} \int \eta^ {\infty} \left(\frac {\partial}{\partial T} \frac {\partial^ {2} V}{\partial \xi^ {2}} + r \frac {\partial^ {2} V}{\partial \xi^ {2}}\right) d \xi d \eta \\ = \int_ {K} ^ {\infty} \int \eta^ {\infty} \left(\frac {1}{2} \frac {\partial^ {2}}{\partial \xi^ {2}} \left(\sigma_ {\mathrm{loc}} ^ {2} (\xi , T) \xi^ {2} \frac {\partial^ {2} V}{\partial \xi^ {2}}\right) - r \frac {\partial}{\partial \xi} \left(\xi \frac {\partial^ {2} V}{\partial \xi^ {2}}\right)\right) d \xi d \eta . \\ \end{array}
$$

Assuming

$$
V, K \frac {\partial V}{\partial K}, K ^ {2} \frac {\partial^ {2} V}{\partial K ^ {2}}, K ^ {2} \frac {\partial^ {3} V}{\partial K ^ {3}} \rightarrow 0 \mathrm{as} K \rightarrow \infty ,
$$

and noting

$$
\begin{array}{l} \int_ {K} ^ {\infty} \int \eta^ {\infty} \frac {\partial}{\partial T} \left(\frac {\partial^ {2} V}{\partial \xi^ {2}}\right) d \xi d \eta = \frac {\partial}{\partial T} \int_ {K} ^ {\infty} \int \eta^ {\infty} \frac {\partial^ {2} V}{\partial \xi^ {2}} d \xi d \eta = \frac {\partial V}{\partial T}, \\ \int_ {K} ^ {\infty} \int \eta^ {\infty} \frac {\partial^ {2} V}{\partial \xi^ {2}} d \xi d \eta = V (K, T), \\ \end{array}
$$

and

$$
\int_ {K} ^ {\infty} \int \eta^ {\infty} \frac {\partial^ {2}}{\partial \xi^ {2}} \left(\sigma_ {\mathrm{loc}} ^ {2} (\xi , T) \xi^ {2} \frac {\partial^ {2} V}{\partial \xi^ {2}}\right) d \xi d \eta = \sigma_ {\mathrm{loc}} ^ {2} (K, T) K ^ {2} \frac {\partial^ {2} V}{\partial K ^ {2}},
$$

$$
\int_ {K} ^ {\infty} \int \eta^ {\infty} \frac {\partial}{\partial \xi} \left(\xi \frac {\partial^ {2} V}{\partial \xi^ {2}}\right) d \xi d \eta = K \frac {\partial V}{\partial K} - V,
$$

we get

$$
\frac {\partial V}{\partial T} + r K \frac {\partial V}{\partial K} = \frac {1}{2} \sigma_ {\mathrm{loc}} ^ {2} (K, T) K ^ {2} \frac {\partial^ {2} V}{\partial K ^ {2}},
$$

for $T > t ^ { * }$ and $K > 0$ , where $t ^ { * }$ is the current time. This is Dupire’s equation, which is often rewritten as

$$
\sigma_ {\mathrm{loc}} (K, T) = \sqrt {\frac {2 \left(\frac {\partial V}{\partial T} + r K \frac {\partial V}{\partial K}\right)}{K ^ {2} \frac {\partial^ {2} V}{\partial K ^ {2}}}}. \tag {1}
$$

Dupire Equation via Implied Volatility In practice, finite difference approximations of the partial derivatives in (1) using market prices of vanilla options may incur significant errors because the prices of deep out-of-the-money and deep in-the-money options are on different scales. Instead, the local volatility function is typically recovered using the implied volatility surface, which is easier to interpolate and extrapolate numerically.1 The local volatility $\sigma _ { \mathrm { l o c } }$ at $S = K$ and time T relates to the implied volatility $\sigma _ { \operatorname* { i m p } } ( K , T )$ as follows:

$$
\sigma_ {\mathrm{loc}} (T, K) = \sqrt {\frac {\sigma_ {\mathrm{imp}} ^ {2} + 2 (T - t ^ {*}) \sigma_ {\mathrm{imp}} \frac {\partial \sigma_ {\mathrm{imp}}}{\partial T} + 2 r K (T - t ^ {*}) \sigma_ {\mathrm{imp}} \frac {\partial \sigma_ {\mathrm{imp}}}{\partial K}}{\left(1 + K \sqrt {T - t ^ {*}} d \frac {\partial \sigma_ {\mathrm{imp}}}{\partial K}\right) ^ {2} + K ^ {2} (T - t ^ {*}) \sigma_ {\mathrm{imp}} \left(\frac {\partial^ {2} \sigma_ {\mathrm{imp}}}{\partial K ^ {2}} - \sqrt {T - t ^ {*}} d \left(\frac {\partial \sigma_ {\mathrm{imp}}}{\partial K}\right) ^ {2}\right)}},
$$

where

$$
d = \frac {\ln \left(\frac {S ^ {*}}{K}\right) + (T - t ^ {*}) \left(r + \frac {1}{2} \sigma_ {\mathrm{imp}} ^ {2}\right)}{\sqrt {T - t ^ {*}} \sigma_ {\mathrm{imp}}}.
$$

# 2.3 Inverse Problem

If only a limited number of quotes are available, Dupire’s equation may not be directly applicable. In this case, the problem can be treated as an inverse problem: find $\sigma _ { \mathrm { l o c } }$ to minimize

$$
\left\| V (S ^ {*}, t ^ {*}; K _ {i}, T _ {j}) - V ^ {*} (K _ {i}, T _ {j}) \right\|,
$$

where $V ( S ^ { * } , t ^ { * } ; \cdot , \cdot )$ satisfies Dupire’s equation

$$
\frac {\partial V}{\partial T} - \frac {1}{2} \sigma_ {\mathrm{loc}} ^ {2} (K, T) K ^ {2} \frac {\partial^ {2} V}{\partial K ^ {2}} + r K \frac {\partial V}{\partial K} = 0, \quad T > t ^ {*}, \quad K > 0,
$$

with the initial condition2

$$
V (S ^ {*}, t ^ {*}; K, t ^ {*}) = (S ^ {*} - K) ^ {+}.
$$

There is extensive literature on this inverse problem.

# 2.4 Pros and Cons

The local volatility model has been widely used.

Advantage: It operates within a complete market, which implies the possibility of perfect hedging.

Drawback: The local volatility function $\sigma _ { \mathrm { l o c } } ( \cdot , \cdot )$ changes every day.

# 3 Stochastic Volatility Models

Volatility does not behave as the local volatility model would like it to behave. Next, we assume that volatility follows a stochastic process.

# 3.1 Random Volatility

We continue to assume that $S _ { t }$ satisfies

$$
d S _ {t} = \mu S _ {t} d t + \sigma_ {t} S _ {t} d W _ {1 t},
$$

where the volatility $\sigma _ { t }$ satisfies

$$
d \sigma_ {t} = p (S _ {t}, \sigma_ {t}, t) d t + q (S _ {t}, \sigma_ {t}, t) d W _ {2 t}.
$$

The two increments $d W _ { 1 t }$ and $d W _ { 2 t }$ have a correlation $\rho .$ The choice of functions $p ( S , \sigma , t )$ （号 and $q ( S , \sigma , t )$ is crucial to the evolution of the volatility and thus to the pricing of derivatives.

The value of an option with stochastic volatility is a function of three variables, $V ( S , \sigma , t )$ .

# 3.2 The Pricing Equation

The new stochastic quantity that we are modeling, the volatility, is not a traded asset. Thus, when volatility is stochastic, we face the problem of having a source of randomness that cannot be easily hedged away. Because we have two sources of randomness, we must hedge our option with two other contracts: one being the underlying asset as usual, and the other being another option to hedge the volatility risk. We must therefore set up a portfolio containing one option, with value denoted by $V ( S , \sigma , t )$ , a quantity $- \Delta$ of the asset, and a quantity $- \Delta _ { 1 }$ of another option with value $V _ { 1 } ( S , \sigma , t )$ . We have

$$
\Pi = V - \Delta S - \Delta_ {1} V _ {1}.
$$

The change in this portfolio in a time dt is given by

$$
\begin{array}{l} d \Pi = \left(\frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} S ^ {2} \frac {\partial^ {2} V}{\partial S ^ {2}} + \rho \sigma q S \frac {\partial^ {2} V}{\partial S \partial \sigma} + \frac {1}{2} q ^ {2} \frac {\partial^ {2} V}{\partial \sigma^ {2}}\right) d t \\ - \Delta_ {1} \left(\frac {\partial V _ {1}}{\partial t} + \frac {1}{2} \sigma^ {2} S ^ {2} \frac {\partial^ {2} V _ {1}}{\partial S ^ {2}} + \rho \sigma q S \frac {\partial^ {2} V _ {1}}{\partial S \partial \sigma} + \frac {1}{2} q ^ {2} \frac {\partial^ {2} V _ {1}}{\partial \sigma^ {2}}\right) d t \\ + \left(\frac {\partial V}{\partial S} - \Delta_ {1} \frac {\partial V _ {1}}{\partial S} - \Delta\right) d S + \left(\frac {\partial V}{\partial \sigma} - \Delta_ {1} \frac {\partial V _ {1}}{\partial \sigma}\right) d \sigma , \\ \end{array}
$$

where we have used Itˆo’s lemma on functions of S, σ, and t.

To eliminate all randomness from the portfolio, we must choose

$$
\frac {\partial V}{\partial S} - \Delta - \Delta_ {1} \frac {\partial V _ {1}}{\partial S} = 0,
$$

to eliminate dS terms, and choose

$$
\frac {\partial V}{\partial \sigma} - \Delta_ {1} \frac {\partial V _ {1}}{\partial \sigma} = 0,
$$

to eliminate dσ terms. This leaves us with

$$
\begin{array}{l} d \Pi = \left(\frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} S ^ {2} \frac {\partial^ {2} V}{\partial S ^ {2}} + \rho \sigma q S \frac {\partial^ {2} V}{\partial S \partial \sigma} + \frac {1}{2} q ^ {2} \frac {\partial^ {2} V}{\partial \sigma^ {2}}\right) d t \\ - \Delta_ {1} \left(\frac {\partial V _ {1}}{\partial t} + \frac {1}{2} \sigma^ {2} S ^ {2} \frac {\partial^ {2} V _ {1}}{\partial S ^ {2}} + \rho \sigma q S \frac {\partial^ {2} V _ {1}}{\partial S \partial \sigma} + \frac {1}{2} q ^ {2} \frac {\partial^ {2} V _ {1}}{\partial \sigma^ {2}}\right) d t \\ = r \Pi d t = r (V - \Delta S - \Delta_ {1} V _ {1}) d t, \\ \end{array}
$$

where we have used arbitrage arguments to set the return on the portfolio equal to the risk-free rate.

As it stands, this is one equation in two unknowns, V and $V _ { 1 }$ . This contrasts with the earlier Black-Scholes case, which had one equation in one unknown.

Collecting all terms on the left-hand side and all $V _ { 1 }$ terms on the right-hand side, we find that

$$
\begin{array}{l} \frac {\frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} S ^ {2} \frac {\partial^ {2} V}{\partial S ^ {2}} + \rho \sigma q S \frac {\partial^ {2} V}{\partial S \partial \sigma} + \frac {1}{2} q ^ {2} \frac {\partial^ {2} V}{\partial \sigma^ {2}} + r S \frac {\partial V}{\partial S} - r V}{\frac {\partial V}{\partial \sigma}} \\ = \frac {\frac {\partial V _ {1}}{\partial t} + \frac {1}{2} \sigma^ {2} S ^ {2} \frac {\partial^ {2} V _ {1}}{\partial S ^ {2}} + \rho \sigma q S \frac {\partial^ {2} V _ {1}}{\partial S \partial \sigma} + \frac {1}{2} q ^ {2} \frac {\partial^ {2} V _ {1}}{\partial \sigma^ {2}} + r S \frac {\partial V _ {1}}{\partial S} - r V _ {1}}{\frac {\partial V _ {1}}{\partial \sigma}}. \\ \end{array}
$$

We are fortunate that the left-hand side is a function of V but not $V _ { 1 }$ , and the righthand side is a function of $V _ { 1 }$ but not V . Since the two options will typically have different payoffs, strikes, or expiries, the only way for this to be possible is for both sides to be independent of the contract type. Both sides can only be functions of the independent variables $S , \sigma$ , and t. Thus we have

$$
\frac {\frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} S ^ {2} \frac {\partial^ {2} V}{\partial S ^ {2}} + \rho \sigma q S \frac {\partial^ {2} V}{\partial S \partial \sigma} + \frac {1}{2} q ^ {2} \frac {\partial^ {2} V}{\partial \sigma^ {2}} + r S \frac {\partial V}{\partial S} - r V}{\frac {\partial V}{\partial \sigma}} = - a (S, \sigma , t),
$$

for some function $a ( S , \sigma , t )$ .

Reordering this equation, we have

$$
\frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} S ^ {2} \frac {\partial^ {2} V}{\partial S ^ {2}} + \rho \sigma q S \frac {\partial^ {2} V}{\partial S \partial \sigma} + \frac {1}{2} q ^ {2} \frac {\partial^ {2} V}{\partial \sigma^ {2}} + r S \frac {\partial V}{\partial S} + a (S, \sigma , t) \frac {\partial V}{\partial \sigma} - r V = 0.
$$

in the solution domain $\sigma > 0 , \ S > 0 , \ t \in [ 0 , T )$ . The terminal condition is

$$
V (S, \sigma , T) = \left\{ \begin{array}{l l} (S - X) ^ {+}, & \text {for call option,} \\ (X - S) ^ {+}, & \text {for put option.} \end{array} \right.
$$

Remark 1 In the risk-neutral world, the underlying asset S follows the process

$$
d S _ {t} = r S _ {t} d t + \sigma S _ {t} d \widehat {W} _ {1 t}.
$$

Similarly, the risk-neutral process of σ is

$$
d \sigma_ {t} = a (S _ {t}, \sigma_ {t}, t) d t + q (S _ {t}, \sigma_ {t}, t) d \widehat {W} _ {2 t},
$$

where

$$
a (S, \sigma , t) = p (S, \sigma , t) - \lambda (S, \sigma , t) q (S, \sigma , t),
$$

and $\lambda ( S , \sigma , t )$ is called the market price of risk.

# 3.3 Named Models and Calibration

We give two named models:

• Hull & White (1987):

$$
d (\sigma_ {t} ^ {2}) = k (b - \sigma_ {t} ^ {2}) d t + c \sigma_ {t} ^ {2} d W _ {2 t},
$$

where k, b, and c are constants.

• Heston (1993):

$$
d (\sigma_ {t} ^ {2}) = k (b - \sigma_ {t} ^ {2}) d t + c \sigma_ {t} d W _ {2 t}.
$$

Explicit price formulas are available for the Heston model. For the Hull-White model, explicit formulas exist when S and σ are uncorrelated.

Calibration. Calibrating the Heston model involves estimating parameters $k , b , c , \rho ,$ and the current volatility level $\sigma _ { 0 }$ . This can be formulated as an optimization problem.

# 4 Jump-Diffusion Models

The basic building block for the random walks we have considered so far is continuous Brownian motion based on normally distributed increments. We can think of this as adding to the return from one day to the next a normally distributed random variable with variance proportional to the timestep.

# 4.1 Jump-Diffusion Process

The extra building block we need for the jump-diffusion model for an asset price is the Poisson process. A Poisson process $d q _ { t }$ is defined as

$$
d q _ {t} = \left\{ \begin{array}{l l} 0, & \text {with probability} 1 - \lambda d t, \\ 1, & \text {with probability} \lambda d t, \end{array} \right.
$$

where λ is called the intensity of the Poisson process.

This Poisson process can be incorporated into a model for an asset in the following way:

$$
\frac {d S _ {t}}{S _ {t}} = \mu d t + \sigma d W _ {t} + (J _ {t} - 1) d q _ {t}.
$$

This is the jump-diffusion process. We assume that there is no correlation between the Brownian motion and the Poisson process. If there is a jump $( d q _ { t } = 1 )$ , then $S _ { t }$ immediately goes to the value $J _ { t } S _ { t }$ . For example, a sudden 10% fall in the asset price can be modeled by $J _ { t } = 0 . 9$ . We can generalize further by allowing $J _ { t }$ to be a random quantity.

A jump-diffusion version of Itˆo’s lemma is

$$
d V (S _ {t}, t) = \left(\frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} S _ {t} ^ {2} \frac {\partial^ {2} V}{\partial S ^ {2}} + \mu S _ {t} \frac {\partial V}{\partial S}\right) d t + \sigma S _ {t} \frac {\partial V}{\partial S} d W _ {t} + \left(V (J _ {t} S _ {t}, t) - V (S _ {t}, t)\right) d q _ {t}.
$$

The random walk in ln $S _ { t }$ follows

$$
\begin{array}{l} d \ln S _ {t} = \left(\mu - \frac {\sigma^ {2}}{2}\right) d t + \sigma d W _ {t} + [ \ln (J _ {t} S _ {t}) - \ln (S _ {t}) ] d q _ {t} \\ = \left(\mu - \frac {\sigma^ {2}}{2}\right) d t + \sigma d W _ {t} + \ln J _ {t} d q _ {t}. \\ \end{array}
$$

# 4.2 Merton’s Model (1976)

Hedging when there are jumps. Hold a portfolio of the option and $- \Delta _ { t }$ of the underlying:

$$
\Pi_ {t} = V (S _ {t}, t) - \Delta_ {t} S _ {t}.
$$

The change in the value of this portfolio is

$$
\begin{array}{l} d \Pi_ {t} = d V _ {t} - \Delta_ {t} d S _ {t} \\ = \left(\frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} S _ {t} ^ {2} \frac {\partial^ {2} V}{\partial S ^ {2}} + \mu S _ {t} \frac {\partial V}{\partial S}\right) d t + \sigma S _ {t} \frac {\partial V}{\partial S} d W _ {t} + (V (J _ {t} S _ {t}, t) - V (S _ {t}, t)) d q _ {t} \\ - \Delta_ {t} (\mu S _ {t} d t + \sigma S _ {t} d W _ {t} + (J _ {t} - 1) S _ {t} d q _ {t}). \\ \end{array}
$$

If we choose

$$
\Delta_ {t} = \frac {\partial V (S _ {t} , t)}{\partial S},
$$

we are following a Black-Scholes type of strategy, hedging the diffusive movements. The change in the portfolio value is then

$$
d \Pi_ {t} = \left(\frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} S _ {t} ^ {2} \frac {\partial^ {2} V}{\partial S ^ {2}}\right) d t + \left(V (J _ {t} S _ {t}, t) - V (S _ {t}, t) - (J _ {t} - 1) S _ {t} \frac {\partial V}{\partial S}\right) d q _ {t}.
$$

The portfolio now evolves in a deterministic fashion, except that every so often there is a non-deterministic jump in its value. It can be argued (Merton 1976) that if the jump component of the asset price process is uncorrelated with the market as a whole, then the risk in the discontinuity should not be priced in the option. Diversifiable risk should not be rewarded. In other words, we can take expectations of this expression and set that value equal to the risk-free return from the portfolio, namely,

$$
\mathbb {E} _ {t} (d \Pi_ {t}) = r \Pi_ {t} d t.
$$

This argument is not completely satisfactory, but is a common assumption whenever there is a risk that cannot be fully hedged.

Since there is no correlation between $d W$ and $d q$ , and

$$
\mathbb {E} _ {t} (d q _ {t}) = \lambda d t,
$$

we arrive at

$$
\frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} S ^ {2} \frac {\partial^ {2} V}{\partial S ^ {2}} + r S \frac {\partial V}{\partial S} - r V + \lambda \mathbb {E} ^ {J} [ V (J S, t) - V (S, t) ] - \lambda \mathbb {E} ^ {J} [ J - 1 ] S \frac {\partial V}{\partial S} = 0.
$$

There is a simple solution of this equation in the special case that the logarithm of J is normally distributed. If the logarithm of J is normally distributed with standard deviation $\sigma ^ { \prime } .$ , and if we write

$$
k = \mathbb {E} ^ {J} [ J - 1 ],
$$

then the price of a European non-path-dependent option can be written as

$$
\sum_ {n = 0} ^ {\infty} \frac {e ^ {- \lambda^ {\prime} (T - t)} (\lambda^ {\prime} (T - t)) ^ {n}}{n !} V _ {B S} (S, t; \sigma_ {n}, r _ {n}),
$$

where

$$
\lambda^ {\prime} = \lambda (1 + k), \quad \sigma_ {n} ^ {2} = \sigma^ {2} + \frac {n \sigma^ {\prime 2}}{T - t}, \quad r _ {n} = r - \lambda k + \frac {n \ln (1 + k)}{T - t},
$$

and $V _ { B S }$ is the Black-Scholes formula for the option value in the absence of jumps. This formula can be interpreted as the sum of individual Black-Scholes values, each of which assumes that there have been n jumps, weighted according to the probability that there will have been n jumps before expiry.

# 4.3 \*Wilmott et al.’s Model

In the above, we hedged the diffusive element of the random walk for the underlying. Another possibility is to hedge both the diffusion and jumps as much as we can. For example, we could choose $\Delta _ { t }$ to minimize the variance of the hedged portfolio.

The changes in the value of the portfolio with an arbitrary $\Delta _ { t }$ is

$$
d \Pi_ {t} = (\ldots) d t + \sigma S _ {t} \left(\frac {\partial V}{\partial S} - \Delta_ {t}\right) d W _ {t} + (V (J _ {t} S _ {t}, t) - V (S _ {t}, t) - \Delta_ {t} (J _ {t} - 1) S _ {t}) d q _ {t}.
$$

The variance in this change, which is a measure of the risk in the portfolio, is

$$
\mathrm{var} [ d \Pi_ {t} ] = \sigma^ {2} S _ {t} ^ {2} \left(\frac {\partial V}{\partial S} - \Delta_ {t}\right) ^ {2} d t + \lambda \mathbb {E} ^ {J} \left[ (V (J _ {t} S _ {t}, t) - V (S _ {t}, t) - \Delta_ {t} (J _ {t} - 1) S _ {t}) ^ {2} \right] d t + O (d t ^ {2}).
$$

Neglecting $O ( d t ^ { 2 } )$ , this is minimized by the choice

$$
\Delta_ {t} = \frac {\lambda \mathbb {E} ^ {J} \left[ (J _ {t} - 1) (V (J _ {t} S _ {t} , t) - V (S _ {t} , t)) \right] + \sigma^ {2} S _ {t} \frac {\partial V}{\partial S}}{\lambda \mathbb {E} ^ {J} \left[ (J _ {t} - 1) ^ {2} \right] + \sigma^ {2} S _ {t}}.
$$

If we value the option as a pure discounted real expectation under this best-hedge strategy, then

$$
\mathbb {E} _ {t} [ d \Pi_ {t} ] = r \Pi_ {t} d t,
$$

or

$$
\begin{array}{l} \frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} S ^ {2} \frac {\partial^ {2} V}{\partial S ^ {2}} + \left(\mu - \frac {\sigma^ {2}}{d} (\mu + \lambda k - r)\right) \frac {\partial V}{\partial S} - r V \\ + \lambda \mathbb {E} ^ {J} \left[ (V (J S, t) - V (S, t)) \left(1 - \frac {J - 1}{d} (\mu + \lambda k - r)\right) \right] = 0, \\ \end{array}
$$

where

$$
d = \lambda \mathbb {E} ^ {J} [ (J - 1) ^ {2} ] + \sigma^ {2}, \quad k = \mathbb {E} ^ {J} [ J - 1 ].
$$

When λ = 0, this recovers the Black-Scholes equation.

# 4.4 Summary

Jump diffusion models undoubtedly capture a real phenomenon that is missing from the Black-Scholes model. Yet, they are rarely used in practice. There are three main reasons for this:

• Difficulty in Parameter Estimation: To use any pricing model, one needs to be able to estimate parameters. In the lognormal model, there is just one parameter (volatility) to estimate, which is manageable. More than one parameter can be too complex. The jump diffusion model, even in its simplest form, requires estimates of the probability of a jump, measured by λ, and its size J. This can be made more complicated by having a distribution for J.   
• Difficulty in Solution: The governing equation is no longer a diffusion equation, which is among the easiest problems to solve numerically, and is more complex than solving the basic Black-Scholes equation.   
• Impossibility of Perfect Hedging: Perfect risk-free hedging is impossible when there are jumps in the underlying asset. The use of a jump diffusion model acknowledges that one’s hedge is less than perfect.

In fact, the above remarks also apply to the stochastic volatility model.