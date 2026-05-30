# Continuous-Time Stochastic Control

# Stochastic Differential Equations

We often assume that the price dynamic $S _ { t }$ of a risky asset is described by a SDE of the form

$$
d S _ {t} = \mu (t, S _ {t}) d t + \sigma (t, S _ {t}) d W _ {t}.
$$

Here $\mu$ and $\sigma$ are functions modeling the drift and volatility of the stock price satisfying a certain technical conditions to ensure the existence of the solution to the SDE. $W _ { t }$ is a Brownian motion modeling the randomness of the price process.

# Stochastic differential equations (SDE)

For short time period, one often assumes that $\mu ( t , S _ { t } ) = \mu$ and $\sigma ( t , S _ { t } ) = \sigma$ are constants. Then

$$
S _ {t} = S _ {0} + \mu t + \sigma W _ {t}.
$$

For longer period of time one often assumes that $\mu ( t , S _ { t } ) = \mu S _ { t }$ and $\sigma ( t , S _ { t } ) = \sigma S _ { t }$ . Then

$$
S _ {t} = S _ {0} \cdot \exp \left((\mu - \frac {\sigma^ {2}}{2}) t + \sigma W _ {t}\right).
$$

# Examples of Stochastic Control

I For wealth/portfolio management applications, we often consider a portfolio consisting of risky assets and a riskless bond.   
I Further, we add a “control action” to the SDE to model how the agent invests in the risky assets and adjusts the portfolio dynamically in time.   
I The wealth/portfolio process then depends on the dynamics of the risky assets, the bond and the control.   
I The goal is usually to maximize the terminal wealth which leads to a stochastic control problem.

# The Merton Problem

Merton portfolio problem aims to maximize the expected utility of terminal wealth.

I The price of the risky asset (suppose there is only one risky asset) follows SDE

$$
d S _ {t} = \mu S _ {t} d t + \sigma S _ {t} d W _ {t}.
$$

I The value of the riskless bond is described by $d b _ { t } = r b _ { t } d t$   
I At time $t \in [ 0 , T ]$ , the total wealth $w _ { t }$ is distributed to the risky asset and riskless bond in a proportion of $\pi _ { t }$ and $1 - \pi _ { t }$ , respectively.   
I The agent has a utility function U.

# The Merton Problem

Thus, the Merton problem is

$$
H (w) = \max _ {\pi} \mathbb {E} [ U (w _ {T} ^ {\pi}) ]
$$

subject to the agent’s wealth process:

$$
d w _ {t} ^ {\pi} = \left[ r + \pi_ {t} (\mu - r) \right] w _ {t} ^ {\pi} d t + \sigma \pi_ {t} w _ {t} ^ {\pi} d W _ {t}, \quad w _ {0} ^ {\pi} = w.
$$

The function $H ( w )$ is referred to as the value function.

# The Merton Problem

I In the Merton problem, $\pi _ { t }$ is the control.   
I The total wealth process $w _ { t } ^ { \pi }$ is determined by $\pi _ { t }$ through the SDE.   
I Later we will also consider different starting point say t. Then explicity the value function is $H ( t , w _ { t } ^ { \pi } )$ .   
I Usually $\pi _ { t }$ has to satisfy a certain technical conditions to ensure the existence of solution to the wealth SDE.   
I We often use $\mathcal { A } _ { t , T }$ (or A when the time period is clear from the context) to denote the set of admissible strategies on interval [t, T ].

# Stochastic Control Problem

Previous example motivates us to consider the general stochastic control problem:

$$
H (x) = \sup _ {u \in \mathcal {A} _ {0, T}} H ^ {u} (x) := \mathbb {E} \left[ G (X _ {T} ^ {u}) + \int_ {0} ^ {T} F (s, X _ {s} ^ {u}, u _ {s}) d s \right],
$$

subject to

$$
d X _ {t} ^ {u} = \mu (t, X _ {t} ^ {u}, u _ {t}) d t + \sigma (t, X _ {t} ^ {u}, u _ {t}) d W _ {t}, \quad X _ {0} ^ {u} = x.
$$

Here, for $t \in [ 0 , T ] , u _ { t }$ is the control process and $X _ { t } ^ { u }$ is the controlled process. In general, $W _ { t }$ is a d-dimensional standard Brownian motion. We call $H ^ { u } ( x )$ the performance measure or the objective function.

For example, we can write the Merton problem in the form of general stochastic control problem by defining:

$$
\begin{array}{l} X _ {t} ^ {\pi} = w _ {t} ^ {\pi}, x = w, \mu (t, X _ {t} ^ {\pi}, \pi_ {t}) = [ r + \pi_ {t} (\mu - r) ] w _ {t} ^ {\pi}, \\ \sigma (t, X _ {t} ^ {\pi}, \pi_ {t}) = \pi_ {t} \sigma w _ {t} ^ {\pi}, G = U \text {and} F = 0. \\ \end{array}
$$

# Stochastic Control Problem

To analyze the solution of the stochastic control problem, we embed it into a class of problems:

$$
H (t, x) = \sup _ {u \in \mathcal {A} _ {t, T}} H ^ {u} (t, x) := \mathbb {E} _ {t, x} \left[ G (X _ {T} ^ {u}) + \int_ {t} ^ {T} F (s, X _ {s} ^ {u}, u _ {s}) d s \right],
$$

subject to

$$
d X _ {t} ^ {u} = \mu (t, X _ {t} ^ {u}, u _ {t}) d t + \sigma (t, X _ {t} ^ {u}, u _ {t}) d W _ {t}, X _ {t} ^ {u} = x.
$$

Here $\mathbb { E } _ { t , x }$ is the conditional expectation with respect to $X _ { t } ^ { u } = x$ .

# Stopping Time

To state the dynamical programming principle, we need the concept of a stopping time. Let $\mathcal { F } _ { t } , \ t \in [ 0 , T ]$ be a filtration representing the gradually revealed information.

Stopping time: A ramdon variable τ is called a stopping time if

$$
[ \tau \leq t ] \subset \mathcal {F} _ {t}.
$$

That is, whether $\tau$ happened or not at time t can be determined by the available information at or before that time.

# Dynamical Programming Principle

# Dynamical programming principle

$$
H (t, x) = \sup _ {u \in \mathcal {A}} \mathbb {E} _ {t, x} \left[ H (\tau , X _ {\tau} ^ {u}) + \int_ {t} ^ {\tau} F (s, X _ {s} ^ {u}, u _ {s}) d s \right],
$$

for all $( t , x ) \in [ 0 , T ] \times \mathbb { R } ^ { n }$ and all stopping time $\tau \leq T$ .

Intuition: Taking total sup is the same as taking the sup of partial sup + running cost. The global optimization problem can be decomposed as a recursive local optimization problem.

# Dynamical Programming Principle

For a given stopping time $\tau \leq T ,$

$$
\sup _ {u \in \mathcal {A}} \mathbb {E} _ {t, x} \left[ H (\tau , X _ {\tau} ^ {u}) + \int_ {t} ^ {\tau} F (s, X _ {s} ^ {u}, u _ {s}) d s \right]
$$

$$
\geq \mathbb {E} _ {t, x} \left[ H (\tau , X _ {\tau} ^ {u}) + \int_ {t} ^ {\tau} F (s, X _ {s} ^ {u}, u _ {s}) d s \right]
$$

$$
\geq \mathbb {E} _ {t, x} \left[ G (X _ {\tau} ^ {u}) + \int_ {\tau} ^ {T} F (s, X _ {s} ^ {u}, u _ {s}) d s + \int_ {t} ^ {\tau} F (s, X _ {s} ^ {u}, u _ {s}) d s \right]
$$

$$
= \mathbb {E} _ {t, x} \left[ G (X _ {\tau} ^ {u}) + \int_ {t} ^ {T} F (s, X _ {s} ^ {u}, u _ {s}) d s \right]
$$

Taking sup on the right hand side, we have

$$
\sup _ {u \in \mathcal {A}} \mathbb {E} _ {t, x} \left[ H (\tau , X _ {\tau} ^ {u}) + \int_ {t} ^ {\tau} F (s, X _ {s} ^ {u}, u _ {s}) d s \right] \geq H (t, x)
$$

# Dynamical Programming Principle

Next for any given $\varepsilon > 0$ , select a control $v ^ { \varepsilon } \in { \mathcal { A } }$ such that

$$
H (t, x) \geq H ^ {v ^ {\varepsilon}} (t, x) \geq H (t, x) - \varepsilon .
$$

Define $\bar { v } ^ { \varepsilon } = u _ { t } 1 _ { t \leq \tau } + v _ { t } ^ { \varepsilon } 1 _ { t > \tau }$ . Then

$$
H (t, x) \geq H ^ {\bar {v} ^ {\varepsilon}} (t, x) = \mathbb {E} _ {t, x} \left[ H ^ {\bar {v} ^ {\varepsilon}} (\tau , X _ {\tau} ^ {\bar {v} ^ {\varepsilon}}) + \int_ {t} ^ {\tau} F (s, X _ {s} ^ {\bar {v} ^ {\varepsilon}}, \bar {v} _ {s} ^ {\varepsilon}) d s \right]
$$

$$
= \mathbb {E} _ {t, x} \left[ H ^ {v ^ {\varepsilon}} \left(\tau , X _ {\tau} ^ {u}\right) + \int_ {t} ^ {\tau} F \left(s, X _ {s} ^ {u}, u _ {s}\right) d s \right]
$$

$$
\geq \mathbb {E} _ {t, x} \left[ H (\tau , X _ {\tau} ^ {u}) + \int_ {t} ^ {\tau} F (s, X _ {s} ^ {u}, u _ {s}) d s \right] - \varepsilon .
$$

Taking the limit as $\varepsilon \to 0$ , we have

$$
H (t, x) \geq \sup _ {u \in \mathcal {A}} \mathbb {E} _ {t, x} \left[ H (\tau , X _ {\tau} ^ {u}) + \int_ {t} ^ {\tau} F (s, X _ {s} ^ {u}, u _ {s}) d s \right].
$$

# Hamilton-Jacobi-Bellman (HJB) Equation

The infinitesimal form of the DPP is Hamilton-Jacobi-Bellman Equation:

$$
\partial_ {t} H (t, x) + \sup _ {u \in \mathcal {A}} \left[ \mathcal {L} _ {t} ^ {u} H (t, x) + F (s, x, u) \right] = 0, H (T, x) = G (x),
$$

where $\mathcal { L } _ { t } ^ { u }$ represents the infinitesimal generator of $X _ { t } ^ { u }$ . For example, in one dimensional case,

$$
\mathcal {L} _ {t} ^ {u} = \mu (t, x, u) \partial_ {x} + \frac {1}{2} \sigma^ {2} (t, x, u) \partial_ {x x}.
$$

# HJB Equation

Using Itˆo’s formula, we have

$$
\begin{array}{l} H (\tau , X _ {\tau} ^ {u}) = H (t, x) + \int_ {t} ^ {\tau} \left(\partial_ {s} + \mathcal {L} _ {s} ^ {u}\right) H \left(s, X _ {s} ^ {u}\right) d s \\ + \int_ {t} ^ {\tau} D _ {x} H (s, X _ {s} ^ {u}) \sigma (s, X _ {s} ^ {u}, u _ {s}) d W _ {s} \\ \end{array}
$$

Note that the stochastic integral term with respect to Brownian motion is a martingale, which must have expectation of 0. Then, for any admissible control u, we get that

$$
\begin{array}{l} H (t, x) \geq \mathbb {E} _ {t, x} \left[ H (\tau , X _ {\tau} ^ {u}) + \int_ {t} ^ {\tau} F (s, X _ {s} ^ {u}, u _ {s}) d s \right] \\ = \mathbb {E} _ {t, x} \left[ H (t, x) + \int_ {t} ^ {\tau} \left(\partial_ {s} + \mathcal {L} _ {s} ^ {u}\right) H \left(s, X _ {s} ^ {u}\right) d s \right. \\ \left. + \int_ {t} ^ {\tau} F (s, X _ {s} ^ {u}, u _ {s}) d s \right] \\ \end{array}
$$

# HJB Equation

It follows that

$$
0 \geq \mathbb {E} _ {t, x} \int_ {t} ^ {\tau} \left[ \left(\partial_ {s} + \mathcal {L} _ {s} ^ {u}\right) H \left(s, X _ {s} ^ {u}\right) + F \left(s, X _ {s} ^ {u}, u _ {s}\right) \right] d s.
$$

Dividing by $\tau - t$ and taking the limit as $\tau  t ,$ we get that

$$
0 \geq (\partial_ {t} + \mathcal {L} _ {t} ^ {u}) H (t, x) + F (t, x, u).
$$

The same argument applies to the optimal control yielding the equality. Thus

$$
0 = \partial_ {t} H (t, x) + \sup _ {u} \left[ \mathcal {L} _ {t} ^ {u} H (t, x) + F (t, x, u) \right].
$$

# Verification Theorem

Verification Theorem shows that the (classical) solution of the HJB equation coincides with the optimal value function.

Verification Theorem: If for $( t , x ) \in [ 0 , T ] \times \mathbb { R } ^ { n }$ , there exists an admissible measurable control $u \in { \mathcal { A } }$ such that

$$
\partial_ {t} \psi (t, x) + \sup _ {u \in \mathcal {A}} \left[ \mathcal {L} _ {t} ^ {u} \psi (t, x) + F (s, x, u) \right] = 0, \psi (T, x) = G (x),
$$

and the SDE

$$
d X _ {s} ^ {u} = \mu (s, X _ {s} ^ {u}, u (s, X _ {s} ^ {u})) d t + \sigma (s, X _ {s} ^ {u}, u (s, X _ {s} ^ {u})) d W _ {s}, X _ {t} ^ {u} = x,
$$

admits a unique solution, then $H ( t , x ) = \psi ( t , x )$ is the optimal value function and u is an optimal control.

# The Merton Problem

Recall the Merton problem:

I The agent invests continuously during the time interval [0, T ].   
I The price of the risky asset is described by the SDE

$$
d S _ {t} = \mu S _ {t} d t + \sigma S _ {t} d W _ {t}.
$$

I The riskless asset $b _ { t }$ has the constant interest rate r so that $d b _ { t } = r b _ { t } d t$ .

I At any time $t \in [ 0 , T ]$ , the agent places $\pi _ { t }$ and $1 - \pi _ { t }$ of the total wealth $w _ { t }$ in the risky asset and riskless asset, respectively.

I The agent has a utility function $U$ to measure his performance of the terminal wealth.

# The Merton Problem

Because

$$
w _ {t} ^ {\pi} = \pi_ {t} w _ {t} ^ {\pi} + (1 - \pi_ {t}) w _ {t} ^ {\pi},
$$

we can write down the SDE of the wealth process $w _ { t } ^ { \pi }$ as

$$
\begin{array}{l} {d w _ {t} ^ {\pi}} = {d \pi_ {t} w _ {t} ^ {\pi} + d (1 - \pi_ {t}) w _ {t} ^ {\pi}} \\ = \mu \pi_ {t} w _ {t} ^ {\pi} d t + \sigma \pi_ {t} w _ {t} ^ {\pi} d W _ {t} + r (1 - \pi_ {t}) w _ {t} ^ {\pi} d t \\ = (r + (\mu - r) \pi_ {t}) w _ {t} ^ {\pi} d t + \sigma \pi_ {t} w _ {t} ^ {\pi} d W _ {t}. \\ \end{array}
$$

# The Merton Problem

We can formulate the Merton problem as a stochastic control problem:

$$
H (w) = \max _ {\pi} \mathbb {E} [ U (w _ {T} ^ {\pi}) ]
$$

subject to

$$
d w _ {t} ^ {\pi} = (r + (\mu - r) \pi_ {t}) w _ {t} ^ {\pi} d t + \sigma \pi_ {t} w _ {t} ^ {\pi} d W _ {t}, \quad w _ {0} ^ {\pi} = w.
$$

# The Merton Problem

To use the dynamical programming principle, we imbed the Merton problem into the dynamic control problem starting from time t:

$$
H (t, w) = \max _ {\pi} \mathbb {E} [ U (w _ {T} ^ {\pi}) | w _ {t} ^ {\pi} = w ]
$$

subject to

$$
d w _ {s} ^ {\pi} = (r + (\mu - r) \pi_ {s}) w _ {s} ^ {\pi} d s + \sigma \pi_ {s} w _ {s} ^ {\pi} d W _ {s}, \quad w _ {t} ^ {\pi} = w.
$$

# The Merton Problem: HJB Equation

We can derive the HJB equation as

$$
H _ {t} + r w H _ {w} + \sup _ {\pi} \left[ (\mu - r) \pi w H _ {w} + \frac {1}{2} \sigma^ {2} \pi^ {2} w ^ {2} H _ {w w} \right] = 0
$$

with the terminal condition

$$
H (T, w) = U (w). \tag {1}
$$

# The Merton Problem: HJB Equation

The supremum over the control is attained at

$$
\pi^ {*} = - \frac {\lambda H _ {w}}{\sigma w H _ {w w}}, \quad \text { where } \lambda = \frac {\mu - r}{\sigma}.
$$

Plugging this optimal control back into the HJB equation, we can get the partial differential equation (PDE) of $H ( t , w )$ a s

$$
H _ {t} + r w H _ {w} - \frac {1}{2} \frac {(\mu - r) ^ {2} H _ {w} ^ {2}}{\sigma^ {2} H _ {w w}} = 0
$$

with the terminal condition

$$
H (T, w) = U (w).
$$

# The Merton Problem: HJB Equation

Example-1: We first consider the log utility $U ( w ) = \mathsf { l n } ( w )$ . We can consider the conjecture of solution in the form of

$$
H (t, w) = \ln (w) + h (t),
$$

where the function $h ( t )$ is to be determined.

Substituting this form of solution into the HJB equation, we get the ordinary differential equation (ODE) of $h ( t )$ a s

$$
0 = h ^ {\prime} (t) + r + \frac {\lambda^ {2}}{2}, h (T) = 0.
$$

We can solve this ODE and obtain the explicit solution as

$$
h (t) = \left(r + \frac {\lambda^ {2}}{2}\right) (T - t).
$$

# The Merton Problem: HJB Equation

We can then obtain the explicit optimal value function as

$$
H (t, w) = \ln (w) + \left(r + \frac {\lambda^ {2}}{2}\right) (T - t).
$$

and the (feedback form) optimal portfolio is given by

$$
\pi^ {*} (t, w) = \frac {\lambda}{\sigma} = \frac {\mu - r}{\sigma^ {2}}.
$$

That is, under the logarithmic utility $U ( x ) = \ln ( x )$ , the optimal portfolio strategy is to invest a fixed (constant) fraction of the wealth in the risky asset.

Remark: fixed fraction is an important investment strategy. Merton problem is the theoretical foundation.

# The Merton Problem: HJB Equation

Example-2: Let us consider the Merton problem with the power utility $\textstyle U ( x ) = { \frac { x ^ { p } } { p } }$ with risk aversion constant $p < 1$ and $p \neq 0$ . Based on Dynamic Programming Principle and

$$
H (t, w) = \max _ {\pi} \mathbb {E} \left[ U \left(w _ {t} ^ {\pi}\right) \mid w _ {t} ^ {\pi} = w \right]
$$

$\mathsf { s . t . } d w _ { t } ^ { \pi } = \left( r + ( \mu - r ) \pi _ { t } \right) w _ { t } ^ { \pi } d t + \sigma \pi _ { t } w _ { t } ^ { \pi } d W _ { t }$

we can get the HJB equation with the terminal condition as

$$
\left\{ \begin{array}{l} H _ {t} + r w H _ {w} + \sup _ {\pi} \left[ (\mu - r) \pi w H _ {w} + \frac {1}{2} \sigma^ {2} \pi^ {2} w ^ {2} H _ {w w} \right] = 0 \\ H (T, w) = \frac {w ^ {p}}{p}. \end{array} \right.
$$

# The Merton Problem: HJB Equation

Plugging the optimal control into the HJB, we get

$$
H _ {t} + r w H _ {w} - \frac {1}{2} \frac {(\mu - r) ^ {2} H _ {w} ^ {2}}{\sigma^ {2} H _ {w w}} = 0
$$

Make the ansatz that $\begin{array} { r } { H ( t , w ) = \frac { w ^ { p } } { p } A ( t ) } \end{array}$ , we have that

$\begin{array} { r } { H _ { t } = \frac { w ^ { p } } { p } A ^ { \prime } ( t ) , H _ { w } = w ^ { p - 1 } A ( t ) , H _ { w w } = ( p - 1 ) w ^ { p - 2 } A ( t ) } \end{array}$ . Plugging them back into the HJB equation, we have that

$$
\frac {\omega^ {p}}{p} A ^ {\prime} (t) + r \omega \cdot \omega^ {p - 1} A (t) - \frac {1}{2} \cdot \frac {(\mu - r) ^ {2} \cdot \omega^ {2 p - 2} A ^ {2} (t)}{\sigma^ {2} \cdot (p - 1) \omega^ {p - 2} A (t)} = 0
$$

which give the ODE of $A ( t )$ a s

$$
A ^ {\prime} (t) + \left[ r - \frac {1}{2} \frac {(\mu - r) ^ {2}}{(p - 1) \sigma^ {2}} \right] \cdot p \cdot A (t) = 0.
$$

# The Merton Problem: HJB Equation

Note that the terminal condition $H ( T , w ) = w ^ { p } / p$ implies the terminal condition of $A ( T ) = 1$ . The solution of the above ODE with the terminal condition $A ( T ) = 1$ is given by

$$
A (t) = e ^ {\left[ \frac {1}{2} \frac {(\mu - r) ^ {2}}{(p - 1) \sigma^ {2}} - r \right] p (t - T)}.
$$

Using the solution $\begin{array} { r } { H ( t , w ) = \frac { w ^ { p } } { p } A ( t ) } \end{array}$ and let $\begin{array} { r } { K = \left[ \frac { 1 } { 2 } \frac { ( \mu - r ) ^ { 2 } } { ( p - 1 ) \sigma ^ { 2 } } - r \right] p } \end{array}$ , we

$$
H _ {w} = w ^ {p - 1} e ^ {K (t - T)}, H _ {w w} = (p - 1) w ^ {p - 2} e ^ {K (t - T)}
$$

and the (feedback form) optimal portfolio is

$$
\pi^ {*} (t, w) = \frac {- (\mu - r) H _ {w}}{\sigma^ {2} w H _ {w w}} = - \frac {\mu - r}{\sigma^ {2} (p - 1)}.
$$

# The Merton Problem: HJB Equation

Example-3: Let us now consider the exponential utility $U ( x ) = - e ^ { - x }$ for the agent. By Dynamic Programming Principle, we can get the HJB equation that

$$
\left\{ \begin{array}{l} H _ {t} + r w H _ {w} + \sup _ {\pi} \left[ (\mu - r) \pi w H _ {w} + \frac {1}{2} \sigma^ {2} \pi^ {2} w ^ {2} H _ {w w} \right] = 0 \\ H (T, w) = - e ^ {- w}. \end{array} \right.
$$

Plugging the optimal control back into HJB equation, we get

$$
H _ {t} + r \omega H _ {\omega} - \frac {1}{2} \cdot \frac {(\mu - r) ^ {2} H _ {\omega} ^ {2}}{\sigma^ {2} H _ {\omega \omega}} = 0
$$

# The Merton Problem: HJB Equation

We make the Ansatz that $H ( t , w ) = - e ^ { A ( t ) w + B ( t ) }$ , and it follows that

$$
H _ {w} = A (t) H, \quad H _ {w w} = A ^ {2} (t) H,
$$

$$
A (T) = - 1, \quad B (T) = 0.
$$

We then get that

$$
\Rightarrow \left\{ \begin{array}{l} H _ {t} = - e ^ {A (t) w + B (t)} [ A ^ {\prime} (t) w + B ^ {\prime} (t) ] = H [ A ^ {\prime} (t) w + B ^ {\prime} (t) ] \\ H _ {w} = - e ^ {A (t) w + B (t)} \cdot A (t) = H \cdot A (t) \\ H _ {w} = - e ^ {A (t) w + B (t)} \cdot A ^ {2} (t) = H \cdot A ^ {2} (t) \end{array} \right.
$$

Plugging them back into the HJB equation, we get

$$
H [ A ^ {\prime} (t) w + B ^ {\prime} (t) ] + r w \cdot H \cdot A (t) - \frac {1}{2} \frac {(\mu - r) ^ {2}}{\sigma^ {2}} \cdot \frac {H ^ {2} \cdot A ^ {2} (t)}{H \cdot A ^ {2} (t)} = 0,
$$

that is,

$$
[ A ^ {\prime} (t) w + B ^ {\prime} (t) ] + r w A (t) - \frac {1}{2} \frac {(\mu - r) ^ {2}}{\sigma^ {2}} = 0.
$$

# The Merton Problem: HJB Equation

We then get

$$
\left\{ \begin{array}{l} A ^ {\prime} (t) + r A (t) = 0 \\ B ^ {\prime} (t) - \frac {1}{2} \frac {(\mu - r) ^ {2}}{\sigma^ {2}} = 0 \end{array} \right. \Rightarrow \left\{ \begin{array}{l} A (t) = - e ^ {- r (t - T)} \\ B (t) = \frac {1}{2} \frac {(\mu - r) ^ {2}}{\sigma^ {2}} (t - T). \end{array} \right.
$$

Using the above expressions, we can get the optimal portfolio as

$$
\pi^ {*} (t, w) = \frac {- (\mu - r) A (t) H}{\sigma^ {2} w A ^ {2} (t) H} = \frac {- (\mu - r)}{\sigma^ {2} w A (t)} = e ^ {r (t - T)} \frac {\mu - r}{\sigma^ {2} w}
$$

# Mean-Reverting Drift Model

Let us consider the portfolio optimization problem with power utility $\textstyle U ( x ) = { \frac { x ^ { p } } { p } }$ with risk aversion constant $p < 1$ and $p \neq 0$ . Let T be the time horizon, and the stock price SDE has a mean-reverting drift term that

$$
d S _ {t} = \mu_ {t} S _ {t} d t + \sigma S _ {t} d W _ {t}, \quad t \in [ 0, T ],
$$

and the drift is a mean-reverting process satisfying

$$
d \mu_ {t} = - (\mu_ {t} - \lambda) d t + \sigma_ {\mu} d W _ {t}, \quad t \in [ 0, T ],
$$

where both $S _ { t }$ and $\mu _ { t }$ are driven by the same Brownian motion $W$ , and $\sigma > 0 , \lambda > 0$ and $\sigma _ { \mu } > 0$ are some constants.

# Mean-Reverting Drift Model

The riskless bond price satisfies $d b _ { t } = r b _ { t } d t$ . Let $w _ { t } ^ { \pi }$ represent the total wealth at time t and $\pi _ { t }$ be the proportional of wealth that the agent invests in the stock. The self-financing wealth process under the control $\pi _ { t }$ is given by

$$
d w _ {t} ^ {\pi} = \big (r + (\mu_ {t} - r) \pi_ {t} \big) w _ {t} ^ {\pi} d t + \sigma \pi_ {t} w _ {t} ^ {\pi} d W _ {t}.
$$

The agent aims to solve the optimal investment problem under utility maximization:

$$
u (t, w, \mu) = \sup _ {\pi} \mathbb {E} [ U (w _ {T} ^ {\pi}) | w _ {t} ^ {\pi} = w, \mu_ {t} = \mu ],
$$

where we take both $w _ { t } ^ { \pi }$ and $\mu _ { t }$ as state processes and the value function $u ( t , w , \mu )$ depends on variables t, w and $\mu$

# Mean-Reverting Drift Model

By the DPP, we know that $u ( t , w _ { t } ^ { \pi ^ { * } } , \mu _ { t } )$ is a martingale under the optimal control $\pi ^ { * }$ . By Ito formula, we can get the HJB equation as

$$
\left\{ \begin{array}{l l} u _ {t} + r w u _ {w} + u _ {\mu} (- \mu + \lambda) + \frac {1}{2} u _ {\mu \mu} \sigma_ {\mu} ^ {2} \\ + \sup _ {\pi} \left[ (\mu - r) \pi w u _ {w} + \frac {1}{2} u _ {w w} \sigma^ {2} \pi^ {2} w ^ {2} + u _ {\mu w} \sigma \sigma_ {\mu} \pi w \right] = 0 \\ u (T, w, \mu) = \frac {w ^ {p}}{p} \end{array} \right.
$$

By the first-order condition, the optimal portfolio control is characterized by

$$
\pi^ {*} = \frac {- (\mu - r) u _ {w} - u _ {w \mu} \sigma_ {\mu} \sigma}{\sigma^ {2} w u _ {w w}}.
$$

# Mean-Reverting Drift Model

Plugging it into the HJB, we have:

$$
u _ {t} + r w u _ {w} + u _ {\mu} (- \mu + \lambda) + \frac {1}{2} u _ {\mu \mu} \sigma_ {\mu} ^ {2} - \frac {1}{2} \frac {((\mu - r) u _ {w} + u _ {w \mu} \sigma_ {\mu} \sigma) ^ {2}}{\sigma^ {2} u _ {w w}} = 0.
$$

We make the conjecture that $\begin{array} { r } { u ( t , w , \mu ) = \frac { w ^ { p } } { p } f ( t , \mu ) } \end{array}$ with

$f ( t , \mu ) = \exp ( A ( t ) \mu ^ { 2 } + B ( t ) \mu + C ( t ) )$ so that

$$
u _ {t} = \frac {w ^ {p}}{p} f _ {t}, \quad u _ {w} = w ^ {p - 1} f, \quad u _ {w w} = (p - 1) w ^ {p - 2} f,
$$

$$
u _ {\mu} = \frac {w ^ {p}}{p} f _ {\mu}, \quad u _ {\mu \mu} = \frac {w ^ {p}}{p} f _ {\mu \mu}, \quad u _ {\mu w} = w ^ {p - 1} f _ {\mu}.
$$

# Mean-Reverting Drift Model

Plugging them back into the HJB equation, we get that

$$
\frac {1}{p} f _ {t} + a f + b f _ {\mu} + c f _ {\mu \mu} + d \frac {f _ {\mu} ^ {2}}{f} = 0,
$$

where constants

$$
a = r - \frac {1}{2} \frac {(\mu - r) ^ {2}}{\sigma^ {2} (p - 1)}, b = \frac {1}{p} (- \mu + \lambda) - \frac {(\mu - r) \sigma_ {\mu}}{\sigma (p - 1)}, c = \frac {1}{2} \frac {\sigma_ {\mu} ^ {2}}{p}, d = - \frac {1}{2} \frac {\sigma_ {\mu} ^ {2}}{(p - 1)}.
$$

Note that

$$
f _ {t} = f (\mu^ {2} A ^ {\prime} (t) + \mu B ^ {\prime} (t) + C ^ {\prime} (t))
$$

$$
f _ {\mu} = f (2 \mu A (t) + B (t))
$$

$$
f _ {\mu \mu} = f (2 A (t))
$$

# Mean-Reverting Drift Model

Therefore, we can get the ordinary differential equations (ODEs) as

$$
\frac {1}{p} A ^ {\prime} (t) + 4 d A ^ {2} (t) = 0
$$

$$
\frac {1}{p} B ^ {\prime} (t) + 2 b A (t) + 4 d A (t) B (t) = 0
$$

$$
\frac {1}{p} C ^ {\prime} (t) + a + b B (t) + 2 c A (t) + d B ^ {2} (t) = 0
$$

# Mean-Reverting Drift Model

Using the explicit structure of the optimal value function, we can get the optimal portfolio in the feedback form as

$$
\begin{array}{l} \pi^ {*} (t, w, \mu) = \frac {- (\mu - r) u _ {w} - u _ {w \mu} \sigma_ {\mu} \sigma}{\sigma^ {2} w u _ {w w}} \\ = \frac {- (\mu - r) - (2 \mu A (t) + B (t)) \sigma_ {\mu} \sigma}{\sigma^ {2} (p - 1)}. \\ \end{array}
$$