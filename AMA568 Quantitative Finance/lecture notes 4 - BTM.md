# Binomial Tree Methods for American Options and Exotic Options

Min Dai

https://sites.google.com/view/mindai

The Hong Kong Polytechnic University

# Contents

1 Binomial Tree Methods for American Options 2   
2 BTMs for Barrier Options 3

2.1 Options with a Single Barrier 3   
2.2 Double Barrier Options . . 4

3 BTMs for Asian Options 4

3.1 Continuous-time model . 5   
3.2 BTM for Asian options . . 5   
3.3 Forward Shooting Grid Method (FSGM) 6

4 Appendix: Equivalence between BTM and Explicit Difference Scheme 7

4.1 Explicit Difference Scheme for the Black-Scholes Equation 7   
4.2 Relation between BTM and Explicit Difference Scheme . 8

# 1 Binomial Tree Methods for American Options

We first recall the binomial tree method (BTM) for European vanilla options.

BTM for European vanilla options. The binomial tree method is a widely used discretetime option pricing model. Let T be the expiration date and [0, T ] be the lifetime of the option. Suppose the time interval is divided into N discrete steps, with time points $t _ { n } = n \Delta t$ , $n = 0 , 1 , \ldots , N$ , where $\Delta t = T / N$ . Let $V _ { j } ^ { n }$ denote the option price at time $t _ { n }$ when the underlying asset price is $S _ { j }$ . Assume the underlying price moves up or down by factors u and $d ,$ respectively, so that

$$
S _ {j + 1} = S _ {j} u, \quad S _ {j - 1} = S _ {j} d.
$$

For a put option, the BTM recursion is given by

$$
\left\{ \begin{array}{l l} V _ {j} ^ {n} = e ^ {- r \Delta t} \left[ p V _ {j + 1} ^ {n + 1} + (1 - p) V _ {j - 1} ^ {n + 1} \right], & j = - n, - n + 2, \ldots , n, \\ & n = 0, 1, \ldots , N - 1, \\ V _ {j} ^ {N} = (X - S _ {0} u ^ {j}) ^ {+}, & j = - N, - N + 2, \ldots , N, \end{array} \right.
$$

where

$$
p = \frac {e ^ {r \Delta t} - d}{u - d}, \quad u = e ^ {\sigma \sqrt {\Delta t}}, \quad d = e ^ {- \sigma \sqrt {\Delta t}}.
$$

BTM for American vanilla options. For American-style put options, the BTM recursion becomes

$$
\left\{ \begin{array}{l l} V _ {j} ^ {n} = \max \left\{e ^ {- r \Delta t} \left[ p V _ {j + 1} ^ {n + 1} + (1 - p) V _ {j - 1} ^ {n + 1} \right], (X - S _ {0} u ^ {j}) ^ {+} \right\}, & j = - n, - n + 2, \ldots , n, \\ & n = 0, 1, \ldots , N - 1, \\ V _ {j} ^ {N} = (X - S _ {0} u ^ {j}) ^ {+}, & j = - N, - N + 2, \ldots , N. \end{array} \right.
$$

Using Taylor expansion, one can show that the BTM is consistent with the following continuous-time model:

$$
\left\{ \begin{array}{l} \max \left\{\mathcal {L} _ {B S} V, (X - S) - V (S, t) \right\} = 0, \quad S > 0, \quad t \in [ 0, T), \\ V (S, T) = (X - S) ^ {+}, \end{array} \right.
$$

where the Black-Scholes operator $\mathcal { L } _ { B S }$ is defined as

$$
\mathcal {L} _ {B S} V = \frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} S ^ {2} \frac {\partial^ {2} V}{\partial S ^ {2}} + r S \frac {\partial V}{\partial S} - r V.
$$

# 2 BTMs for Barrier Options

# 2.1 Options with a Single Barrier

Consider a down-and-out call option with terminal payoff

$$
(S _ {T} - X) ^ {+} \mathbf {1} _ {\{S _ {t} > H, t \in [ 0, T ] \}},
$$

where H is the barrier level and 1 is the indicator function:

$$
\mathbf {1} _ {\{S _ {t} > H, t \in [ 0, T ] \}} = \left\{ \begin{array}{l l} 1, & \text { if } S _ {t} > H \text { for all } t \in [ 0, T ], \\ 0, & \text { otherwise }. \end{array} \right.
$$

By the risk-neutral pricing principle, the option value at time zero is

$$
e ^ {- r T} \widehat {\mathbb {E}} \left[ (S _ {T} - X) ^ {+} \mathbf {1} _ {\{S _ {t} > H, t \in [ 0, T ] \}} \right].
$$

Monte Carlo simulation can be used to approximate this value, but it applies only to European-style options.

The BTM can be extended to barrier options. Let $V ( S , t )$ denote the option price before the barrier is hit. Then, for $S > H$ and $t < T$ , the BTM recursion is given by

$$
V (S, t - \Delta t) = e ^ {- r \Delta t} \left[ p V (S u, t) + (1 - p) V (S d, t) \right],
$$

with boundary and terminal conditions

$$
V (H, t) = 0, \quad V (S, T) = (S - X) ^ {+}.
$$

The backward induction is performed on the domain $\{ S > H \} \times [ 0 , T )$ .

By consistency with the Black-Scholes equation, V satisfies

$$
\mathcal {L} _ {B S} V (S, t) = 0,
$$

with the above boundary and terminal conditions.

The BTM can also handle early exercise features in American barrier options.

# 2.2 Double Barrier Options

Consider an option with two barriers $H _ { u }$ and $H _ { d } ,$ , above and below the initial asset price, respectively.

Knock-out case: If the asset touches either barrier before expiry, the option knocks out; otherwise, at expiry, the payoff is $( S - X ) ^ { + }$ . The price function $V ( S , t ; H _ { u } , H _ { d } )$ satisfies

$$
V (S, t - \Delta t) = e ^ {- r \Delta t} \left[ p V (S u, t) + (1 - p) V (S d, t) \right], \quad S \in (H _ {d}, H _ {u}), \quad t \in [ 0, T),
$$

with boundary conditions

$$
V (H _ {u}, t) = 0, \quad V (H _ {d}, t) = 0, \quad t \in [ 0, T),
$$

and terminal condition

$$
V (S, T) = (S - X) ^ {+}, \quad S \in [ H _ {d}, H _ {u} ].
$$

Knock-in case: If the asset touches both barriers before expiry, the payoff is $( S - X ) ^ { + }$ ; otherwise, the option is worthless. The price function satisfies the same recursion in $( H _ { d } , H _ { u } )$ 号 with terminal condition

$$
V (S, T) = 0, \quad S \in [ H _ {d}, H _ {u} ].
$$

The boundary conditions are given by the prices of corresponding single-barrier options:

$$
V (H _ {u}, t) = C _ {d i} (H _ {u}, t; H _ {d}), \quad V (H _ {d}, t) = C _ {u i} (H _ {d}, t; H _ {u}), \quad t \in [ 0, T),
$$

where $C _ { d i }$ and $C _ { u i }$ denote down-in and up-in call option prices, respectively.

# 3 BTMs for Asian Options

Let $S _ { t }$ be the underlying asset price process and $A _ { t }$ be the arithmetic average price defined by

$$
A _ {t} = \frac {1}{t} \int_ {0} ^ {t} S _ {\tau} d \tau .
$$

The value of an arithmetic Asian option is a function of $S _ { t } , A _ { t } .$ , and time t:

$$
V = V (S _ {t}, A _ {t}, t).
$$

At expiry, the payoff $\Lambda ( S _ { T } , A _ { T } )$ is given by

$$
\Lambda (S _ {T}, A _ {T}) = \left\{ \begin{array}{l l} (A _ {T} - X) ^ {+}, & \text {fixed strike Asian call,} \\ (X - A _ {T}) ^ {+}, & \text {fixed strike Asian put,} \\ (S _ {T} - A _ {T}) ^ {+}, & \text {floating strike Asian call,} \\ (A _ {T} - S _ {T}) ^ {+}, & \text {floating strike Asian put.} \end{array} \right.
$$

Problem: Find $V ( S _ { t } , A _ { t } , t )$ for $0 \leq t < T$ .

# 3.1 Continuous-time model

Using delta-hedging or replication arguments, V satisfies

$$
\left\{ \begin{array}{l l} \mathcal {L} V = 0, & t \in (0, T), \\ V (S, A, T) = \Lambda (S, A), \end{array} \right.
$$

for $( S , A ) \in ( 0 , \infty ) ^ { 2 }$ , where

$$
\mathcal {L} V = \frac {1}{t} (S - A) \frac {\partial V}{\partial A} + \mathcal {L} _ {B S} V.
$$

# 3.2 BTM for Asian options

Discretize time as $t _ { n } = n \Delta t , n = 0 , 1 , . . . , N$ , with $\Delta t = T / N$ . Let $V ^ { n } ( S , A )$ denote the option price at time $t _ { n }$ with underlying price S and average A given by

$$
A = \frac {1}{n + 1} \sum_ {i = 0} ^ {n} S _ {t _ {i}},
$$

where $S _ { t _ { i } }$ is the underlying price at time $t _ { i }$ . Assume S moves up to $S u$ with probability p or down to $S d$ with probability $1 - p$ at time $t _ { n + 1 }$ . Then A updates to

$$
A ^ {u} = \frac {(n + 1) A + S u}{n + 2}, \quad A ^ {d} = \frac {(n + 1) A + S d}{n + 2}.
$$

By no-arbitrage, the BTM recursion for American-type Asian options is

$$
V ^ {n} (S, A) = e ^ {- r \Delta t} \left[ p V ^ {n + 1} (S u, A ^ {u}) + (1 - p) V ^ {n + 1} (S d, A ^ {d}) \right], \tag {1}
$$

with

$$
p = \frac {e ^ {r \Delta t} - d}{u - d}, \quad u = e ^ {\sigma \sqrt {\Delta t}}, \quad d = e ^ {- \sigma \sqrt {\Delta t}}.
$$

At expiry,

$$
V ^ {N} (S, A) = \Lambda (S, A).
$$

Backward induction using (1) and the terminal condition yields the option price.

# 3.3 Forward Shooting Grid Method (FSGM)

The BTM is computationally expensive for Asian options due to the growing number of possible averages. Hull and White (1993) proposed restricting averages to a predetermined $\mathrm { g r i d }$ , and Barraquand and Pudet (1996) extended this idea and developed the forward shooting grid method (FSGM).

For a given $\Delta t ,$ define

$$
\Delta Y = \rho \sigma \sqrt {\Delta t},
$$

where $\rho$ is a quantization parameter (with $1 / \rho$ an integer). Define discrete asset and average price grids:

$$
S _ {j} ^ {n} = u ^ {j}, \quad A _ {k} ^ {n} = e ^ {k \Delta Y}, \quad j, k \in \mathbb {Z}, \quad n = 0, \ldots , N.
$$

At time $t _ { n } , ( S _ { j } ^ { n } , A _ { k } ^ { n } )$ moves up or down with probabilities p and $1 - p$ to

$$
(S _ {j + 1} ^ {n + 1}, A _ {k ^ {+}} ^ {n + 1}), (S _ {j - 1} ^ {n + 1}, A _ {k ^ {-}} ^ {n + 1}),
$$

where

$$
A _ {k ^ {\pm}} ^ {n + 1} = \frac {(n + 1) A _ {k} ^ {n} + S _ {j \pm 1} ^ {n + 1}}{n + 2}.
$$

Since $A _ { k ^ { \pm } } ^ { n + 1 }$ may not lie on the grid, interpolation is required. Define

$$
k _ {\mathrm{floor}} ^ {\pm} = \left\lfloor \frac {\ln A _ {k ^ {\pm}} ^ {n + 1}}{\Delta Y} \right\rfloor ,
$$

where ⌊·⌋ is the floor function.

Let $U ^ { n } ( S _ { j } ^ { n } , A _ { k } ^ { n } )$ denote the option value at $( t _ { n } , S _ { j } ^ { n } , A _ { k } ^ { n } )$ . The FSGM backward recursion is

$$
\left\{ \begin{array}{l} U ^ {n} (S _ {j} ^ {n}, A _ {k} ^ {n}) = e ^ {- r \Delta t} \left[ p \Pi_ {A} U ^ {n + 1} (S _ {j + 1} ^ {n + 1}, A _ {k ^ {+}} ^ {n + 1}) + (1 - p) \Pi_ {A} U ^ {n + 1} (S _ {j - 1} ^ {n + 1}, A _ {k ^ {-}} ^ {n + 1}) \right], \\ U ^ {N} (S _ {j} ^ {N}, A _ {k} ^ {N}) = (A _ {k} ^ {N} - X) ^ {+}, \end{array} \right.
$$

for $n = N - 1 , \ldots , 0$ , where $\Pi _ { A }$ is the interpolation operator $( \mathrm { e . g . }$ , linear interpolation):

$$
\Pi_ {A} U ^ {n + 1} (S _ {j \pm 1} ^ {n + 1}, A _ {k ^ {\pm}} ^ {n + 1}) = \alpha_ {- 1} ^ {\pm} U ^ {n + 1} (S _ {j \pm 1} ^ {n + 1}, A _ {k _ {\text {floor}} ^ {\pm} - 1} ^ {n + 1}) + \alpha_ {0} ^ {\pm} U ^ {n + 1} (S _ {j \pm 1} ^ {n + 1}, A _ {k _ {\text {floor}} ^ {\pm}} ^ {n + 1}) + \alpha_ {1} ^ {\pm} U ^ {n + 1} (S _ {j \pm 1} ^ {n + 1}, A _ {k _ {\text {floor}} ^ {\pm} + 1} ^ {n + 1}),
$$

with weights $\alpha _ { - 1 } ^ { \pm } + \alpha _ { 0 } ^ { \pm } + \alpha _ { 1 } ^ { \pm } = 1$ .

Linear interpolation is recommended for accuracy and efficiency.

# 4 Appendix: Equivalence between BTM and Explicit Difference Scheme

# 4.1 Explicit Difference Scheme for the Black-Scholes Equation

Consider the transformation

$$
V (S, t) = u (x, t), \quad S = e ^ {x}.
$$

Then u satisfies

$$
\left\{ \begin{array}{l} \frac {\partial u}{\partial t} + \frac {\sigma^ {2}}{2} \frac {\partial^ {2} u}{\partial x ^ {2}} + \left(r - \frac {\sigma^ {2}}{2}\right) \frac {\partial u}{\partial x} - r u = 0, \quad x \in \mathbb {R}, \quad t \in [ 0, T), \\ u (x, T) = (X - e ^ {x}) ^ {+}. \end{array} \right. \tag {2}
$$

Discretize the domain with mesh sizes $\Delta x , \Delta t > 0$ , and $N \Delta t = T$ . Define the lattice

$$
Q = \{(j \Delta x, n \Delta t): 0 \leq n \leq N, j \in \mathbb {Z} \},
$$

and let $U _ { j } ^ { n }$ approximate $u ( j \Delta x , n \Delta t )$ . The explicit difference scheme is

$$
\frac {U _ {j} ^ {n + 1} - U _ {j} ^ {n}}{\Delta t} + \frac {\sigma^ {2}}{2} \frac {U _ {j + 1} ^ {n + 1} - 2 U _ {j} ^ {n + 1} + U _ {j - 1} ^ {n + 1}}{\Delta x ^ {2}} - \left(r - \frac {\sigma^ {2}}{2}\right) \frac {U _ {j + 1} ^ {n + 1} - U _ {j - 1} ^ {n + 1}}{2 \Delta x} - r U _ {j} ^ {n} = 0,
$$

which can be rearranged as

$$
U _ {j} ^ {n} = \frac {1}{1 + r \Delta t} \left[ (1 - \alpha) U _ {j} ^ {n + 1} + \alpha \left(a U _ {j + 1} ^ {n + 1} + (1 - a) U _ {j - 1} ^ {n + 1}\right) \right],
$$

where

$$
\alpha = \sigma^ {2} \frac {\Delta t}{\Delta x ^ {2}}, \quad a = \frac {1}{2} + \left(r - \frac {\sigma^ {2}}{2}\right) \frac {\Delta x}{2 \sigma^ {2}}.
$$

The terminal condition is

$$
U _ {j} ^ {N} = (X - e ^ {j \Delta x}) ^ {+}, j \in \mathbb {Z}.
$$

# 4.2 Relation between BTM and Explicit Difference Scheme

Setting α = 1, i.e.,

$$
\sigma^ {2} \frac {\Delta t}{\Delta x ^ {2}} = 1,
$$

the scheme reduces to

$$
U _ {j} ^ {n} = \frac {1}{1 + r \Delta t} \left[ a U _ {j + 1} ^ {n + 1} + (1 - a) U _ {j - 1} ^ {n + 1} \right],
$$

where

$$
a = \frac {1}{2} \left[ 1 + \left(r - \frac {\sigma^ {2}}{2}\right) \frac {\sqrt {\Delta t}}{\sigma} \right].
$$

Recall the BTM on the same lattice is

$$
V _ {j} ^ {n} = e ^ {- r \Delta t} \left[ p V _ {j + 1} ^ {n + 1} + (1 - p) V _ {j - 1} ^ {n + 1} \right], \quad j = - n, - n + 2, \ldots , n,
$$

with terminal condition

$$
V _ {j} ^ {N} = (X - u ^ {j}) ^ {+}, \quad j = - N, - N + 2, \ldots , N.
$$

Since

$$
e ^ {- r \Delta t} = \frac {1}{1 + r \Delta t} + O (\Delta t ^ {2}), \quad p = a + O (\Delta t ^ {3 / 2}), \quad u = e ^ {\sigma \sqrt {\Delta t}} = e ^ {\Delta x},
$$

the binomial tree method is equivalent to the explicit difference scheme up to higher-order terms in $\Delta t .$ .