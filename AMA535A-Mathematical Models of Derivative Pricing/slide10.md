# AMA535: Mathematics of Derivative Pricing AMA535A: Mathematical Models of Derivative Pricing

XU, Zuo Quan

The Hong Kong Polytechnic University

# Other Options

# Introduction to Asian Options

# Definition

Asian options are path-dependent options whose payoff depends on some form of averaging of the underlying asset price.

# Origin of the Name

Term “Asian” comes from the first known transaction occurring in Tokyo.   
Reflects the Asian financial markets where these were first popularized.

# Motivation

# Why Asian Options Exist

Contracts depending on single snapshot are vulnerable to sudden large shocks or price manipulation.   
• Asian options are more robust against such phenomena.   
• Smoothing effect reduces volatility impact.

# Classification of Asian Options

Let $A _ { T }$ denote the average price over the entire period [0, T ] between initiation and maturity.

# Fixed Strike:

Call payoff: $( A _ { T } - K ) ^ { + }$ .   
Put payoff: $( K - A _ { T } ) ^ { + }$ .

# Floating Strike:

Call payoff: $( S _ { T } - A _ { T } ) ^ { + }$ .   
Put payoff: $( A _ { T } - S _ { T } ) ^ { + }$ .

# Types of Averaging Methods

Four main types of averaging for $A _ { T }$

Discretely sampled:

• Arithmetic average: $\textstyle { \frac { 1 } { n } } \sum _ { i = 1 } ^ { n } S _ { t _ { i } }$   
Geometric average: exp $\textstyle \left( { \frac { 1 } { n } } \sum _ { i = 1 } ^ { n } \ln S _ { t _ { i } } \right) = ( S _ { t _ { 1 } } \dots S _ { t _ { n } } ) ^ { 1 / n }$

Continuously sampled:

• Arithmetic average: $\begin{array} { r } { { \frac { 1 } { T } } \int _ { 0 } ^ { T } S _ { t } \mathrm { d } t } \end{array}$   
• Geometric average: exp $\begin{array} { r } { \left( \frac { 1 } { T } \int _ { 0 } ^ { T } \ln S _ { t } \mathrm { d } t \right) } \end{array}$ .

# PDE for Path-Dependent Options

Introduce a path-dependent variable

$$
I _ {t} = \int_ {0} ^ {t} f (u, S _ {u}) \mathrm{d} u,
$$

where $f ( \cdot )$ is specific to the path-dependent option under consideration.

Assume the value for the path-dependent option is $V ( t , x , I )$   
Apply to Itô’s lemma to $V ( t , S _ { t } , I _ { t } )$ :

$$
\mathrm{d} V (t, S _ {t}, I _ {t}) = \frac {\partial V}{\partial t} \mathrm{d} t + \frac {\partial V}{\partial x} \mathrm{d} S _ {t} + \frac {\partial V}{\partial I} \mathrm{d} I _ {t} + \frac {1}{2} \frac {\partial^ {2} V}{\partial x ^ {2}} \mathrm{d} \langle S, S \rangle_ {t}.
$$

# PDE for Path-Dependent Options

• Note $\mathrm { d } I _ { t } = f ( t , S _ { t } )$ dt.   
• In the risk-neutral world: $\mathrm { d } S _ { t } = r S _ { t } \mathrm { d } t + \sigma S _ { t } \mathrm { d } B _ { t } ^ { Q }$   
• Using risk-neutral valuation principle:

# PDE for Path-Dependent Options

$$
\begin{array}{l} \frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} x ^ {2} \frac {\partial^ {2} V}{\partial x ^ {2}} + r x \frac {\partial V}{\partial x} - r V + \frac {\partial V}{\partial I} f (t, x) = 0, \\ (t, x, I) \in [ 0, T ] \times (0, \infty) \times (0, \infty). \\ \end{array}
$$

# Key Insight

The path-dependency enters through the additional term $\textstyle { \frac { \partial V } { \partial I } } f ( t , x )$ in the drift.

# Boundary Conditions for Continuously Sampled Average

• Arithmetic average: $\begin{array} { r } { f ( t , x ) = x , A _ { T } = \frac { I _ { T } } { T } } \end{array}$   
Fixed Strike:

Call payoff: $\begin{array} { r } { V ( T , x , I ) = ( \frac { I } { T } - K ) ^ { + } } \end{array}$ .   
• Put payoff: $\begin{array} { r } { V ( T , x , I ) = ( K - \frac { I } { T } ) ^ { + } } \end{array}$

Floating Strike:

Call payoff: $\begin{array} { r } { V ( T , x , I ) = ( x - \frac { I } { T } ) ^ { + } } \end{array}$ .   
• Put payoff: $\begin{array} { r } { V ( T , x , I ) = ( \frac { I } { T } - x ) ^ { + } } \end{array}$ .

# Boundary Conditions for Continuously Sampled Average

• Geometric average: $f ( t , x ) = \ln x , A _ { T } = e ^ { \frac { I _ { T } } { T } }$   
Fixed Strike:

• Call payoff: $V ( T , x , I ) = ( e ^ { \frac { I } { T } } - K ) ^ { + }$ .   
• Put payoff: $V ( T , x , I ) = ( K - e ^ { \frac { I } { T } } ) ^ { + }$

Floating Strike:

Call payoff: $V ( T , x , I ) = ( x - e ^ { \frac { I } { T } } ) ^ { + }$ .   
• Put payoff: $V ( T , x , I ) = ( e ^ { \frac { I } { T } } - x ) ^ { + }$ .

# Closed Form for Continuously Sampled Geometric Average Options

Closed form price formulae exist for continuously sampled geometric average Asian options.   
Note $\mathrm { d } I _ { t } = \ln S _ { t }$ dt, so

$$
I _ {T} = I _ {t} + (T - t) \ln S _ {t} + \int_ {t} ^ {T} (\ln S _ {u} - \ln S _ {t}) \mathrm{d} u,
$$

so the Asian call option value with fixed strike is

$$
\begin{array}{l} C _ {\mathrm{fix}} (t, x, I) = e ^ {- r (T - t)} \mathbb {E} ^ {Q} \left[ \left(e ^ {\frac {I _ {T}}{T}} - K\right) ^ {+} \mid S _ {t} = x, I _ {t} = I \right] \\ = e ^ {- r (T - t)} \mathbb {E} ^ {Q} \left[ (e ^ {\frac {I + (T - t) \ln x + \xi}{T}} - K) ^ {+} \mid S _ {t} = x, I _ {t} = I \right]. \\ \end{array}
$$

where

$$
\xi = \int_ {t} ^ {T} \left(\ln S _ {u} - \ln S _ {t}\right) \mathrm{d} u.
$$

# Closed Form for Continuously Sampled Geometric Asian Options

• One can prove that, in the risk-neutral world,

$$
\xi = \int_ {t} ^ {T} (\ln S _ {u} - \ln S _ {t}) \mathrm{d} u
$$

is independent of the history $\mathcal { F } _ { t }$ , and follows $N ( \bar { \mu } , \bar { \sigma } ^ { 2 } )$ , where

$$
\bar {\mu} = \frac {(2 r - \sigma^ {2}) (T - t) ^ {2}}{4}, \bar {\sigma} ^ {2} = \frac {\sigma^ {2} (T - t) ^ {3}}{3}.
$$

Thus,

$$
\begin{array}{l} \mathbb {E} ^ {Q} \left[ (e ^ {\frac {I + (T - t) \ln x + \xi}{T}} - K) ^ {+} \mid S _ {t} = x, I _ {t} = I \right] \\ = \mathbb {E} ^ {Q} \left[ \left(e ^ {\frac {I + (T - t) \ln x + \xi}{T}} - K\right) ^ {+} \right] \\ = \int_ {- \infty} ^ {\infty} (e ^ {\frac {I + (T - t) \ln x + \bar {\mu} + \bar {\sigma} y}{T}} - K) ^ {+} \frac {1}{\sqrt {2 \pi}} e ^ {- \frac {1}{2} y ^ {2}}   \mathrm{d} y. \\ \end{array}
$$

# Closed Form for Continuously Sampled Geometric Asian Options

# Exercise 11.1

Derive the Black-Scholes-like price formulae for call and put options with fixed and floating strike.

# Summary

# Key Points on Asian Options

• Depend on average price rather than terminal price.   
• Two main types: fixed strike and floating strike.   
• Four averaging: discrete/continuous, arithmetic/geometric.   
• PDE approach extends naturally to path-dependent options.   
• Additional term appears in PDE due to path-dependency.   
• Derive specific PDE for arithmetic Asian options.   
• Discuss numerical methods for solving these PDEs.   
• Explore approximation techniques for arithmetic averages.

# Barrier Option

One of the most commonly traded path-dependent options is the continuous barrier option. This is an option with the ordinary call/put payoff subject to an additional event of whether a prescribed level has been crossed or not by the underlying stock price during the life of the option.   
In general, barrier options can be classified according to whether the asset price needs to pass or to avoid a certain level to receive a payoff. In the first case they are called knock-in options, in the second knock-out.

# Down-and-Out Call Barrier Option

• A down-and-out call option striking at K and with a barrier at B will pay

$$
(S _ {T} - K) ^ {+}
$$

at maturity T , provided the underlying stock price never goes below B, i.e. the barrier is being avoided.

If the barrier is reached before maturity, the option is said to be knock out and the option becomes worthless.   
Thus its terminal payoff can be written as

$$
(S _ {T} - K) ^ {+} \mathbb {1} _ {\{\inf _ {t \leqslant T} S _ {t} > B \}}
$$

$$
= \left\{ \begin{array}{l l} S _ {T} - K, & \text { if   } S _ {t} > B \text {   for   all   } t \leqslant T \text {   and   } S _ {T} > K; \\ 0, & \text { otherwise. } \end{array} \right.
$$

# Down-and-In Call Barrier Option

• A down-and-in call option will pay $( S _ { T } - K ) ^ { + }$ at maturity T , provided at some point during the life of the option the underlying stock passes below B; otherwise, the option becomes worthless.   
The option is said to knock in when the barrier is crossed.   
Its the terminal payoff can be written as

$$
(S _ {T} - K) ^ {+} \mathbb {1} _ {\{\inf _ {t \leqslant T} S _ {t} \leqslant B \}}
$$

$$
= \left\{ \begin{array}{l l} S _ {T} - K, & \text { if   } S _ {t} \leqslant B \text {   for   some   } t \leqslant T \text {   and   } S _ {T} > K; \\ 0, & \text { otherwise. } \end{array} \right.
$$

# Remarks

The above are examples of knock-out and knock-in options with a down-stream barrier. That is, the options are knock-out or knock-in as soon as the current stock price moves down to the barrier.   
Similarly, we can define options with an upstream barrier, where the barrier lies above the current stock.   
In general, we can have any combination of up/down, in/out and call/put that we like.   
If one knock-out and one knock-in options have the same payoff and barrier, then (show this by no-arbitrage argument)

knock-out + knock-in = vanilla European.

# Reflection Principle for Brownian Motion

We explain the reflection principle for Brownian motion. The argument is not rigorous at all, so you should refer to more advanced texts for technical details.   
Let B be a Brownian motion, and let $m _ { t }$ denote the minimum value of B over the time horizon [0, t], i.e. $m _ { t } = \operatorname* { m i n } _ { s \leqslant t } B _ { s }$ .   
We now compute the probability of the event ${ \mathcal { A } } ,$ , defined by

$$
\mathcal {A} = \left\{B _ {T} \geqslant x, m _ {T} \leqslant y \right\}, y <   0, y \leqslant x.
$$

Note $\mathcal { A } = \{ B _ { T } \geqslant x \}$ if $y \geqslant 0$ , since $m _ { T } \leqslant 0$ holds trivially.

We now link it by the reflection principle to the event B, defined by

$$
\mathcal {B} = \{B _ {T} \leqslant 2 y - x \}.
$$

# Reflection Principle for Brownian Motion

![](images/532f80dec429003e00a7ea1c606e7911e4d63f84ae6edd212ad334710aabf284.jpg)

<details>
<summary>line</summary>

| t     | Blue Line | Red Line |
|-------|-----------|----------|
| 0     | 0         | 0        |
| τ     | y         | y        |
| >τ    | >y        | <y       |
</details>

Reflection Principle: The process reflected about level y (red curve) after the first hitting time ⌧ is also a Brownian motion.

Mathematically, $B _ { T } - B _ { \tau }$ is symmetrically distributed, so that

$$
\mathbb {P} (B _ {T} - B _ {\tau} \geqslant x - y \mid \mathcal {F} _ {\tau}) = \mathbb {P} (B _ {T} - B _ {\tau} \leqslant y - x \mid \mathcal {F} _ {\tau}).
$$

# Reflection Principle for Brownian Motion

For any path in ${ \mathcal { A } } ,$ the hitting time $\tau$ for the level y must be no late than $T .$ . Now, if we were to reflect the path after the time $\tau$ about the horizontal level $y ,$ , the terminal value of such a ”reflected” path would fall below the level $2 y - x$ , thus resulting in a path in .   
On the other hand, for any path in , the hitting time $\tau$ for the level $y$ must be no late than $T _ { \parallel }$ , since $0 > y \geqslant 2 y - x$ . Now, if we were to reflect the path after the time $\tau$ about the horizontal level $y ,$ , the terminal value of such a ”reflected” path would fall above the level x, thus resulting in a path in .

# Reflection Principle for Brownian Motion

• Mathematically, $\mathbb { P } ( \mathcal { A } ) = \mathbb { P } ( \mathcal { B } ) , \mathfrak { i . e . }$ ,

$$
\mathbb {P} (B _ {T} \geqslant x, m _ {T} \leqslant y) = \mathbb {P} (B _ {T} \leqslant 2 y - x), y <   0, y \leqslant x.
$$

Consequently,

$$
\mathbb {P} (B _ {T} \geqslant x, m _ {T} > y) = \mathbb {P} (x \leqslant B _ {T} \leqslant x - 2 y), y <   0, y \leqslant x;
$$

and

$$
\mathbb {P} (m _ {T} \geqslant y) = \mathbb {P} (- | B _ {T} | \geqslant y), y <   0.
$$

More generally, for any function g, we have

$$
\begin{array}{l} \mathbb {E} [ g (B _ {T}) \mathbb {1} _ {\mathcal {A}} ] = \mathbb {E} [ g (2 y - B _ {T}) \mathbb {1} _ {\mathcal {B}} ] \\ = \mathbb {E} [ g (2 y - B _ {T}) \mathbb {1} _ {B _ {T} \leqslant 2 y - x} ] \\ = \int_ {- \infty} ^ {2 y - x} g (2 y - z) \frac {1}{\sqrt {2 \pi T}} e ^ {- \frac {z ^ {2}}{2 T}} \mathrm{d} z. \\ \end{array}
$$

# PDE for Down-and-Out Barrier Option

Let us denote the value of a down-and-out barrier option by $V ( t , x )$

• When the barrier is hit, the option becomes worthless, thus

$$
V (t, B) = 0, t \in [ 0, T ].
$$

The solution domain for $( t , x )$ is $[ 0 , T ] \times ( B , \infty )$ .   
The value at T is the same as corresponding vanilla European payoff $( \varphi ( x )$ say) as long as $x > B$ .   
The Black-Scholes PDE holds in the solution domain:

$$
\left\{ \begin{array}{l l} V _ {t} (t, x) + \frac {1}{2} \sigma^ {2} x ^ {2} V _ {x x} (t, x) + r x V _ {x} (t, x) - r V (t, x) = 0, \\ \qquad \qquad \qquad \qquad \qquad \qquad (t, x) \in [ 0, T ] \times (B, \infty), \\ V (T, x) = \varphi (x), & \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad x > B. \end{array} \right.
$$

# Formula for Down-and-Out Barrier Option

Let

$$
d _ {1, 2} = \frac {\log (x) - \log (K)}{\sigma \sqrt {T - t}} + (r \pm \frac {1}{2} \sigma) \sqrt {T - t},
$$

$$
d _ {3, 4} = \frac {\log (B ^ {2}) - \log (x K)}{\sigma \sqrt {T - t}} + (r \pm \frac {1}{2} \sigma) \sqrt {T - t},
$$

$$
d _ {5, 6} = \frac {\log (x) - \log (B)}{\sigma \sqrt {T - t}} + (r \pm \frac {1}{2} \sigma) \sqrt {T - t},
$$

$$
d _ {7, 8} = \frac {\log (B) - \log (S)}{\sigma \sqrt {T - t}} + (r \pm \frac {1}{2} \sigma) \sqrt {T - t}.
$$

# Formula for Down-and-Out Barrier Option

# Theorem 11.1 (Formula for Down-and-Out Barrier Option)

Let $C _ { D O } ( t , x , B , K )$ denote the value of Down-and-Out Barrier Option. Let $C _ { E } ( t , x , K )$ denote the value of vanilla European call option.

• $I f B \leqslant K$ , then

$$
C _ {D O} (t, x, B, K) = C _ {E} (t, x, K) - \left(\frac {B}{x}\right) ^ {\frac {2 r}{\sigma^ {2}} - 1} C _ {E} (t, B ^ {2} / x, K).
$$

• $I f B > K$ , then

$$
\begin{array}{l} C _ {D O} (t, x, B, K) = x N (d _ {5}) - K e ^ {- r (T - t)} N (d _ {6}) \\ - \left(\frac {B}{x}\right) ^ {\frac {2 r}{\sigma^ {2}} + 1} x N (d _ {7}) - \left(\frac {B}{x}\right) ^ {\frac {2 r}{\sigma^ {2}} - 1} K e ^ {- r (T - t)} N (d _ {8}). \\ \end{array}
$$