# AMA535: Mathematics of Derivative Pricing AMA535A: Mathematical Models of Derivative Pricing

XU, Zuo Quan

The Hong Kong Polytechnic University

# Brownian Motion & Stochastic Calculus

# Sample

Stock price of Cheung Kong in the past years   
![](images/bf014b5d6aca2a9e5add010656e21ee0f6c00ad155703761be3f7c1833baef34.jpg)

<details>
<summary>line</summary>

| Date       | Price (HKD) | Volume (Millions) |
| ---------- | ----------- | ----------------- |
| Nov 30, 2010 | 130         | 30                |
</details>

# Sample

Stock price of Hong Kong Electric in the past years   
![](images/a51c810b09ee9725f0975a0e1b501ec3ac7626a05e9d667a50b774395f7b324b.jpg)

<details>
<summary>line</summary>

| Date       | Price (Millions) | Volume (Millions) |
| ---------- | ---------------- | ----------------- |
| Nov 30, 2010 | 52               | 15                |
</details>

# Observation

• Stock prices exhibit a trend (drift).   
• Stock prices also show random fluctuations (volatility).

# Model

We model the stock price based on these observations. Return rate over a short interval $[ t , t + \Delta t ]$ :

$$
\text { return   rate } = \frac {\text { price } - \text { original   price }}{\text { original   price }}.
$$

The return rate of a stock on a short time $[ t , t + \Delta t ]$ is expressed as

$$
\frac {\Delta S _ {t}}{S _ {t}},
$$

where $\Delta S _ { t } = S _ { t + \Delta t } - S _ { t }$ .

# Model: Stock Return Rate

By our observations,

$$
\frac {\Delta S _ {t}}{S _ {t}} = \mu \Delta t + \sigma \Delta B _ {t}
$$

where

• µ = drift (average rate of return),   
• ω = volatility (randomness),   
$\Delta B _ { t }$ = random variable with zero mean (to be defined).

# Stochastic Di!erential Equation (SDE)

Adopting di!erential notation, we write:

$$
\frac {\mathrm{d} S _ {t}}{S _ {t}} = \mu \mathrm{d} t + \sigma \mathrm{d} B _ {t},
$$

or equivalently,

$$
\mathrm{d} S _ {t} = \mu S _ {t} \mathrm{d} t + \sigma S _ {t} \mathrm{d} B _ {t},
$$

and in integral form,

$$
S _ {t} = S _ {0} + \int_ {0} ^ {t} \mu S _ {u} \mathrm{d} u + \int_ {0} ^ {t} \sigma S _ {u} \mathrm{d} B _ {u}.
$$

# Deterministic Case: No Volatility

If $\sigma = 0$ , the model reduces to:

$$
S _ {t} = S _ {0} + \int_ {0} ^ {t} \mu S _ {u} \mathrm{d} u,
$$

or, in di!erential form,

$$
\frac {\mathrm{d} S _ {t}}{S _ {t}} = \mu \mathrm{d} t.
$$

This is an ordinary di!erential equation (ODE) with solution:

$$
S _ {t} = S _ {0} e ^ {\mu t}.
$$

Interpretation: Exponential growth, like a bank account with interest rate $\mu$ and no uncertainty.

# Deterministic vs Stochastic Growth

![](images/ef751ecfa4b956aa6789c09d3d1b74fed1c7f377940084bbd1767c1feb916e32.jpg)

<details>
<summary>line</summary>

| t    | Deterministic | Stochastic |
| ---- | ------------- | ---------- |
| t1   | ~0.5          | ~0.3       |
| t2   | ~1.0          | ~0.6       |
| t3   | ~1.8          | ~0.9       |
| t4   | ~2.8          | ~1.2       |
| t5   | ~4.0          | ~1.5       |
| t6   | ~6.0          | ~1.8       |
| t7   | ~8.0          | ~2.0       |
| t8   | ~10.0         | ~2.2       |
| t9   | ~12.0         | ~2.4       |
| t10  | ~14.0         | ~2.6       |
| t11  | ~16.0         | ~2.8       |
| t12  | ~18.0         | ~3.0       |
| t13  | ~20.0         | ~3.2       |
| t14  | ~22.0         | ~3.4       |
| t15  | ~24.0         | ~3.6       |
| t16  | ~26.0         | ~3.8       |
| t17  | ~28.0         | ~4.0       |
| t18  | ~30.0         | ~4.2       |
| t19  | ~32.0         | ~4.4       |
| t20  | ~34.0         | ~4.6       |
| t21  | ~36.0         | ~4.8       |
| t22  | ~38.0         | ~5.0       |
| t23  | ~40.0         | ~5.2       |
| t24  | ~42.0         | ~5.4       |
| t25  | ~44.0         | ~5.6       |
| t26  | ~46.0         | ~5.8       |
| t27  | ~48.0         | ~6.0       |
| t28  | ~50.0         | ~6.2       |
| t29  | ~52.0         | ~6.4       |
| t30  | ~54.0         | ~6.6       |
| t31  | ~56.0         | ~6.8       |
| t32  | ~58.0         | ~7.0       |
| t33  | ~60.0         | ~7.2       |
| t34  | ~62.0         | ~7.4       |
| t35  | ~64.0         | ~7.6       |
| t36  | ~66.0         | ~7.8       |
| t37  | ~68.0         | ~8.0       |
| t38  | ~70.0         | ~8.2       |
| t39  | ~72.0         | ~8.4       |
| t40  | ~74.0         | ~8.6       |
| t41  | ~76.0         | ~8.8       |
| t42  | ~78.0         | ~9.0       |
| t43  | ~80.0         | ~9.2       |
| t44  | ~82.0         | ~9.4       |
| t45  | ~84.0         | ~9.6       |
| t46  | ~86.0         | ~9.8       |
| t47  | ~88.0         | ~10.0      |
| t48  | ~90.0         | ~10.2      |
| t49  | ~92.0         | ~10.4      |
| t50  | ~94.0         | ~10.6      |
| t51  | ~96.0         | ~10.8      |
| t52  | ~98.0         | ~11.0      |
| t53  | ~100.0        | ~11.2      |
| t54  | ~102.0        | ~11.4      |
| t55  | ~104.0        | ~11.6      |
| t56  | ~106.0        | ~11.8      |
| t57  | ~108.0        | ~12.0      |
| t58  | ~110.0        | ~12.2      |
| t59  | ~112.0        | ~12.4      |
| t60  | ~114.0        | ~12.6      |
| t61  | ~116.0        | ~12.8      |
| t62  | ~118.0        | ~13.0      |
| t63  | ~120.0        | ~13.2      |
| t64  | ~122.0        | ~13.4      |
| t65  | ~124.0        | ~13.6      |
| t66  | ~126.0        | ~13.8      |
| t67  | ~128.0        | ~14.0      |
| t68  | ~130.0        | ~14.2      |
| t69  | ~132.0        | ~14.4      |
| t70  | ~134.0        | ~14.6      |
| t71  | ~136.0        | ~14.8      |
| t72  | ~138.0        | ~15.0      |
| t73  | ~140.0        | ~15.2      |
| t74  | ~142.0        | ~15.4      |
| t75  | ~144.0        | ~15.6      |
| t76  | ~146.0        | ~15.8      |
| t77  | ~148.0        | ~16.0      |
| t78  | ~150.0        | ~16.2      |
| t79  | ~152.0        | ~16.4      |
| t80  | ~154.0        | ~16.6      |
| t81  | ~156.0        | ~16.8      |
| t82  | ~158.0        | ~17.0      |
| t83  | ~160.0        | ~17.2      |
| t84  | ~162.0        | ~17.4      |
| t85  | ~164.0        | ~17.6      |
| t86  | ~166.0        | ~17.8      |
| t87  | ~168.0        | ~18.0      |
| t88  | ~170.0        | ~18.2      |
| t89  | ~172.0        | ~18.4      |
| t90  | ~174.0        | ~18.6      |
| t91  | ~176.0        | ~18.8      |
| t92  | ~178.0        | ~19.0      |
| t93  | ~180.0        | ~19.2      |
| t94  | ~182.0        | ~19.4      |
| t95  | ~184.0        | ~19.6      |
| t96  | ~186.0        | ~19.8      |
| t97  | ~188.0        | ~20.0      |
| t98  | ~190.0        | ~20.2      |
| t99  | ~192.0        | ~20.4      |
| t100 | ~194.0        | ~20.6      |
| t1     | -             | -          |
| T     = -T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   T   F    end
    end
</details>

# Key Questions

• What happens if the volatility ω is not zero?   
• What is $B _ { t } ?$ (Brownian motion)   
• What is the meaning of the stochastic integral?

$$
S _ {t} = S _ {0} + \int_ {0} ^ {t} \mu S _ {u} \mathrm{d} u + \int_ {0} ^ {t} \sigma S _ {u} \mathrm{d} B _ {u}.
$$

# History of Brownian Motion

1827: Robert Brown, an English botanist, observed that pollen grains suspended in water performed a continual, random “swarming motion.” This phenomenon was later named Brownian motion.   
1905: Albert Einstein provided a theoretical explanation, attributing the motion to the random bombardment of pollen grains by water molecules. This work linked Brownian motion to molecular theory and provided evidence for the existence of atoms.   
1923: Norbert Wiener gave a rigorous mathematical foundation for this process, proving the existence of what is now called the Wiener process.

In this course, we will use the terms Brownian motion and Wiener process interchangeably.

# Definition: Brownian Motion

A stochastic process $B : [ 0 , \infty ) \times \Omega  \mathbb { R }$ is called a standard Brownian motion (or Wiener process) on a probability space $( \Omega , \mathcal { F } , \mathbb { P } )$ if

(a) $B _ { 0 } = 0$   
(b) The sample paths $t \mapsto B _ { t }$ are continuous;   
Stationary increments: For any $t \ > \ s \ \geqslant \ 0 , \ B _ { t } \ - \ B _ { s } \ \sim$ $\mathcal { N } ( 0 , t - s )$ ;   
(d) Independent increments: For any $0 \leqslant t _ { 0 } < t _ { 1 } < \cdot \cdot \cdot < t _ { n } <$ $t _ { n + 1 }$ and $n \geqslant 1$ , the random variables

$$
B _ {t _ {0}}, B _ {t _ {1}} - B _ {t _ {0}}, B _ {t _ {2}} - B _ {t _ {1}}, \ldots , B _ {t _ {n + 1}} - B _ {t _ {n}}
$$

are independent.

# Remark 8.1

Brownian motion is the fundamental model for continuous-time randomness.

# Extensions of Brownian Motion

# Adapted Brownian Motion:

Let $\{ \mathcal { F } _ { t } : t \geqslant 0 \}$ be a filtration (representing the information available up to time t). We say B is an $\cdot$ -Brownian motion if, for any $t > s \geqslant 0$ , the increment $B _ { t } - B _ { s }$ is independent of $\mathcal { F } _ { s }$ .

# Multidimensional Brownian Motion:

The process $\{ B _ { t } = ( B _ { t } ^ { 1 } , B _ { t } ^ { 2 } , \ldots , B _ { t } ^ { n } ) ^ { \prime } , t \geqslant 0 \}$ is called an $n -$ dimensional standard Brownian motion if each $\{ B _ { t } ^ { i } , t \geqslant 0 \}$ is a one-dimensional standard Brownian motion and the components are independent.

These generalizations are essential for modeling multiple sources of randomness in finance.

# Property: Covariance of Brownian Motion

# Example 8.1

Show that Cov $( B _ { s } , B _ { t } ) = \operatorname* { m i n } ( s , t )$ for all s, $t \geqslant 0$

# Proof.

Assume $s \leqslant t .$ . Then $\boldsymbol { B _ { t } } = \boldsymbol { B _ { s } } + \left( \boldsymbol { B _ { t } } - \boldsymbol { B _ { s } } \right)$ , where $B _ { s }$ and $B _ { t } - B _ { s }$ are independent, so

$$
\begin{array}{l} \operatorname{Cov} (B _ {s}, B _ {t}) = \mathbb {E} [ B _ {s} B _ {t} ] - \mathbb {E} [ B _ {s} ] \mathbb {E} [ B _ {t} ] \\ = \mathbb {E} [ B _ {s} (B _ {s} + (B _ {t} - B _ {s})) ] \\ = \mathbb {E} [ B _ {s} ^ {2} ] + \mathbb {E} [ B _ {s} (B _ {t} - B _ {s}) ] \\ = \mathbb {E} [ B _ {s} ^ {2} ] + \mathbb {E} [ B _ {s} ] \mathbb {E} [ B _ {t} - B _ {s} ] \\ = s. \\ \end{array}
$$

The case $s > t$ can be proved similarly.

# Property

# Example 8.2

$$
F i n d \mathbf {V a r} (3 B _ {1} + 6 B _ {4} + 2 B _ {7}) a n d \mathbb {E} [ B _ {1} ^ {2} B _ {2} B _ {4} ].
$$

Solution: Let $Z _ { 1 } = B _ { 7 } - B _ { 4 }$ and $Z _ { 2 } = B _ { 4 } - B _ { 1 }$ . Then $B _ { 1 } , \ Z _ { 1 }$ , and $Z _ { 2 }$ are independent. Note $B _ { 1 } \sim N ( 0 , 1 ) , Z _ { 1 } \sim N ( 0 , 3 ) , Z _ { 2 } \sim$ $N ( 0 , 3 )$ , so

$$
\begin{array}{l} \mathbf {V a r} (3 B _ {1} + 6 B _ {4} + 2 B _ {7}) \\ = \operatorname{Var} \left(2 Z _ {1} + 8 Z _ {2} + 1 1 B _ {1}\right) \\ = \operatorname{Var} \left(2 Z _ {1}\right) + \operatorname{Var} \left(8 Z _ {2}\right) + \operatorname{Var} \left(1 1 B _ {1}\right) \\ = 4 \operatorname{Var} \left(Z _ {1}\right) + 6 4 \operatorname{Var} \left(Z _ {2}\right) + 1 2 1 \operatorname{Var} \left(B _ {1}\right) \\ = 4 * 3 + 6 4 * 3 + 1 2 1 * 1 = 3 2 5. \\ \end{array}
$$

# Definition: Markov Property

Markov property means that only the present value of a process is relevant for predicting the future; the past history and the way the present has emerged from the past are irrelevant.

A real-valued process $\{ X _ { t } , t \geqslant 0 \}$ has the Markov property (with respect to the filtration $\{ \mathcal { F } _ { t } , t \geqslant 0 \} )$ if, for any $t > s \geqslant 0$ and any open set $A \subseteq \mathbb { R }$ ,

$$
\mathbb {P} (X _ {t} \in A \mid \mathcal {F} _ {s}) = \mathbb {P} (X _ {t} \in A \mid X _ {s}).
$$

A stochastic process that satisfies the Markov property is called a Markov process.

# Remark 8.2

The Markov property is fundamental for modeling memoryless random phenomena.

# Markov Process

# Theorem 10

Brownian motion is a Markov process.

# Proof.

By property (d), for any $t > s \geqslant 0$ , the increment $B _ { t } - B _ { s }$ is independent of $\mathcal { F } _ { s }$ . Thus,

$$
\begin{array}{l} \mathbb {P} (B _ {t} \in A \mid \mathcal {F} _ {s}) = \mathbb {P} (B _ {t} - B _ {s} \in A - B _ {s} \mid \mathcal {F} _ {s}) \\ = \mathbb {P} (B _ {t} - B _ {s} \in A - B _ {s} | B _ {s}) \\ = \mathbb {P} (B _ {t} \in A \mid B _ {s}), \\ \end{array}
$$

for any open set $A \subseteq \mathbb { R }$ . Therefore, Brownian motion is a Markov process.

# Definition: Martingale, Submartingale, Supermartingale

Let $\{ X _ { t } , t \ \geqslant \ 0 \}$ be a stochastic process adapted to a filtration $\{ \mathcal { F } _ { t } , t \geqslant 0 \}$ .

• Submartingale: X is a submartingale if $\mathbb { E } [ | X _ { t } | ] < \infty$ and

$$
\mathbb {E} \left[ X _ {t} \mid \mathcal {F} _ {s} \right] \geqslant X _ {s}, \quad \forall 0 \leqslant s \leqslant t.
$$

Supermartingale: X is a supermartingale if $\mathbb { E } [ | X _ { t } | ] < \infty$ and

$$
\mathbb {E} [ X _ {t} \mid \mathcal {F} _ {s} ] \leqslant X _ {s}, \quad \forall 0 \leqslant s \leqslant t.
$$

Martingale: X is a martingale if it is both a submartingale and a supermartingale, i.e.,

$$
\mathbb {E} [ X _ {t} \mid \mathcal {F} _ {s} ] = X _ {s}, \quad \forall 0 \leqslant s \leqslant t.
$$

# Remark 8.3

Martingales are central to modern probability theory and financial mathematics.

# Martingale: Examples

# Exercise 8.1

Show that $\{ B _ { t } ^ { 2 } - t , t \ge 0 \}$ and $\left\{ e ^ { a B _ { t } - \frac { 1 } { 2 } a ^ { 2 } t } , t \geqslant 0 \right\}$ are both martingales, where a is a constant.

# Definition

A random variable ε valued in $[ 0 , \infty ]$ is called a stopping time (with respect to a given filtration $\{ \mathcal { F } _ { t } , t \geqslant 0 \} )$ if, at any time $t ,$ we know whether $\tau$ has happened before or after time $t ,$ , namely,

$$
\{\tau \leqslant t \}, \{\tau > t \} \in \mathcal {F} _ {t}, \quad \forall t.
$$

In other words, the determination of whether $\tau$ has occurred by time t can be made by looking at the information $\mathcal { F } _ { t }$ , without anticipation of the future.

# Finite and Bounded Stopping Times

We say ε is a finite stopping time if $\tau < \infty$ with probability one (also called almost surely). It is bounded if there exists a constant c such that $\tau \leqslant c$ with probability one.

# Exercise 8.2

Show that if ε is a nonnegative constant, then it is a stopping time.

# Exercise 8.3

$I f \tau$ and ϑ are both stopping times, then so are $\tau \wedge \theta , \tau \vee \theta , \tau + \theta$ and $4 \tau$ . What about $\tau / 2 ?$

Here and hereafter, $a \wedge b = \operatorname* { m i n } \{ a , b \}$ and $a \vee b = \operatorname* { m a x } \{ a , b \}$

# Hitting Time

Suppose $\{ X _ { t } , t \geqslant 0 \}$ is a real-valued continuous stochastic process and let A be a subset of R.

The hitting time is the first time $X _ { t }$ hits $A _ { i }$ , that is,

$$
\tau_ {A} = \inf \{t \geqslant 0: X _ {t} \in A \}.
$$

Then $\tau _ { A }$ is a stopping time.

If $A$ is closed, then $X _ { \tau _ { A } } \in A$ and $X _ { t } \notin A$ for any $t < \tau _ { A }$ . It may happen that $X _ { t }$ never hits $A ,$ , so that $\tau _ { A } = + \infty$ .

# First Passage Time

For a constant $a \in \mathbb { R }$ , we define the first passage time for the level a as

$$
T _ {a} = \inf \{t \geqslant 0 \mid X _ {t} = a \}.
$$

Then $T _ { a }$ is also a stopping time for any $a \in \mathbb { R }$ .

# Exercise 8.4

Given $a > X _ { 0 }$ , show that

$$
\left\{T _ {a} \leqslant t \right\} = \left\{\max _ {s \leqslant t} X _ {s} \geqslant a \right\}.
$$

Given $a < X _ { 0 }$ , show that

$$
\left\{T _ {a} \leqslant t \right\} = \left\{\min _ {s \leqslant t} X _ {s} \leqslant a \right\}.
$$

Hence we conclude that the first passage time is a stopping time.

# Doob’s Optional Stopping Theorem

# Theorem 8.1 (Doob’s Optional Stopping Theorem)

Suppose $\{ X _ { t } , t \geqslant 0 \}$ is a martingale and ε is a stopping time. If one of the following conditions holds:

• ε is a bounded random variable, i.e., $\tau \leqslant T$ for some constant   
• The stopped process $\{ X _ { t \wedge \tau } , t \geqslant 0 \}$ is bounded and $\tau < \infty$   
Then

$$
\mathbb {E} [ X _ {\tau} ] = X _ {0}.
$$

# Remark 8.4

This theorem is fundamental in the theory of martingales and has many applications in stochastic processes and mathematical finance.

# Example

# Example 8.3

$$
L e t \tau = \min \{t \geqslant 0: B _ {t} \notin (- 1, 1) \}. S h o w t h a t \mathbb {E} [ \tau ] = 1.
$$

Solution: Because $\{ B _ { t } ^ { 2 } - t , t \geqslant 0 \}$ is a martingale, by Doob’s Optional Stopping Theorem,

$$
\mathbb {E} [ B _ {\tau} ^ {2} - \tau ] = B _ {0} ^ {2} - 0 = 0,
$$

so $\mathbb { E } [ \tau ] = \mathbb { E } [ B _ { \tau } ^ { 2 } ]$ . At time ε , we have $B _ { \tau } = \pm 1$ , so $B _ { \tau } ^ { 2 } = 1$ . Thus,

$$
\mathbb {E} [ \tau ] = \mathbb {E} [ B _ {\tau} ^ {2} ] = 1.
$$

# Exercise 8.5

Determine the probability that a Brownian motion hits →1 earlier than 3.

# Definition: Stochastic (Itô) Integral for Simple Processes

A process f is called a simple process if it can be written as

$$
f (t) = X _ {0} \mathbf {1} _ {\{0 \}} (t) + \sum_ {i \geqslant 0} X _ {i} \mathbf {1} _ {(t _ {i}, t _ {i + 1} ]} (t) = \left\{ \begin{array}{l l} X _ {0}, & t = 0; \\ X _ {k}, & t _ {k} <   t \leqslant t _ {k + 1}, \end{array} \right.
$$

where $0 = t _ { 0 } < t _ { 1 } < \cdots < t _ { k } < \cdot \cdot \cdot$ is a partition of $[ 0 , \infty )$ and $X _ { k }$ are square-integrable, $\mathcal { F } _ { t _ { k } - \mathsf { m e a s u r a b l } }$ le random variables $( k =$ $0 , 1 , 2 , \ldots )$ . The stochastic integral (or Itô integral) of f on [0, T ] is defined as, if $t _ { k } \leqslant T \leqslant t _ { k + 1 }$ ,

$$
\begin{array}{l} \int_ {0} ^ {T} f (t) \mathrm{d} B _ {t} = \sum_ {i \geqslant 0} X _ {i} \left(B (T \wedge t _ {i + 1}) - B (T \wedge t _ {i})\right) \\ = X _ {0} B _ {t _ {1}} + X _ {1} (B _ {t _ {2}} - B _ {t _ {1}}) + \dots + X _ {k} (B _ {T} - B _ {t _ {k}}). \\ \end{array}
$$

# Definition: Stochastic Integral for General Processes

Let $ { \mathcal { L } } ^ { 2 } ( [ 0 , T ] )$ be the set of $\{ \mathcal { F } _ { t } : t \geqslant 0 \}$ -adapted processes $f$ such that

$$
\int_ {0} ^ {T} \mathbb {E} [ f ^ {2} (t) ] \mathrm{d} t <   + \infty .
$$

Given $f \in \mathcal { L } ^ { 2 } ( [ 0 , T ] )$ , for any sequence of simple processes $\{ f _ { i } ( t ) \} _ { i \geqslant 1 }$ such that

$$
\lim _ {i \rightarrow \infty} \int_ {0} ^ {T} \mathbb {E} \left[ (f (t) - f _ {i} (t)) ^ {2} \right] \mathrm{d} t = 0,
$$

the sequence of stochastic integrals $\begin{array} { r } { \int _ { 0 } ^ { T } f _ { i } ( t ) \mathrm { d } B _ { t } } \end{array}$ has a unique limit in $ { \mathcal { L } } ^ { 2 } ( [ 0 , T ] )$ . We define

$$
\int_ {0} ^ {T} f (t) \mathrm{d} B _ {t}
$$

as this limit. This limits is independent of the choice of $\{ f _ { i } ( t ) \} _ { i \geqslant 1 }$

# Property

# Example 8.4

For any constant a, we have

$$
\int_ {0} ^ {T} a \mathrm{d} B _ {t} = a B _ {T}.
$$

# Property

# Proposition 8.2

For any two processes f and $g \in \mathcal L ^ { 2 } ( [ 0 , T ] )$ and any two constants a and b, we have

$$
\int_ {0} ^ {T} (a f (t) + b g (t)) \mathrm{d} B _ {t} = a \int_ {0} ^ {T} f (t) \mathrm{d} B _ {t} + b \int_ {0} ^ {T} g (t) \mathrm{d} B _ {t}
$$

# Proposition 8.3

For any process $f \in \mathcal { L } ^ { 2 } ( [ 0 , \infty ) )$ and three constants $t _ { 1 } < t _ { 2 } < t _ { 3 }$ we have

$$
\int_ {t _ {1}} ^ {t _ {2}} f (s) \mathrm{d} B _ {s} + \int_ {t _ {2}} ^ {t _ {3}} f (s) \mathrm{d} B _ {s} = \int_ {t _ {1}} ^ {t _ {3}} f (s) \mathrm{d} B _ {s}.
$$

# Itô Isometry

# Theorem 8.4 (Itô Isometry)

For any processes $f \in { \mathcal { L } } ^ { 2 } ( [ 0 , T ] )$ , we have

$$
\mathbb {E} \left[ \left(\int_ {0} ^ {T} f (t) \mathrm{d} B _ {t}\right) ^ {2} \right] = \int_ {0} ^ {T} \mathbb {E} \left[ f ^ {2} (t) \right] \mathrm{d} t.
$$

# Theorem 8.5

For any two processes f, $g \in \mathcal L ^ { 2 } ( [ 0 , T ] )$ , we have

$$
\mathbb {E} \left[ \int_ {u} ^ {T} f (s) \mathrm{d} B _ {s} \mid \mathcal {F} _ {u} \right] = 0,
$$

$$
\mathbb {E} \left[ \int_ {u} ^ {T} f (s) \mathrm{d} B _ {s} \int_ {u} ^ {T} g (s) \mathrm{d} B _ {s} \Bigg | \mathcal {F} _ {u} \right] = \int_ {u} ^ {T} \mathbb {E} \left[ f (s) g (s) \mid \mathcal {F} _ {u} \right] \mathrm{d} s.
$$

# Properties of Stochastic Integrals

# Theorem 8.6

For any two processes f, $g \in \mathcal L ^ { 2 } ( [ 0 , T ] )$ , we have

$$
\mathbb {E} \left[ \int_ {0} ^ {T} f (s) \mathrm{d} B _ {s} \int_ {0} ^ {T} g (s) \mathrm{d} \overline {{B}} _ {s} \right] = \int_ {0} ^ {T} \mathbb {E} \left[ \rho (s) f (s) g (s) \right] \mathrm{d} s,
$$

where $\{ B _ { t } , t \geqslant 0 \}$ and $\{ \overline { { B } } _ { t } , t \geqslant 0 \}$ are two Brownian motions with a correlation process $\{ \rho _ { t } , t \geqslant 0 \}$ .

# Remark 8.5

This property generalizes the Itô isometry to the case of correlated Brownian motions.

# Definition: Itô Process

We call a process of the form

$$
X _ {t} = X _ {0} + \int_ {0} ^ {t} b (s) \mathrm{d} s + \int_ {0} ^ {t} \sigma (s) \mathrm{d} B _ {s}, \quad t \geqslant 0,
$$

an Itô process in integral form, where the drift b(·) and the volatility $\sigma ( \cdot )$ are $\{ \mathcal { F } _ { t } : t \geqslant 0 \}$ -adapted processes.

The process is often rewritten in its di!erential form:

$$
\mathrm{d} X _ {t} = b (t) \mathrm{d} t + \sigma (t) \mathrm{d} B _ {t}.
$$

# Theorem 8.7

An Itô process is a martingale if and only if its drift is always zero, $i . e . , b ( t ) \equiv 0$ .

# Generalized Brownian Motion

For an Itô process

$$
X _ {t} = X _ {0} + \int_ {0} ^ {t} b (s) \mathrm{d} s + \int_ {0} ^ {t} \sigma (s) \mathrm{d} B _ {s}, \quad t \geqslant 0,
$$

if the drift $b ( \cdot )$ and the volatility $\sigma ( \cdot )$ are both constant, i.e., $b ( \cdot ) \equiv b$ and $\sigma ( \cdot ) \equiv \sigma$ , then

$$
X _ {t} = X _ {0} + b t + \sigma B _ {t},
$$

which is called generalized Brownian motion, Brownian motion with drift, or generalized Wiener process starting at $X _ { 0 }$ , with drift rate b and volatility rate ω.

# Mean

# Theorem 8.8

$$
I f \mathrm{d} X _ {t} = b (t) \mathrm{d} t + \sigma (t) \mathrm{d} B _ {t}. T h e n
$$

$$
\mathrm{d} \left(\mathbb {E} [ X _ {t} ]\right) = \mathbb {E} [ b (t) ] \mathrm{d} t.
$$

# Proof.

$$
X _ {t} = X _ {0} + \int_ {0} ^ {t} b (s) \mathrm{d} s + \int_ {0} ^ {t} \sigma (s) \mathrm{d} B _ {s},
$$

by taking expectation on both sides, we obtain

$$
\begin{array}{l} \mathbb {E} [ X _ {t} ] = \mathbb {E} [ X _ {0} ] + \mathbb {E} \left[ \int_ {0} ^ {t} b (s) \mathrm{d} s \right] + \mathbb {E} \left[ \int_ {0} ^ {t} \sigma (s) \mathrm{d} B _ {s} \right] \\ = \mathbb {E} [ X _ {0} ] + \int_ {0} ^ {t} \mathbb {E} [ b (s) ] \mathrm{d} s. \\ \end{array}
$$

# Quadratic Variation

The quadratic variation process of the Itô process

$$
\mathrm{d} X _ {t} = b (t) \mathrm{d} t + \sigma (t) \mathrm{d} B _ {t},
$$

often denoted by $\langle X \rangle _ { t }$ , is defined as

$$
\langle X \rangle_ {t} = \int_ {0} ^ {t} | \sigma (s) | ^ {2} \mathrm{d} s, \quad t \geqslant 0.
$$

In its di!erential form:

$$
\mathrm{d} \left<   X \right> _ {t} = | \sigma (t) | ^ {2} \mathrm{d} t.
$$

# Exercise 8.6

Show that $\langle B \rangle _ { t } = t$

# Itô’s Lemma for General Itô Process

We say $\varphi ( t , x )$ is smooth if $\varphi _ { t } ( t , x ) , \ \varphi _ { x } ( t , x )$ and $\varphi _ { x x } ( t , x )$ exist and are all continuous.

# Theorem 8.9 (Itô’s Lemma)

Let $\varphi ( t , x )$ be a deterministic smooth function and $X _ { t }$ be an Itô process. Then the process $\varphi ( t , X _ { t } )$ is also an Itô process. Moreover,

$$
\mathrm{d} \varphi (t, X _ {t}) = \varphi_ {t} (t, X _ {t}) \mathrm{d} t + \varphi_ {x} (t, X _ {t}) \mathrm{d} X _ {t} + \frac {1}{2} \varphi_ {x x} (t, X _ {t}) \mathrm{d} \langle X \rangle_ {t}.
$$

# Corollary 8.10

Let $\varphi ( x )$ be a deterministic smooth function and $X _ { t }$ be an Itô process. Then

$$
\mathrm{d} \varphi (X _ {t}) = \varphi_ {x} (X _ {t}) \mathrm{d} X _ {t} + \frac {1}{2} \varphi_ {x x} (X _ {t}) \mathrm{d} \langle X \rangle_ {t}.
$$

# Itô’s Lemma for Brownian Motion

# Corollary 8.11

Let $\varphi ( t , x )$ be a deterministic smooth function. Then

$$
\mathrm{d} \varphi (t, B _ {t}) = \left(\varphi_ {t} (t, B _ {t}) + \frac {1}{2} \varphi_ {x x} (t, B _ {t})\right) \mathrm{d} t + \varphi_ {x} (t, B _ {t}) \mathrm{d} B _ {t}.
$$

# Corollary 8.12

Let $\varphi ( x )$ be a deterministic smooth function. Then

$$
\mathrm{d} \varphi (B _ {t}) = \frac {1}{2} \varphi_ {x x} (B _ {t}) \mathrm{d} t + \varphi_ {x} (B _ {t}) \mathrm{d} B _ {t}.
$$

# Example

# Example 8.5

Show that $\frac { 1 } { 2 } ( B _ { t } ^ { 2 } - t )$ is an Itô process and

$$
\int_ {0} ^ {t} B _ {s} \mathrm{d} B _ {s} = \frac {1}{2} (B _ {t} ^ {2} - t).
$$

# Proof.

We have

$$
\mathrm{d} \varphi (B _ {t}) = \frac {1}{2} \varphi_ {x x} (B _ {t}) \mathrm{d} t + \varphi_ {x} (B _ {t}) \mathrm{d} B _ {t}.
$$

Let $\varphi ( x ) = x ^ { 2 }$ . Then $\varphi _ { x } ( x ) = 2 x$ and $\varphi _ { x x } ( x ) = 2$ , so the above becomes

$$
\mathrm{d} (B _ {t} ^ {2}) = 2 B _ {t} \mathrm{d} B _ {t} + \mathrm{d} t.
$$

Hence

$$
B _ {t} ^ {2} = B _ {0} ^ {2} + \int_ {0} ^ {t} 2 B _ {s} \mathrm{d} B _ {s} + \int_ {0} ^ {t} \mathrm{d} s = 2 \int_ {0} ^ {t} B _ {s} \mathrm{d} B _ {s} + t.
$$

# Stock Price Model

Recall that the continuous-time stock price model is given by

$$
\mathrm{d} S _ {t} = \mu S _ {t} \mathrm{d} t + \sigma S _ {t} \mathrm{d} B _ {t}.
$$

Let $\varphi ( x ) = \log x$ , then

$$
\varphi_ {x} (x) = \frac {1}{x}, \qquad \varphi_ {x x} (x) = - \frac {1}{x ^ {2}}.
$$

It follows from Itô’s Lemma that

$$
\begin{array}{l} \mathrm{d} \varphi (S _ {t}) = \varphi_ {x} (S _ {t}) \mathrm{d} S _ {t} + \frac {1}{2} \varphi_ {x x} (S _ {t}) \mathrm{d} \langle S \rangle_ {t} \\ = \varphi_ {x} (S _ {t}) (\mu S _ {t} \mathrm{d} t + \sigma S _ {t} \mathrm{d} B _ {t}) + \frac {1}{2} \varphi_ {x x} (S _ {t}) (\sigma S _ {t}) ^ {2} \mathrm{d} t \\ = \frac {1}{S _ {t}} (\mu S _ {t} \mathrm{d} t + \sigma S _ {t} \mathrm{d} B _ {t}) - \frac {1}{2} \frac {1}{S _ {t} ^ {2}} (\sigma S _ {t}) ^ {2} \mathrm{d} t \\ = \left(\mu - \frac {1}{2} \sigma^ {2}\right) \mathrm{d} t + \sigma \mathrm{d} B _ {t}. \\ \end{array}
$$

# Geometric Brownian Motion

$$
\mathrm{d} \left(\log S _ {t}\right) = \left(\mu - \frac {1}{2} \sigma^ {2}\right) \mathrm{d} t + \sigma \mathrm{d} B _ {t}
$$

Write it in integral form:

$$
\begin{array}{l} \log S _ {t} = \log S _ {0} + \int_ {0} ^ {t} \left(\mu - \frac {1}{2} \sigma^ {2}\right) \mathrm{d} s + \int_ {0} ^ {t} \sigma \mathrm{d} B _ {s} \\ = \log S _ {0} + \left(\mu - \frac {1}{2} \sigma^ {2}\right) t + \sigma B _ {t}. \\ \end{array}
$$

Now we obtain an explicit expression for $S _ { t }$ :

$$
S _ {t} = S _ {0} e ^ {(\mu - \frac {1}{2} \sigma^ {2}) t + \sigma B _ {t}}
$$

so we call the process $S ( \cdot )$ a geometric Brownian motion (GBM).

# Distribution of Geometric Brownian Motion

From

$$
\log S _ {t} = \log S _ {0} + \left(\mu - \frac {1}{2} \sigma^ {2}\right) t + \sigma B _ {t}
$$

we see that

$$
\log S _ {T} - \log S _ {0} \sim N \left(\left(\mu - \frac {1}{2} \sigma^ {2}\right) T, \sigma^ {2} T\right),
$$

or equivalently,

$$
\log S _ {T} \sim N \left(\log S _ {0} + \left(\mu - \frac {1}{2} \sigma^ {2}\right) T, \sigma^ {2} T\right)
$$

We say $S _ { T }$ follows a log-normal distribution because the logarithm of $S _ { T }$ is normally distributed.

# Covariation Process

The covariation (or cross-variance) process of two Itô processes $X _ { t }$ and $Y _ { t }$ is defined by

$$
\langle X, Y \rangle_ {t} = \frac {1}{4} (\langle X + Y \rangle_ {t} - \langle X - Y \rangle_ {t}).
$$

If $X _ { t }$ and $Y _ { t }$ are given by

$$
\mathrm{d} X _ {t} = b _ {1} (t) \mathrm{d} t + \sigma_ {1} (t) \mathrm{d} B _ {t},
$$

$$
\mathrm{d} Y _ {t} = b _ {2} (t) \mathrm{d} t + \sigma_ {2} (t) \mathrm{d} \overline {{B}} _ {t},
$$

where $\{ B _ { t } , t \geqslant 0 \}$ and $\{ \overline { { B } } _ { t } , t \geqslant 0 \}$ are two Brownian motions with a correlation $\rho _ { t }$ . Then

$$
\langle X, Y \rangle_ {t} = \int_ {0} ^ {t} \rho (s) \sigma_ {1} (s) \sigma_ {2} (s) d s, \quad t \geqslant 0.
$$

If one of $X _ { t }$ or $Y _ { t }$ is deterministic, then $\langle X , Y \rangle _ { t } = 0$ .

# Bivariate Itô’s Lemma

# Theorem 8.13 (Bivariate Itô’s Lemma)

Let $\varphi ( t , x , y )$ be a determinist smooth function and $X _ { t }$ and $Y _ { t }$ be two Itô processes. Then the process $\varphi ( t , X _ { t } , Y _ { t } )$ is also an Itô process. Moreover,

$$
\begin{array}{l} \mathrm{d} \varphi (t, X _ {t}, Y _ {t}) = \varphi_ {t} (t, X _ {t}, Y _ {t}) \mathrm{d} t \\ + \varphi_ {x} (t, X _ {t}, Y _ {t}) \mathrm{d} X _ {t} + \frac {1}{2} \varphi_ {x x} (t, X _ {t}, Y _ {t}) \mathrm{d} \langle X \rangle_ {t} \\ + \varphi_ {y} (t, X _ {t}, Y _ {t}) \mathrm{d} Y _ {t} + \frac {1}{2} \varphi_ {y y} (X _ {t}, Y _ {t}) \mathrm{d} \langle Y \rangle_ {t} \\ + \varphi_ {x y} (t, X _ {t}, Y _ {t}) \mathrm{d} \langle X, Y \rangle_ {t}. \\ \end{array}
$$

# Bivariate Itô’s Lemma

# Example 8.6

For two Itô processes $X _ { t }$ and $Y _ { t }$ , we have

$$
\mathrm{d} (X _ {t} Y _ {t}) = Y _ {t} \mathrm{d} X _ {t} + X _ {t} \mathrm{d} Y _ {t} + \mathrm{d} \langle X, Y \rangle_ {t}.
$$

In particular, if one of $X _ { t }$ or $Y _ { t }$ has no volatility term (i.e., is deterministic), then

$$
\mathrm{d} \left(X _ {t} Y _ {t}\right) = Y _ {t} \mathrm{d} X _ {t} + X _ {t} \mathrm{d} Y _ {t}.
$$