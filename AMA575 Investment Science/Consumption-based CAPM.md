# Consumption-based CAPM

Lecturer: Selena QIAN

Hong Kong Polytechnic University

February 4, 2026

From CAPM to CCAPM: Connect to macroeconomic variables → what is the environment endogenizing the relationship in CAPM.   
Motivation of better understanding return: Arbitrage from the right model. e.g. a high alpha indicating undervalued stock → buy.

. Illustration

$$
\begin{array}{l} E _ {\text { Market }} (R _ {i}) = R _ {f} + \lambda_ {M} \times \operatorname{Cov} (R _ {i}, R _ {M}), \\ E _ {T u r e} (R _ {i}) = \alpha + R _ {f} + \lambda_ {M} \times \operatorname{Cov} (R _ {i}, R _ {M}), \text {   where   } \alpha > 0. \\ \end{array}
$$

The CAPM could be improved.

Risk-averse investors want to smooth consumption over time and different states of economy → they buy and sell financial assets.   
Why do people save? → So they can consume more in the future.   
How do people save? → By investing in financial assets.   
Asset prices (and, hence, returns) must somehow be related to investor’s consumption!

Maximization problem:

$$
\max _ {Y} U (C _ {t}) + E _ {t} [ \theta   U (C _ {t + 1}) ]
$$

$\begin{array} { r l } { { 5 . \mathrm { t . } } } & { { } C _ { t } = e _ { t } - P _ { t } Y } \end{array}$

$$
C _ {t + 1} = e _ {t + 1} + (P _ {t + 1} + D _ {t + 1}) Y
$$

Future payoff: $P _ { t + 1 } + D _ { t + 1 }$ .   
Time discount factor: $\theta$   
Time additive utility.   
You can only choose portfolio, Y .   
Endowment at date t, $e _ { t }$   
。 Of course, in equilibrium, price is affected by trading strategy.

Solution to the maximization problem (the Euler equation):

$$
U ^ {\prime} (C _ {t}) P _ {i, t} = E _ {t} \left[ \theta U ^ {\prime} \left(C _ {t + 1}\right) \left(P _ {i, t + 1} + D _ {i, t + 1}\right) \right].
$$

。 Intuition

. LHS: Extra utility from selling a unit of asset at time t. Note sell a unit of stock at price $P _ { i , t }$ get you $P _ { i , t }$ consumption, and $U ^ { \prime } ( C _ { t } ) P _ { i , i }$ t extra utility.   
RHS: Expected extra discounted utility from holding a unit of asset from time t to time $t + 1$ .

From the definition of net returns, $R _ { i , t + 1 } \equiv \frac { P _ { i , t + 1 } + D _ { i , t + 1 } - P _ { i , t } } { P _ { i , t } }$ Pi ,t+1 + Di ,t+1 − Pi ,t , it follows: Pi ,t

$$
1 = E _ {t} \left[ \theta \frac {U ^ {\prime} (C _ {t + 1})}{U ^ {\prime} (C _ {t})} (1 + R _ {i, t + 1}) \right].
$$

$$
1 = E _ {t} \left[ m _ {t + 1} (1 + R _ {i, t + 1}) \right]. \tag {1}
$$

where $m _ { t + 1 } = \theta \frac { U ^ { \prime } ( C _ { t + 1 } ) } { U ^ { \prime } ( C _ { t } ) }$ is the so called stochastic discount factor.

The “Law of One Price” (LOP) (“Principle of no arbitrage”) implies that there will always exist a stochastic discount factor, $m _ { t + 1 }$ , such that (1) holds → Asset pricing theories can conveniently be expressed in terms of their implied stochastic discount factors.   
In the C-CAPM, the stochastic discount factor equals the intertemporal marginal rate of substitution in consumption.

Time-separable “power utility” (Constant Relative Risk Aversion, CRRA):

$$
U (C _ {t}) = \frac {C _ {t} ^ {1 - \gamma} - 1}{1 - \gamma}. \tag {2}
$$

where $\gamma \geq 0$ is the constant degree of relative risk-aversion.

$$
\Rightarrow \quad m _ {t + 1} = \theta \left(\frac {C _ {t + 1}}{C _ {t}}\right) ^ {- \gamma}. \tag {3}
$$

? Risk-neutrality: $\gamma = 0 \Rightarrow m _ { t + 1 } = \theta$

$$
E _ {t} (1 + R _ {i, t + 1}) = \frac {1 - \operatorname{Cov} _ {t} \left((1 + R _ {i , t + 1}) , \theta \left(\frac {C _ {t + 1}}{C _ {t}}\right) ^ {- \gamma}\right)}{E _ {t} \left(\theta \left(\frac {C _ {t + 1}}{C _ {t}}\right) ^ {- \gamma}\right)}. \tag {4}
$$

The more positively correlated $R _ { i , t + 1 }$ is with $\frac { C _ { t + 1 } } { C _ { t } }$ , the higher expected return.   
Intuition: When returns and consumption growth are positively correlated, the asset is expected to give bad returns when consumption is low, and good returns when consumption is high → the asset does not help smooth consumption over time → the asset is considered ‘risky’ and, hence, demands a high expected return.   
Expected return equals to riskless rate + risk premium.

# The Risk-free Rate and the C-CAPM

A ‘risk-free’ asset has a known return from t to t + 1, and a zero correlation with the stochastic discount factor

$$
\Rightarrow 1 + R _ {f, t + 1} = \frac {1}{E _ {t} m _ {t + 1}}.
$$

With CRRA utility:

$$
1 + R _ {f, t + 1} = \frac {1}{E _ {t} \left(\theta \left(\frac {C _ {t + 1}}{C _ {t}}\right) ^ {- \gamma}\right)}. \tag {5}
$$

? In the C-CAPM, the risk-free return is endogenous (in contrast to the standard CAPM, where it is exogenous) and intimately related to expected consumption growth. . For $\gamma > 0$ , the risk-free rate is high (low) when consumption growth is expected to be high (low). (What is the intuition?)

If consumption is likely to be higher in the future → consume more in order to smooth their lifetime consumption.

# Assume that Ri,t+1 and Ct+1/Ct are Jointly Log-normally Distributed

For reality, assume log-normal distribution, while for simplicity, turn to normal distribution.   
Let $r _ { i , t + 1 } \equiv \mathsf { l n } ( 1 + R _ { i , t + 1 } )$ and $\Delta c _ { t + 1 } \equiv \mathsf { I n } \left( \frac { C _ { t + 1 } } { C _ { t } } \right)$ be jointly normally distributed, with variances $\sigma _ { i , t + 1 } ^ { 2 }$ and $\sigma _ { c , t + 1 } ^ { 2 }$ , respectively, and covariance $\mathsf { C o v } _ { t } ( \Delta c _ { t + 1 } , r _ { i , t + 1 } )$ . Then the C-CAPM with CRRA utility implies expressions for $\boldsymbol { E } _ { t } { \boldsymbol { r } } _ { i , t + 1 }$ and $r _ { f , t + 1 }$ .

$$
r _ {f, t + 1} = - \ln \theta + \gamma E _ {t} \Delta c _ {t + 1} - \frac {1}{2} \gamma^ {2} \sigma_ {c, t + 1} ^ {2}. \tag {6}
$$

$$
E _ {t} r _ {i, t + 1} - r _ {f, t + 1} + \frac {1}{2} \sigma_ {i, t + 1} ^ {2} = \gamma \operatorname{Cov} _ {t} (\Delta c _ {t + 1}, r _ {i, t + 1}). \tag {7}
$$

$$
E _ {t} r _ {i, t + 1} = r _ {f, t + 1} - \frac {1}{2} \sigma_ {i, t + 1} ^ {2} + \gamma \operatorname{Cov} _ {t} (\Delta c _ {t + 1}, r _ {i, t + 1}).
$$

Real interest rates are high when people are impatient, when expected consumption growth is high (intertemporal substitution), or when risk is low (precautionary saving).

# Derivation

To derive above expression for the risk-free rate (6), start with (4).   
Using the fact that normal z means $E e ^ { z } = e ^ { E ( z ) + \frac { 1 } { 2 } \sigma ^ { 2 } ( z ) }$ . The term ${ \scriptstyle { \frac { 1 } { 2 } } } \sigma ^ { 2 } ( z )$ is called Jensen’s inequality effect.   
We have

$$
\begin{array}{l} 1 + R _ {f, t + 1} = \frac {1}{E _ {t} \left(\theta \left[ \exp \left(\ln \left(\frac {C _ {t + 1}}{C _ {t}}\right) ^ {- \gamma}\right) \right]\right)} \\ = \left[ \theta E _ {t} \left(\exp \left(- \gamma \ln \left(\frac {C _ {t + 1}}{C _ {t}}\right)\right)\right) \right] ^ {- 1} \\ = \left[ \theta E _ {t} \left(\exp (- \gamma \Delta c _ {t + 1})\right) \right] ^ {- 1} \\ \end{array}
$$

$$
= \left[ \theta \exp \Big (- \gamma E _ {t} \Delta c _ {t + 1} + \frac {\gamma^ {2}}{2} \sigma^ {2} (\Delta c _ {t + 1}) \Big) \right] ^ {- 1}.
$$

# Explanation on Eq. (7)

. The term $\scriptstyle { \frac { 1 } { 2 } } \sigma _ { i , t + 1 } ^ { 2 }$ is the Jensen effect. But if we consider the log of the expected ratio of gross returns, we eliminate the need for the Jensen inequality term.   
Note that

$$
E [ 1 + R _ {t + 1} ] = E [ e ^ {r _ {t + 1}} ] = e ^ {E [ r _ {t + 1} ] + \frac {1}{2} \sigma_ {t + 1} ^ {2}}
$$

then we have

$$
\begin{array}{l} \ln \left(E _ {t} \left[ (1 + R _ {t + 1}) / (1 + R _ {f, t}) \right]\right) = \ln \left(E _ {t} [ 1 + R _ {t + 1} ]\right) - \ln \left(1 + R _ {f, t}\right) \\ = \ln \left(e ^ {E [ r _ {t + 1} ] + \frac {1}{2} \sigma_ {t + 1} ^ {2}}\right) - \ln (1 + R _ {f, t}) \\ = E \left[ r _ {t + 1} \right] + \frac {1}{2} \sigma_ {t + 1} ^ {2} - r _ {f, t} = \gamma \operatorname{cov} _ {t} \left(c _ {t + 1}, r _ {t + 1}\right). \\ \end{array}
$$

Covariances are ‘king’ in stochastic discount factor models, not volatility.

Risk-premium on asset i = (Price of risk) × (Amount of risk) where:

Price of $\mathsf { r i s k } = \gamma$   
Amount of $\mathsf { r i s k } = \mathsf { C o v } _ { t } \big ( \Delta c _ { t + 1 } , r _ { i , t + 1 } \big )$

Notice the analogy to the standard CAPM, where (Price of risk) $= \frac { E ( R _ { m } ) - R _ { f } } { \sigma _ { m } ^ { 2 } }$ , and $( \mathsf { A m o u n t  o f } \mathsf { r i s k } ) = \mathsf { C o v } ( R _ { i } , R _ { m } )$ .

Expected return on the market portfolio: All expressions above also apply when the risky asset is the market portfolio. Just set i = m such that $R _ { i , t + 1 } = R _ { m , t + 1 }$ and $r _ { i , t + 1 } = r _ { m , t + 1 } \to$ In the C-CAPM the market return is endogenous (in contrast to the standard CAPM, where it is exogenous).   
. CAPM is a special case of C-CAPM: CAPM implies that

$$
m _ {t + 1} = a + b R _ {m, t + 1}
$$

If $\mathsf { U } ^ { \prime } ( \mathsf { C } _ { t + 1 } )$ is perfectly correlated with $R _ { m , t + 1 }$ , C-CAPM reduces to CAPM.

# Commonnesses

Express average return as riskless rate + risk premium.   
Use covariance to measure the risk of risky asset.

# 。 Differences

Different measure of bad time! Consumption growth is more fundamental!   
C-CAPM endogenizes the riskless rate, which is exogenously given in CAPM!