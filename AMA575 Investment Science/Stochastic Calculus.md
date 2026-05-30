# Stochastic Calculus

# Conditional Expectation: Discrete Case

I Recall that for any two events E and F, the conditional probability of E given F is defined, as long as $\mathbb { P } ( F ) > 0$ , by

$$
\mathbb {P} (E | F) = \frac {\mathbb {P} (E \cap F)}{\mathbb {P} (F)}
$$

Hence, if X and Y are discrete random variables, it is natural to define the conditional probability mass function of X given that Y = y by

$$
\begin{array}{l} p _ {X \mid Y} (x \mid y) = \mathbb {P} \left\{X = x \mid Y = y \right\} \\ = \frac {\mathbb {P} \{X = x , Y = y \}}{\mathbb {P} \{Y = y \}} \\ = \frac {p (x , y)}{p _ {Y} (y)} \\ \end{array}
$$

for all values of y such that ${ \mathbb { P } } \left\{ Y = y \right\} = p _ { Y } ( y ) > 0 .$ .

# Conditional Expectation: Discrete Case

I Similarly, the conditional probability distribution function of X given that Y = y is defined, for all y such that ${ \mathbb { P } } \left\{ Y = y \right\} > 0$ , by

$$
\begin{array}{l} F _ {X \mid Y} (x \mid y) = \mathbb {P} \left\{X \leq x \mid Y = y \right\} \\ = \sum_ {a \leq x} p _ {X | Y} (a | y) \\ \end{array}
$$

I Finally, the conditional expectation of X given that Y = y is defined by

$$
\begin{array}{l} \mathbb {E} [ X | Y = y ] = \sum_ {x} x \mathbb {P} \left\{X = x | Y = y \right\} \\ = \sum_ {x} x p _ {X | Y} (x | y) \\ \end{array}
$$

I In general, we define

$$
\mathbb {E} [ X | A ] = \sum_ {x} x \frac {\mathbb {P} (\{X = x \} \cap A)}{\mathbb {P} (A)} = \frac {\mathbb {E} [ X \mathbf {1} _ {A} ]}{\mathbb {P} (A)},
$$

where ${ \mathbf { 1 } } _ { A }$ is the indicator random variable on the event A.

# Conditional Expectation: Discrete Case

I We should take the conditional expectation $\mathbb { E } [ X | Y = y ]$ given the event $\{ Y = y \}$ as a function of the variable y, so we can define $H ( y ) = \mathbb { E } [ X | Y = y ]$ . For different choice of value y, the value of conditional expectation is also different.   
I In general, we can also define conditional expectation given the random variable Y , i.e., E[X |Y ] which is then another random variable. In practice, we can always first compute $H ( y ) = \mathbb { E } [ X | Y = y ]$ , and then $\mathbb { E } [ X | Y ] = H ( Y )$ by replacing y by Y .   
I If X is independent of Y, then the conditional mass function, distribution, and expectation are the same as unconditional ones. So if X is independent of Y, then

$$
p _ {X \mid Y} (x \mid y) = \mathbb {P} \left\{X = x \mid Y = y \right\}
$$

$$
= \mathbb {P} \{X = x \} = p _ {X} (x)
$$

# Conditional Expectation: Discrete Case

I Example: Suppose X and Y are discrete random variables taking values in {1, 2} and

$$
\mathbb {P} (X = 1, Y = 1) = \frac {1}{2}, \quad \mathbb {P} (X = 1, Y = 2) = \frac {1}{1 0},
$$

$$
\mathbb {P} (X = 2, Y = 1) = \frac {1}{1 0}, \quad \mathbb {P} (X = 2, Y = 2) = \frac {3}{1 0}.
$$

Compute E[X |Y = 1].

I Solution: By definition, we have

$$
\mathbb {E} [ X | Y = 1 ] = 1 \mathbb {P} (X = 1 | Y = 1) + 2 \mathbb {P} (X = 2 | Y = 1)
$$

$$
= \frac {\mathbb {P} (X = 1 , Y = 1)}{\mathbb {P} (Y = 1)} + 2 \frac {\mathbb {P} (X = 2 , Y = 1)}{\mathbb {P} (Y = 1)}
$$

$$
= \frac {1 / 2}{3 / 5} + 2 \frac {1 / 1 0}{3 / 5} = \frac {7}{6}.
$$

# Conditional Expectation: Continuous Case

I If X and Y have joint probability density function $f ( x , y )$ , then the conditional probability density function of X given that $\{ Y = y \}$ , is defined for all values of y such that $f _ { Y } ( y ) > 0$ , by

$$
f _ {X \mid Y} (x \mid y) = \frac {f (x , y)}{f _ {Y} (y)}
$$

To motivate this definition, multiply the left side by dx and the right side by $( d x d y ) / d y$ to get

$$
\begin{array}{l} f _ {X \mid Y} (x \mid y) d x = \frac {f (x , y) d x d y}{f _ {Y} (y) d y} \\ \approx \frac {\mathbb {P} \left\{x \leq X \leq x + d x , y \leq Y \leq y + d y \right\}}{\mathbb {P} \left\{y \leq Y \leq y + d y \right\}} \\ = \mathbb {P} \left\{x \leq X \leq x + d x | y \leq Y \leq y + d y \right\} \\ \end{array}
$$

In other words, for small values dx and dy, $f _ { X \mid Y } ( x | y ) d x$ is approximately the conditional probability that X is between x and $x + d x$ given that Y is between y and $y + d y$ .

# Conditional Expectation: Continuous Case

I The conditional expectation of X, given that $\{ Y = y \}$ , is defined for all values of y such that $f _ { Y } ( y ) > 0$ by

$$
\mathbb {E} [ X | Y = y ] = \int_ {- \infty} ^ {\infty} x f _ {X | Y} (x | y) d x
$$

I Similarly, we can define the random variable $\mathbb { E } [ X | Y ]$ and if we define a function $H ( y ) = \mathbb { E } [ X | Y = y ]$ , then $\mathbb { E } [ X | Y ] = H ( Y )$ .   
I Example: Suppose the joint density of X and Y is given by

$$
f (x, y) = \left\{ \begin{array}{l l} 6 x y (2 - x - y), & 0 <   x <   1, 0 <   y <   1 \\ 0, & \text { otherwise } \end{array} \right.
$$

Compute the conditional expectation of X given that Y = y,where $0 < y < 1$ .

# Conditional Expectation: Continuous Case

# I Solution:

$$
\begin{array}{l} f _ {X \mid Y} (x \mid y) = \frac {f (x , y)}{f _ {Y} (y)} \\ = \frac {6 x y (2 - x - y)}{\int_ {0} ^ {1} 6 x y (2 - x - y) d x} \\ = \frac {6 x (2 - x - y)}{4 - 3 y} \\ \end{array}
$$

$$
\begin{array}{l} \mathbb {E} [ X | Y = y ] = \int_ {0} ^ {1} \frac {6 x ^ {2} (2 - x - y) d x}{4 - 3 y} \\ = \frac {(2 - y) 2 - \frac {6}{4}}{4 - 3 y} \\ = \frac {5 - 4 y}{8 - 6 y} \\ \end{array}
$$

# Properties

I Recall that $\mathbb { E } [ X | Y ]$ is itself a random variable. One important property of conditional expectation is the tower property:

$$
\mathbb {E} [ X ] = \mathbb {E} [ \mathbb {E} [ X | Y ] ]. \tag {1}
$$

If Y is a discrete random variable, then Equation (2) states that

$$
\mathbb {E} [ X ] = \sum_ {y} \mathbb {E} [ X | Y = y ] \mathbb {P} \{Y = y \}
$$

while if Y is continuous with density $f _ { Y } ( y )$ , then Equation (2) says that

$$
\mathbb {E} [ X ] = \int_ {- \infty} ^ {\infty} \mathbb {E} [ X | Y = y ] f _ {Y} (y) d y
$$

In general, we have the rule that if $H ( Y ) = \mathbb { E } [ X | Y ]$ , then for any function g ,

$$
\mathbb {E} [ H (Y) g (Y) ] = \mathbb {E} [ X g (Y) ].
$$

# Properties

I Proof (when X and Y are discrete) We must show that

$$
\mathbb {E} [ X ] = \sum_ {y} \mathbb {E} [ X | Y = y ] \mathbb {P} \{Y = y \}
$$

Now the right side of the preceding can be written

$$
\begin{array}{l} \sum_ {y} \mathbb {E} [ X | Y = y ] \mathbb {P} \{Y = y \} = \sum_ {y} \sum_ {x} x \mathbb {P} \{X = x | Y = y \} \mathbb {P} \{Y = y \} \\ = \sum_ {y} \sum_ {x} x \frac {\mathbb {P} \{X = x , Y = y \}}{\mathbb {P} \{Y = y \}} \mathbb {P} \{Y = y \} \\ = \sum_ {y} \sum_ {x} x \mathbb {P} \{X = x, Y = y \} \\ = \sum_ {x} x \sum_ {y} \mathbb {P} \{X = x, Y = y \} \\ = \sum_ {x} x \mathbb {P} \{X = x \} = \mathbb {E} [ X ] \\ \end{array}
$$

Some basic properties of conditional expectations given random variables:

I Linearity: ${ \mathbb E } [ a Y + b Z | X ] = a { \mathbb E } [ Y | X ] + b { \mathbb E } [ Z | X ] .$ .   
I Monotonicity: If we know $Z \leq Y$ , then $\mathbb { E } [ Z | X ] \leq \mathbb { E } [ Y | X ]$ .   
I We have $\mathbb { E } [ c | X ] = c$ for any constant c.   
I If X and Y are independent, then $\mathbb { E } [ Y | X ] = \mathbb { E } [ Y ]$   
I Take out what is known: $\mathbb { E } [ g ( X ) | X ] = g ( X )$ .

# General Conditional Expectation

# Conditional expectation

Let X be a random variable on probability space $( \Omega , P )$ and let $\mathcal { F }$ be a general information set. Then $\mathbb { E } [ X | \mathcal { F } ]$ is an ${ \mathcal { F } } .$ -measurable random variable such that, for any event $F \in { \mathcal { F } }$ ,

$$
\int_ {F} \mathbb {E} [ X | \mathcal {F} ] d P = \int_ {F} X d P.
$$

# Properties

I Linearity: ${ \mathbb E } [ a X + b Y | { \mathcal F } ] = a { \mathbb E } [ X | { \mathcal F } ] + b { \mathbb E } [ Y | { \mathcal F } ]$ .   
I Take out what is known: let X be a random variable and Y be an F-measurable random variable. Then $\mathbb { E } [ X Y | { \mathcal { F } } ] = Y \mathbb { E } [ X | { \mathcal { F } } ]$ . In particular, $\mathbb { E } [ Y | \mathcal { F } ] = Y$ .   
I Independence: if X is independent of $\mathcal { F }$ then $\mathbb { E } [ X | { \mathcal { F } } ] = \mathbb { E } [ X ]$ .   
I The tower properties: if $\mathcal { G } \subset \mathcal { F }$ then

$$
\mathbb {E} [ \mathbb {E} [ X | \mathcal {G} ] | \mathcal {F} ] = \mathbb {E} [ \mathbb {E} [ X | \mathcal {F} ] | \mathcal {G} ] = \mathbb {E} [ X | \mathcal {G} ].
$$

In particular, $\mathbb { E } [ \mathbb { E } [ X | { \mathcal { F } } ] ] = \mathbb { E } [ X ]$ .

# Discrete-time Stochastic Process

I Play the game i times and always bet 1.   
I Denote the outcome of the ith game by $Y _ { j }$   
I Then $Y _ { j }$ is a random variable and $P ( Y _ { i } = 1 ) = P ( Y _ { i } = - 1 ) = 1 / 2$   
I If we start with an initial endowment of $w _ { 0 }$ then our total wealth after the i th game is

$$
w _ {i} = w _ {0} + Y _ {1} + \dots + Y _ {i}. \tag {2}
$$

I Now $\left( w _ { i } \right) _ { i = 1 } ^ { n }$ is an example of a discrete-time stochastic process.

# Information

The information we can get at each stage can be illustrated with the following binary tree.

<table><tr><td> $\mathcal{F}_{0}$ </td><td> $\mathcal{F}_{1}$ </td><td> $\mathcal{F}_{2}$ </td><td> $\mathcal{F}_{3}$ </td></tr><tr><td></td><td></td><td>HH</td><td>HHH</td></tr><tr><td></td><td>H</td><td></td><td>HHT</td></tr><tr><td></td><td></td><td>HT</td><td>HTH</td></tr><tr><td></td><td></td><td></td><td>HTT</td></tr><tr><td> $\{\Omega\}$ </td><td></td><td></td><td>THH</td></tr><tr><td></td><td></td><td>TH</td><td>THT</td></tr><tr><td></td><td>T</td><td></td><td>TTH</td></tr><tr><td></td><td></td><td>TT</td><td>TTT</td></tr></table>

# Filtration for 3 Coin Tosses

I $\mathcal { F } _ { 0 } = \{ \emptyset , \{ \Omega \} \}$

I Then ${ \mathcal { F } } _ { 1 } = 2 ^ { \{ H , T \} }$ , where {H,T} = {{HHH, HHT, HTH, HTT}, {THH,THT,TTH,TTT}}.

I Similarly, after 2 tosses $\mathcal { F } _ { 2 } = 2 ^ { \{ H H , H T , T H , T T \} }$ , where {HH,HT,TH,TT} = {{HHH, HHT}, {HTH, HTT}, {THH,THT}, {TTH,TTT}}.

I All the information are represented by F3 = 2Ω,Ω = {HHH,HHT,HTH,HTT,THH,THT,TTH,TTT}.

# General Filtration

I Let $\Omega$ be a sample space (representing possible states of a chance event).   
I A sequence of information sets $\left( \sigma { \mathrm { - } } \mathsf { a } | \mathsf { g e b r a } \right) \mathcal { F } : \mathcal { F } _ { i } , i = 0 , 1 , \ldots , n$ satisfying

$$
\mathcal {F} _ {0} \subset \mathcal {F} _ {1} \subset \mathcal {F} _ {2} \subset \dots \subset \mathcal {F} _ {n} \tag {3}
$$

is called a filtration.

I If a random variable $W _ { j }$ relies only on information up to time i , for any a, $( w _ { i } < a ) \in \mathcal { F } _ { i }$ , we say that $W _ { j }$ is $\mathcal { F } _ { i ^ { - } } \mathsf { m e a s u r a b l e }$ .   
I We say a stochastic process $X = ( X _ { i } )$ is $\mathcal { F } _ { \sf - a d a p t e d }$ if, for each $i , X _ { i }$ is $\mathcal { F } _ { i ^ { - } } \mathsf { m e a s u r a }$ ble.

# Discrete-time Martingale

I Toss a fair coin is a fair game in the sense that no player has an advantage.   
I In other words, restricted to information at (i − 1)th game, the expectation of $W _ { j }$ and $W _ { I - 1 }$ are the same.   
I Mathematically,

$$
\mathbb {E} [ w _ {i} \mid \mathcal {F} _ {i - 1} ] = w _ {i - 1}. \tag {4}
$$

I A stochastic process satisfying (4) is called a martingale.

# Examples

1. Let $X _ { j }$ be independent with $\mathbb { E } [ X _ { i } ] = 0$ for all i . Then, $S _ { 0 } = 0$ , $S _ { i } = X _ { 1 } + \ldots + X _ { i }$ defines a martingale.   
2. Let $X _ { j }$ be independent with $\mathbb { E } [ X _ { i } ] = 0$ and $\mathsf { V a r } [ X _ { i } ] = \sigma ^ { 2 }$ for all i . Then, $M _ { 0 } = 0 , M _ { i } = S _ { i } ^ { 2 } - i \sigma ^ { 2 }$ gives a martingale.   
3. Let $X _ { j }$ be independent random variables with $\mathbb { E } [ X _ { i } ] = 1$ for all i . Then, $M _ { 0 } = 0$ ,

$$
M _ {i} = X _ {1} \times \dots \times X _ {i}
$$

gives a martingale with respect to $\mathcal { F } _ { j }$ .

# Martingale Transform

Can we take advantage of a fair game by changing the betting size? Let us try to formulate the problem mathematically.

I Let $( M _ { i } ) _ { i = 1 } ^ { n }$ be an $\mathcal { F } _ { j }$ adapted martingale representing this fair game. Denote $M _ { 0 } = 0$ .   
I $A _ { i }$ is the bet for the i th game.   
I $A _ { i }$ has to be $\mathcal { F } _ { i - 1 }$ -measurable called predictable (determined after the (i − 1)th game).   
I At the end of the ith game the player has

$$
w _ {i} = \sum_ {k = 1} ^ {i} A _ {k} (M _ {k} - M _ {k - 1}). \tag {5}
$$

I The new stochastic process $\left( w _ { i } \right) _ { i = 1 } ^ { n }$ is a martingale transform of $( M _ { i } ) _ { i = 0 } ^ { n }$ .

# Martingale Transform

# Martingale Transform Theorem

Let $M _ { i }$ be a martingale and $A _ { i }$ be a predictable process with respect to $\mathcal { F } _ { j }$ . Then the martingale transform $\begin{array} { r } { w _ { i } = \sum _ { k = 1 } ^ { i } A _ { k } ( M _ { k } - M _ { k - 1 } ) } \end{array}$ is also a martingale.

Proof.

$$
\mathbb {E} [ w _ {i} - w _ {i - 1} \mid \mathcal {F} _ {i - 1} ] = \mathbb {E} [ A _ {i} (M _ {i} - M _ {i - 1}) \mid \mathcal {F} _ {i - 1} ]
$$

$$
= A _ {i} \mathbb {E} [ M _ {i} - M _ {i - 1} \mid \mathcal {F} _ {i - 1} ] = 0.
$$

# Continuous-time Stochastic Process

I Stochastic process: Let $( \Omega , { \mathcal { F } } , P )$ be a probability space and let $[ 0 , T ]$ be an interval. $( X _ { t } ) , t \in [ 0 , T ]$ is a stochastic process if for every $t , X _ { t }$ is a random variable on $( \Omega , { \mathcal { F } } , P )$ .   
I For each fixed $\omega \in \Omega$ ,

$$
t \to X _ {t} (\omega)
$$

is called a path of the stochastic process $( X _ { t } )$

I A stochastic process $( X _ { t } )$ can also be viewed as a two variable function

$$
(t, \omega) \rightarrow X _ {t} (\omega) = X (t, \omega).
$$

# General Filtration

I Let $( \Omega , { \mathcal { F } } , P )$ be a probability space and let $[ 0 , T ]$ be an interval. Then $( \mathcal { F } _ { t } ) , t \in [ 0 , T ]$ is a filtration if for every t, $\mathcal { F } _ { t } \subset \mathcal { F }$ is a σ-algebra and, for any $s < t$ ,

$$
\mathcal {F} _ {s} \subset \mathcal {F} _ {t}.
$$

Again, $\mathcal { F } _ { t }$ represents the information set up to time t.

I We say a stochastic process $( X _ { t } )$ is $( \mathcal { F } _ { t } )$ -adapted provided that, for every $t \in [ 0 , T ] , X _ { t }$ is $\mathcal { F } _ { t } .$ -measurable.   
I Define $\mathcal { F } _ { t } = \sigma ( \{ X _ { s } ^ { - 1 } ( F ) : s \in [ 0 , t ] , F \in \mathcal { B } \} )$ , where $\boldsymbol { B }$ is all the Borel sets in $R ^ { n }$ . Then $( \mathcal { F } _ { t } )$ is the filtration generated by the stochastic process $X _ { t }$ .

# 1-dimensional Brownian motion (Wiener)

A stochastic process $\{ B _ { t } : t \in [ 0 , T ) \}$ is called a Brownian motion starting from x if

1. $\begin{array} { r } { B _ { 0 } = x , } \end{array}$   
2. for $0 \leq t _ { 1 } < t _ { 2 } < . . . < t _ { k } \leq T$ , the random variables

$$
B _ {t _ {2}} - B _ {t _ {1}}, B _ {t _ {3}} - B _ {t _ {2}}, \ldots , B _ {t _ {k}} - B _ {t _ {k - 1}}
$$

are independent,

3. for $0 \leq s \leq t \leq T , B _ { t } - B _ { s }$ has Gaussian distribution with mean 0 and variance t − s,   
4. for $\omega$ in a set of probability one, the path $B _ { t } ( \omega )$ is continuous.

# Multi-dimensional Brownian motion

# Multi-dimensional Brownian motion

A vector stochastic process $\{ B _ { t } : t \in [ 0 , T ] \}$ in $R ^ { n }$ is called a Brownian motion starting from $x = ( x ^ { 1 } , x ^ { 2 } , \ldots , x ^ { n } )$ if $B _ { t } = \left( B _ { t } ^ { 1 } , B _ { t } ^ { 2 } , \ldots , B _ { t } ^ { n } \right)$ where $B _ { t } ^ { i } , i = 1 , 2 , \ldots , n$ are independent 1-dimensional Brownian motion starting from $x ^ { i }$ .

If $x = 0$ , we say $\left( B _ { t } \right)$ is a standard Brownian motion. A Brownian motion starting from x can be viewed as a standard Brownian motion shifted by x.

# Covariance of a Brownian motion

# Covariance of a Brownian motion

Let $( X _ { t } )$ be a Gaussian process with continuous paths and $\mathbb { E } [ X _ { t } ] = 0$ for all $t \in [ 0 , T ]$ . Then $( X _ { t } )$ is a standard Brownian motion if and only if $\mathrm { c o v } ( X _ { s } , X _ { t } ) = s \wedge t$ .

For a standard 1-dimensional Brownian motion $\left( B _ { t } \right)$ , we can also use its density function to directly calculate higher moments

$$
\mathbb {E} [ (B _ {t} - B _ {s}) ^ {3} ] = 0,
$$

and

$$
\mathbb {E} [ (B _ {t} - B _ {s}) ^ {4} ] = 3 (t - s) ^ {2}.
$$

# Stochastic Integral

I The stochastic integral can be viewed as a continuous version of the martingale transform.   
I This is one of the key tools in quantitative finance.   
I We focus on some main idea rather than technical details.

# Integrable function space V

I Let $B ( t )$ be a one dimensional standard Brownian motion.   
I Let ${ \mathcal { F } } _ { t } : = \sigma \{ B ^ { - 1 } ( s ) : s \leq t \}$ be the filtration generated by the Brownian motion.   
I We define the stochastic integral (Itˆo integral) for the class of functions V from $[ 0 , \infty ) \times \Omega \to R$ satisfying:

(i) $f ( t , \omega )$ is $B \times { \mathcal { F } }$ measurable;   
(ii) for fixed t, $f ( t , \omega )$ is $\mathcal { F } _ { t }$ adapted;   
(iii) $\begin{array} { r } { \mathbb { E } [ \int _ { s } ^ { T } f ( t , \omega ) ^ { 2 } d t ] < \infty . } \end{array}$

# Itˆo Integral for Elementary Functions

I We use the idea of approximation by elementary functions.   
I They are of the form

$$
\phi (t, \omega) = \sum_ {j} e _ {j} (\omega) \chi_ {[ t _ {j}, t _ {j + 1})} (t),
$$

I where $e _ { j }$ is $\mathcal { F } _ { t _ { j } }$ adapted and $\chi _ { [ t _ { j } , t _ { j + 1 } ) } ( t ) = 1 , t \in [ t _ { j } , t _ { j + 1 } )$ and 0 otherwise.   
I For an elementary function $\phi$ we define

$$
\int_ {S} ^ {T} \phi (t, \omega) d B (t) = \sum_ {j} e _ {j} (\omega) (B (t _ {j + 1}) - B (t _ {j})).
$$

I This is a martingale transform.

# Approximating V

I From the measure and integration theory we know that for any function $f \in \nu$ there exists a sequence of elementary functions $\phi _ { n }$ such that

$$
\mathbb {E} [ \int_ {S} ^ {T} [ f (t, \omega) - \phi_ {n} (t, \omega) ] ^ {2} d t ] \to 0, \text {   as   } n \to \infty . \tag {6}
$$

I The Itˆo integration for f in V is defined by

$$
\int_ {S} ^ {T} f (t, \omega) d B (t) = \lim _ {n \rightarrow \infty} \int_ {S} ^ {T} \phi_ {n} (t, \omega) d B (t), a. s.
$$

where $\phi _ { n }$ that satisfies (6).

# Properties

I Itˆo isometry: Let $\phi \in \mathcal V$ be an elementary function. Then

$$
\mathbb {E} [ (\int_ {0} ^ {T} \phi (t, \omega) d B (t)) ^ {2} ] = \mathbb {E} [ \int_ {0} ^ {T} \phi^ {2} (t, \omega) d t ].
$$

I R T fdB(t) = R U fdB(t) + R T fdB(t).   
I $\begin{array} { r } { \int _ { S } ^ { T } ( a f + b g ) d B ( t ) = a \int _ { S } ^ { T } f d B ( t ) + b \int _ { S } ^ { T } g d B ( t ) . } \end{array}$   
I $\begin{array} { r } { \int _ { S } ^ { T } \ d t d B ( t ) } \end{array}$ is $\mathcal { F } _ { T }$ measurable.   
I $\begin{array} { r } { \mathbb { E } [ \int _ { S } ^ { T } f d B ( t ) ] = 0 . } \end{array}$

# Continuous-time Martingale

# Definition of continuous martingale

A stochastic process $M _ { t }$ is a martingale with respect to the filtration $\mathcal { F } _ { t }$ on probability space $( \Omega , { \mathcal { F } } , P )$ if

(i) $M _ { t }$ is $\mathcal { F } _ { t }$ measurable,

(ii) $\mathbb { E } [ | M _ { t } | ] < \infty$ , and

(iii) $\mathbb { E } [ M _ { s } | \mathcal { F } _ { t } ] = M _ { t }$ , for $s > t$

Here the expectation is with respect to probability $P _ { - }$ .

# Examples

# Brownian motion is a martingale

Brownian motion B(t) on R is a martingale with respect to the filtration $\mathcal { F } _ { t } = \sigma ( \{ B ( s ) : s \leq t \} )$ .

I (i) follows from the definition of $\mathcal { F } _ { t }$ .   
I (ii) can be derived from Jensen’s inequality:

$$
\mathbb {E} [ | B (t) | ] ^ {2} \leq \mathbb {E} [ B (t) ^ {2} ] \leq t <   T <   \infty .
$$

I (iii) is due to the independence of the increment of $B ( s ) - B ( t )$ and $B ( t ) = B ( t ) - B ( 0 )$ , which implies that, for $s > t$ ,

$$
\mathbb {E} [ B (s) | \mathcal {F} _ {t} ] = \mathbb {E} [ B (s) - B (t) + B (t) | \mathcal {F} _ {t} ]
$$

$$
= \mathbb {E} [ B (s) - B (t) ] + \mathbb {E} [ B (t) | \mathcal {F} _ {t} ] = B (t)
$$

# Stochastic Integrals as Martingales

# Theorem

For $\begin{array} { r } { f \in \mathscr { V } , M _ { t } = \int _ { 0 } ^ { t } f ( s , \omega ) d B ( s ) } \end{array}$ is a martingale.

I The proof of $\begin{array} { r } { M _ { t } = \int _ { 0 } ^ { t } f ( s , \omega ) d B ( s ) } \end{array}$ is a martingale depend on discrete approximation.   
I Intuitively, this is the limit of a discrete martingale derived from a martingale transform of a discrete version of B(t).

# Multi-dimensional Case

Let $B = \left( B _ { 1 } , B _ { 2 } , \ldots , B _ { n } \right)$ be an n-dimensional Brownian motion and $v = \left( v _ { i j } \right)$ be an $m \times n$ matrix function. A vector form of the Itˆo integration $\int _ { S } ^ { T } v d B ( t )$ is defined component-wise: the ith component is

$$
\sum_ {j = 1} ^ {n} \int_ {S} ^ {T} v _ {i j} (t, \omega) d B _ {j} (t, \omega).
$$

# Itˆo Formula

# Itˆo formula

Let $f ( t , x ) \in C ^ { 2 }$ and let $B _ { t }$ be an one dimensional Brownian motion. Then

$$
d f (t, B _ {t}) = f _ {t} (t, B _ {t}) d t + f _ {x} (t, B _ {t}) d B _ {t} + \frac {1}{2} f _ {x x} (t, B _ {t}) d t. \tag {7}
$$

I We can also write the integral form as

$$
f (t, B _ {t}) = f (0, 0) + \int_ {0} ^ {t} f _ {t} (s, B _ {s}) d s \tag {8}
$$

$$
+ \int_ {0} ^ {t} f _ {x} (s, B _ {s}) d B _ {s} + \frac {1}{2} \int_ {0} ^ {t} f _ {x x} (t, B _ {t}) d t.
$$

I Formula (7) looks like an usual chain rule except for the last term.

# Heuristic Explanation

I We know that $\begin{array} { r } { f ( t , B _ { t } ) - f ( 0 , 0 ) = \int _ { 0 } ^ { t } d f ( t , B _ { t } ) } \end{array}$ .   
I Expand $d f ( t , B _ { t } )$ using the Taylor’s expansion.   
I Since terms of order $o ( d t )$ will vanish in the integration process, we only need to do this up to the second order.   
I That gives us

$$
\begin{array}{l} {d f (t, B _ {t})} = {f _ {t} (t, B _ {t}) d t + f _ {x} (t, B _ {t}) d B _ {t} + \frac {1}{2} f _ {x x} (t, B _ {t}) d B _ {t} ^ {2}} \\ + \frac {1}{2} f _ {t t} (t, B _ {t}) d t ^ {2} + f _ {t x} (t, B _ {t}) d t d B _ {t}. \\ \end{array}
$$

I Note that $d t ^ { 2 }$ and $d t d B _ { t }$ are $o ( d t )$ , the last two terms can be omitted and we have

# Heuristic Explanation

I

$$
d f (t, B _ {t}) = f _ {t} (t, B _ {t}) d t + f _ {x} (t, B _ {t}) d B _ {t} + \frac {1}{2} f _ {x x} (t, B _ {t}) d B _ {t} ^ {2}.
$$

I By the property of the Brownian motion, we have $\mathbb { E } [ d B _ { t } ^ { 2 } ] = d t$ and

$$
\mathbb {E} [ (d B _ {t} ^ {2} - d t) ^ {2} ] = \mathbb {E} [ d B _ {t} ^ {4} ] - 2 \mathbb {E} [ d B _ {t} ^ {2} ] d t + d t ^ {2} = 2 d t ^ {2}.
$$

I Thus we can replace $d B _ { t } ^ { 2 }$ by dt.   
I That is the Itˆo’s formula

$$
d f = f _ {t} d t + f _ {x} d B _ {t} + \frac {1}{2} f _ {x x} d t.
$$

# Itˆo Processes

Let $B _ { t }$ be a 1-dim Brownian motion with respect to filtration $\mathcal { H } _ { t }$ on $( \Omega , { \mathcal { F } } , P )$ . Then

$$
X _ {t} = X _ {0} + \int_ {0} ^ {t} u (s, \omega) d s + \int_ {0} ^ {t} v (s, \omega) d B _ {s}
$$

is called a (1-dim) Itˆo processes if u, v are $\mathcal { H } _ { t }$ adapted,

$$
P \left[ \int_ {0} ^ {t} v (s, \omega) ^ {2} d s <   \infty \text {for all} t \geq 0 \right] = 1
$$

and

$$
P \left[ \int_ {0} ^ {t} | u (s, \omega) | d s <   \infty \mathrm{forall} t \geq 0 \right] = 1.
$$

# Itˆo Processes

I We can write it as   
I Here u indicating drift and v indicating magnitude of the variation of the random part.   
I Example: Let $X _ { t } = B _ { t } ^ { 2 }$ . Then

$$
d X _ {t} = u d t + v d B _ {t}.
$$

$$
d X _ {t} = d t + 2 B _ {t} d B _ {t}.
$$

Is this a Itˆo process?

The heuristic argument lead us to the following simple rule in handling the differential term arising in the Taylor expansion of a function of the Itˆo process usually called box algebra.

<table><tr><td></td><td> $dt$ </td><td> $dB_{t}$ </td></tr><tr><td> $dt$ </td><td>0</td><td>0</td></tr><tr><td> $dB_{t}$ </td><td>0</td><td> $dt$ </td></tr></table>

# General Itˆo Formula

# General Itˆo formula

Let $f ( t , x ) \in C ^ { 2 }$ and let $X _ { t }$ be an Itˆo process. Then

$$
d f (t, X _ {t}) = f _ {t} (t, X _ {t}) d t + f _ {x} (t, X _ {t}) d X _ {t} + \frac {1}{2} f _ {x x} (t, X _ {t}) (d X _ {t}) ^ {2}.
$$

I For example, if $X _ { t } = \mu t + \sigma B _ { t }$ then $d X _ { t } = \mu d t + \sigma d B _ { t }$ . Using the box algebra we have

$$
\begin{array}{l} {d f (t, X _ {t})} = {f _ {t} d t + f _ {x} d X _ {t} + \frac {1}{2} f _ {x x} d X _ {t} ^ {2}} \\ = f _ {t} d t + \mu f _ {x} d t + \sigma f _ {x} d B _ {t} + \frac {1}{2} \sigma^ {2} f _ {x x} d t \\ \end{array}
$$

# More Examples

I Applying the Itˆo formula to $f ( x ) = x ^ { 2 }$ we have

$$
\int_ {0} ^ {t} B _ {s} d B _ {s} = \frac {1}{2} (B _ {t} ^ {2} - t).
$$

I Letting f (t, x ) = tx we have

$$
t B _ {t} = \int_ {0} ^ {t} B _ {s} d s + \int_ {0} ^ {t} s d B _ {s}
$$

or

$$
\int_ {0} ^ {t} s d B _ {s} = t B _ {t} - \int_ {0} ^ {t} B _ {s} d s.
$$

# Integration by Parts

The pattern in handling $f ( x ) = x ^ { 2 }$ holds in more general setting

# Integration by parts

Let $g ( s )$ be a continuous function with bounded variation with respect to $s \in [ 0 , t ]$ . Then

$$
\int_ {0} ^ {t} g (s) d B _ {s} = g (t) B _ {t} - \int_ {0} ^ {t} g ^ {\prime} (s) B _ {s} d s.
$$

Proof. Applying the Itˆo formula to $\textstyle f ( t , x ) = g ( t ) x$ .

# Multi-dimensional Case

I Let $X _ { t } = ( X _ { t } ^ { 1 } , \ldots , X _ { t } ^ { n } )$ be an n-dimensional Itˆo process satisfying

$$
d X _ {t} = u d t + v d B _ {t},
$$

where u is an n-dimensional vector, v an $n \times m$ matrix and $B _ { t }$ an n-dimensional Brownian motion.

I We require the components of u and v satisfy similar conditions in define the 1-dim Itˆo processes.   
I Suppose that $g ( t , x ) : [ 0 , \infty ) \times R ^ { n }  R ^ { p }$ has continuous second order partial derivatives. Then, for $Y _ { t } = g ( t , X _ { t } )$ ,

$$
d Y _ {t} ^ {k} = \frac {\partial g _ {k}}{d t} d t + \sum_ {i = 1} ^ {n} \frac {\partial g _ {k}}{\partial x _ {i}} d X _ {t} ^ {i} + \frac {1}{2} \sum_ {i, j = 1} ^ {n} \frac {\partial^ {2} g _ {k}}{\partial x _ {i} \partial x _ {j}} d X _ {t} ^ {i} d X _ {t} ^ {j}. \tag {9}
$$

# Multi-dimensional Case

I Let $X _ { t } , Y _ { t }$ be Itˆo processes.   
I Applying the Itˆo formula to $f ( X _ { t } , Y _ { t } ) = X _ { t } Y _ { t }$ we have

$$
d (X _ {t} Y _ {t}) = X _ {t} d Y _ {t} + Y _ {t} d X _ {t} + d X _ {t} d Y _ {t}.
$$

I The integral form in the following general integration by parts formula

$$
\int_ {0} ^ {t} X _ {s} d Y _ {s} = X _ {t} Y _ {t} - X _ {0} Y _ {0} - \int_ {0} ^ {t} Y _ {s} d X _ {s} - \int_ {0} ^ {t} d X _ {s} d Y _ {s}.
$$

# Multi-dimensional Box Algebra

<table><tr><td></td><td> $dt$ </td><td> $dB_{t}^{1}$ </td><td> $dB_{t}^{2}$ </td><td>...</td><td> $dB_{t}^{n}$ </td></tr><tr><td> $dt$ </td><td>0</td><td>0</td><td>0</td><td>...</td><td>0</td></tr><tr><td> $dB_{t}^{1}$ </td><td>0</td><td> $dt$ </td><td>0</td><td>...</td><td>0</td></tr><tr><td> $dB_{t}^{2}$ </td><td>0</td><td>0</td><td> $dt$ </td><td>...</td><td>0</td></tr><tr><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td></tr><tr><td> $dB_{t}^{n}$ </td><td>0</td><td>0</td><td>0</td><td>...</td><td> $dt$ </td></tr></table>

# Example

Let $R ( t , \omega ) = | B ( t , \omega ) |$ | where $B ( t , \omega ) = ( B ^ { 1 } ( t , \omega ) , \ldots , B ^ { n } ( t , \omega ) )$ is an n-dimensional Brownian motion $\left( n > 2 \right)$ . Then

$$
d R = \sum_ {i = 1} ^ {n} \frac {B _ {i}}{R} d B ^ {i} (t) + \frac {n - 1}{2 R} d t.
$$

# Martingale Representation

# Martingale representation

Let $B _ { t }$ be an n-dimensional Brownian motion generating filtration $\mathcal { F } _ { t } ^ { n }$ . Suppose that $M _ { t }$ is an $\mathcal { F } _ { t } ^ { n }$ martingale with respect to probability measure $P$ and that $M _ { t } \in L ^ { 2 } ( P )$ for all $t \geq 0$ . Then there exists a unique stochastic process $v \in \mathcal { V } ^ { n }$ such that

$$
M _ {t} = \mathbb {E} [ M _ {0} ] + \int_ {0} ^ {t} v d B _ {s}.
$$

# Stochastic Differential Equation

I This lecture focus on the Stochastic Differential Equations.   
I We focus on SDE of the form

$$
d X _ {t} = b (t, X _ {t}) d t + \sigma (t, X _ {t}) d B _ {t}. \tag {10}
$$

I This is the central topic of our course and most application problems are modeled by such equations.

# Stochastic Differential Equation

I A simple model for stock price movement is

$$
d S _ {t} = \mu S _ {t} d t + \sigma S _ {t} d B _ {t}. \tag {11}
$$

I Here $S _ { t }$ is a random process representing the stock price with current pricing $S _ { 0 }$ .   
I Coefficient $\mu$ signifies a growth rate believes to be determined by fundamentals and   
I $\sigma$ perturbation due to various complicating factors.

# Stochastic Differential Equation

I We may guess a solution of the form $S _ { t } = f ( t , B _ { t } )$ .   
I Using the Itˆo formula and (11) we have

$$
f _ {t} d t + f _ {x} d B _ {t} + \frac {1}{2} f _ {x x} d t = \mu f d t + \sigma f d B _ {t}.
$$

I Thus,

$$
f _ {x} = \sigma f \tag {12}
$$

and

$$
f _ {t} + \frac {1}{2} f _ {x x} = f \tag {13}
$$

# Stochastic Differential Equation

I From (12) we have $\begin{array} { r } { f ( t , x ) = \exp ( \sigma x + g ( t ) ) } \end{array}$   
I substitute into (13) we have $\begin{array} { r } { f ( t , x ) = C \mathrm { e x p } ( ( \mu - \frac { 1 } { 2 } \sigma ^ { 2 } ) t + \sigma x ) } \end{array}$ .   
I It follows that

$$
S _ {t} = S _ {0} \mathrm{exp} ((\mu - \frac {1}{2} \sigma^ {2}) t + \sigma B _ {t}).
$$

# Geometric Brownian motion

I The stochastic process

$$
S _ {t} = S _ {0} \mathrm{exp} ((\mu - \frac {1}{2} \sigma^ {2}) t + \sigma B _ {t}).
$$

is called a geometric Brownian motion.

Intuitively, this tells us that the compound growth rate of the price is a Brownian motion with a ‘drift’.   
I Note that $\mathbb { E } [ S _ { t } ] = S _ { 0 } \mathrm { e x p } ( \mu t )$ .