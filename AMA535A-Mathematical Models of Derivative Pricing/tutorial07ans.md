# Tutorial Seven

1. Suppose the price of a non-dividend-paying stock at time 0 is 100. The annal volatility of the stock is 30%. The annal interest rate is 12% with continuous compounding. Use a four-step binomial tree model with equal step to price the American option maturing in one-year written on the stock with the payo! function

$$
g (S) = 1 0 * (1 1 - \sqrt {S}) ^ {+}.
$$

(a) Find the risk-neutral probability $p .$   
(b) Find the price of the option.   
(c) Find the probability to early exercise in the risk-neutral world.

# Solution.

(a) We have $\sigma = 3 0 \%$ , !t = 1/4, r = 12%, $u = e ^ { \sigma { \sqrt { \Delta t } } } = 1 . 1 6 1 8 4$ and $d = 1 / u =$ 0.8607. The risk-neutral probability is

$$
p = \frac {e ^ {r \Delta t} - d}{u - d} = \frac {e ^ {12\% * 1 / 4} - 0 . 8 6 0 7}{1 . 1 6 1 8 4 - 0 . 8 6 0 7} = 56.37 \%.
$$

(b) The stock prices will be

$$
\begin{array}{l} S _ {u} = S u = 1 1 6. 1 8 4, \quad S _ {d} = S d = 8 6. 0 7, \\ S _ {u ^ {2}} = S u ^ {2} = 1 3 4. 9 8 7, \quad S _ {d ^ {2}} = S d ^ {2} = 7 4. 0 8, \\ S _ {u ^ {3}} = S u ^ {3} = 1 5 6. 8 3, \quad S _ {d ^ {3}} = S d ^ {3} = 6 3. 7 6, \\ S _ {u ^ {4}} = S u ^ {4} = 1 8 2. 2 1, \quad S _ {d ^ {4}} = S d ^ {4} = 5 4. 8 7. \\ \end{array}
$$

The exercise payo!s are

$$
g (S) = 1 0, \quad g (S u) = 2. 2 1, \quad g (S u ^ {2}) = 0, \quad g (S u ^ {3}) = 0, \quad g (S u ^ {4}) = 0,
$$

$$
g (S d) = 1 7. 2 3, \quad g (S d ^ {2}) = 2 3. 9 3, \quad g (S d ^ {3}) = 3 0. 1 5, \quad g (S d ^ {4}) = 3 5. 9 3.
$$

The option prices at maturity will be

$$
\begin{array}{l} f _ {u ^ {4}} = g (S u ^ {4}) = 0, \\ f _ {u ^ {3} d} = g (S u ^ {3} d) = g (S u ^ {2}) = 0, \\ f _ {u ^ {2} d ^ {2}} = g (S u ^ {2} d ^ {2}) = g (S) = 1 0. \\ f _ {u d ^ {3}} = g (S u d ^ {3}) = g (S d ^ {2}) = 2 3. 9 3. \\ f _ {d ^ {4}} = g \left(S d ^ {4}\right) = 3 5. 9 3. \\ \end{array}
$$

Let $\alpha = e ^ { - r \Delta t } p = 0 . 5 4 7 0$ and $\beta = e ^ { - r \Delta t } ( 1 - p ) = 0 . 4 2 3 4$ . Therefore,

$$
\begin{array}{l} f _ {u ^ {3}} = \max \{g (S u ^ {3}), \alpha * f _ {u ^ {4}} + \beta * f _ {u ^ {3} d} \} \\ = \max \{0, 0. 5 4 7 0 * 0 + 0. 4 2 3 4 * 0 \} = 0, \\ \end{array}
$$

$$
f _ {u ^ {2} d} = \max \{g (S u ^ {2} d), \alpha * f _ {u ^ {3} d} + \beta * f _ {u ^ {2} d ^ {2}} \}
$$

$$
= \max \{2. 2 1, 0. 5 4 7 0 * 0 + 0. 4 2 3 4 * 1 0 \} = 4. 2 3 4,
$$

$$
f _ {u d ^ {2}} = \max \{g (S u d ^ {2}), \alpha * f _ {u ^ {2} d ^ {2}} + \beta * f _ {u d ^ {3}} \}
$$

$$
= \max \{1 7. 2 3, 0. 5 4 7 0 * 1 0 + 0. 4 2 3 4 * 2 3. 9 3 \} = 1 7. 2 3, \quad \text {early}
$$

$$
\begin{array}{l} f _ {d ^ {3}} = \max \left\{g \left(S d ^ {3}\right), \alpha * f _ {u d ^ {3}} + \beta * f _ {d ^ {4}} \right\} \\ = \max \{3 0. 1 5, 0. 5 4 7 0 * 2 3. 9 3 + 0. 4 2 3 4 * 3 5. 9 3 \} = 3 0. 1 5, \quad \text {early} \\ \end{array}
$$

$$
f _ {u ^ {2}} = \max \{g (S u ^ {2}), \alpha * f _ {u ^ {3}} + \beta * f _ {u ^ {2} d} \}
$$

$$
= \max \{0, 0. 5 4 7 0 * 0 + 0. 4 2 3 4 * 4. 2 3 4 \} = 1. 7 9 3,
$$

$$
\begin{array}{l} f _ {u d} = \max \left\{g (S u d), \alpha * f _ {u ^ {2} d} + \beta * f _ {u d ^ {2}} \right\} \\ = \max \{1 0, 0. 5 4 7 0 * 4. 2 3 4 + 0. 4 2 3 4 * 1 7. 2 3 \} = 1 0, \quad \text {early} \\ \end{array}
$$

$$
\begin{array}{l} f _ {d ^ {2}} = \max \left\{g \left(S d ^ {2}\right), \alpha * f _ {u d ^ {2}} + \beta * f _ {d ^ {3}} \right\} \\ = \max \{2 3. 9 3, 0. 5 4 7 0 * 1 7. 2 3 + 0. 4 2 3 4 * 3 0. 1 5 \} = 2 3. 9 3, \quad \text {early} \\ \end{array}
$$

$$
\begin{array}{l} f _ {u} = \max \left\{g (S u), \alpha * f _ {u ^ {2}} + \beta * f _ {u d} \right\} \\ = \max \{2. 2 1, 0. 5 4 7 0 * 1. 7 9 3 + 0. 4 2 3 4 * 1 0 \} = 5. 2 1, \\ \end{array}
$$

$$
\begin{array}{l} f _ {d} = \max \left\{g (S d), \alpha * f _ {u d} + \beta * f _ {d ^ {2}} \right\} \\ = \max \{1 7. 2 3, 0. 5 4 7 0 * 1 0 + 0. 4 2 3 4 * 2 3. 9 3 \} = 1 7. 2 3, \quad \text {early} \\ \end{array}
$$

$$
\begin{array}{l} f = \max \left\{g (S), \alpha * f _ {u} + \beta * f _ {d} \right\} \\ = \max \{1 0, 0. 5 4 7 0 * 5. 2 1 + 0. 4 2 3 4 * 1 7. 2 3 \} = 1 0. 1 5. \\ \end{array}
$$

(c) One should early exercise when the stock price goes up in the first step, or up in the first step and down in the second step, so the probability is $\textstyle 1 - p + p ( 1 - p ) =$ $1 - p ^ { 2 } = 6 8 . 2 2 \%$ .

2. Find the value of $\mathbf { V a r } ( 3 B _ { 1 } + 2 B _ { 2 } + 4 B _ { 4 } )$ .

# Solution.

Let $Z _ { 1 } = B _ { 4 } - B _ { 2 }$ and $Z _ { 2 } = B _ { 2 } - B _ { 1 }$ . Then $B _ { 1 } , Z _ { 1 }$ , and $Z _ { 2 }$ are independent. Note $B _ { 1 } \sim N ( 0 , 1 ) , Z _ { 1 } \sim N ( 0 , 2 ) , Z _ { 2 } \sim N ( 0 , 1 )$ , so

$$
\begin{array}{l} \operatorname{Var} \left(3 B _ {1} + 2 B _ {2} + 4 B _ {4}\right) = \operatorname{Var} \left(4 Z _ {1} + 6 Z _ {2} + 9 B _ {1}\right) \\ = \operatorname{Var} \left(4 Z _ {1}\right) + \operatorname{Var} \left(6 Z _ {2}\right) + \operatorname{Var} \left(9 B _ {1}\right) \\ = 1 6 \operatorname{Var} \left(Z _ {1}\right) + 3 6 \operatorname{Var} \left(Z _ {2}\right) + 8 1 \operatorname{Var} \left(B _ {1}\right) \\ = 1 6 * 2 + 3 6 * 1 + 8 1 * 1 = 1 4 9. \\ \end{array}
$$

3. Find the value of ${ \bf E } [ B _ { 1 } ^ { 2 } B _ { 2 } B _ { 5 } ]$ .

# Solution.

Note $B _ { 5 } - B _ { 2 } \sim N ( 0 , 3 )$ , so we have

$$
\begin{array}{l} \mathbf {E} \left[ B _ {1} ^ {2} B _ {2} B _ {5} \right] = \mathbf {E} \left[ B _ {1} ^ {2} B _ {2} ((B _ {5} - B _ {2}) + B _ {2}) \right] \\ = \mathbf {E} \left[ B _ {1} ^ {2} B _ {2} (B _ {5} - B _ {2}) \right] + \mathbf {E} \left[ B _ {1} ^ {2} B _ {2} ^ {2} \right] \\ = \mathbf {E} \left[ B _ {1} ^ {2} B _ {2} \right] \mathbf {E} \left[ \left(B _ {5} - B _ {2}\right) \right] + \mathbf {E} \left[ B _ {1} ^ {2} B _ {2} ^ {2} \right] \\ = \mathbf {E} \left[ B _ {1} ^ {2} B _ {2} ^ {2} \right]. \\ \end{array}
$$

Let $Z _ { 1 } = B _ { 2 } - B _ { 1 }$ Then $B _ { 1 }$ and $Z _ { 1 }$ are independent. Note $Z _ { 1 } \ \sim \ N ( 0 , 1 )$ and $B _ { 1 } \sim N ( 0 , 1 )$ , so we have

$$
\begin{array}{l} \mathbf {E} \left[ B _ {1} ^ {2} B _ {2} B _ {5} \right] = \mathbf {E} \left[ B _ {1} ^ {2} B _ {2} ^ {2} \right] = \mathbf {E} \left[ B _ {1} ^ {2} (Z _ {1} + B _ {1}) ^ {2} \right] \\ = \mathbf {E} \left[ B _ {1} ^ {2} (Z _ {1} ^ {2} + 2 Z _ {1} B _ {1} + B _ {1} ^ {2}) \right] \\ = \mathbf {E} \left[ B _ {1} ^ {2} Z _ {1} ^ {2} \right] + 2 \mathbf {E} \left[ B _ {1} ^ {3} Z _ {1} \right] + \mathbf {E} \left[ B _ {1} ^ {4} \right] \\ = \mathbf {E} [ B _ {1} ^ {2} ] \mathbf {E} [ Z _ {1} ^ {2} ] + 2 \mathbf {E} [ B _ {1} ^ {3} ] \mathbf {E} [ Z _ {1} ] + \mathbf {E} [ B _ {1} ^ {4} ] = 1 + \mathbf {E} [ B _ {1} ^ {4} ]. \\ \end{array}
$$

Note $B _ { 1 } \sim N ( 0 , 1 )$ , by the moment generating function, we have $\mathbf { E } \left[ e ^ { a B _ { 1 } } \right] = e ^ { { \frac { 1 } { 2 } } a ^ { 2 } }$ . Applying the Taylor’s expansion,

$$
\begin{array}{l} \mathbf {E} \left[ e ^ {a B _ {1}} \right] = \mathbf {E} \left[ 1 + a B _ {1} + \frac {1}{2} a ^ {2} B _ {1} ^ {2} + \frac {1}{3 !} a ^ {3} B _ {1} ^ {3} + \frac {1}{4 !} a ^ {4} B _ {1} ^ {4} + \dots \right] \\ = 1 + \mathbf {E} [ B _ {1} ] a + \frac {1}{2} a ^ {2} \mathbf {E} [ B _ {1} ^ {2} ] + \frac {1}{3 !} a ^ {3} \mathbf {E} [ B _ {1} ^ {3} ] + \frac {1}{4 !} a ^ {4} \mathbf {E} [ B _ {1} ^ {4} ] + \dots , \\ e ^ {\frac {1}{2} a ^ {2}} = 1 + \frac {1}{2} a ^ {2} + \frac {1}{2} \left(\frac {1}{2} a ^ {2}\right) ^ {2} + \dots . \\ \end{array}
$$

Comparing the coe"cients of $a ^ { 4 }$ , we deduce that ${ \bf E } [ B _ { 1 } ^ { 4 } ] = 3$ . Therefore,

$$
\mathbf {E} \left[ B _ {1} ^ {2} B _ {2} B _ {5} \right] = 1 + \mathbf {E} \left[ B _ {1} ^ {4} \right] = 4.
$$

4. Determine E[max $\{ B _ { 1 } - B _ { 4 } , 0 \} ]$ .

# Solution.

Let $Z = B _ { 1 } - B _ { 4 } \sim N ( 0 , 3 )$ . Then $Z / \sqrt { 3 } \sim N ( 0 , 1 )$ and

$$
\begin{array}{l} \mathbf {E} [ \max \{B _ {1} - B _ {4}, 0 \} ] = \mathbf {E} \left[ Z ^ {+} \right] = \sqrt {3} \mathbf {E} \left[ (Z / \sqrt {3}) ^ {+} \right] \\ = \sqrt {3} \frac {1}{\sqrt {2 \pi}} \int_ {- \infty} ^ {\infty} t ^ {+} e ^ {- 0. 5 t ^ {2}} \mathrm{d} t \\ = \sqrt {3} \frac {1}{\sqrt {2 \pi}} \int_ {0} ^ {\infty} t e ^ {- 0. 5 t ^ {2}} \mathrm{d} t \\ = - \sqrt {3} \frac {1}{\sqrt {2 \pi}} e ^ {- 0. 5 t ^ {2}} \bigg | _ {t = 0} ^ {\infty} = \frac {\sqrt {3}}{\sqrt {2 \pi}} \\ \end{array}
$$

5. Determine $\mathbf { E } \left[ ( e ^ { B _ { 1 } - B _ { 2 } } - 3 ) ^ { + } \right]$ . Use $\begin{array} { r } { N ( x ) = \frac { 1 } { \sqrt { 2 \pi } } \int _ { - \infty } ^ { x } e ^ { - 0 . 5 t ^ { 2 } } } \end{array}$ dt to express your result. Solution.

Let $Z = B _ { 1 } - B _ { 2 } \sim N ( 0 , 1 )$ . Then

$$
\begin{array}{l} \mathbf {E} \left[ (e ^ {B _ {1} - B _ {2}} - 3) ^ {+} \right] = \mathbf {E} \left[ (e ^ {Z} - 3) ^ {+} \right] = \frac {1}{\sqrt {2 \pi}} \int_ {- \infty} ^ {\infty} (e ^ {t} - 3) ^ {+} e ^ {- 0. 5 t ^ {2}} \mathrm{d} t \\ = \frac {1}{\sqrt {2 \pi}} \int_ {\ln (3)} ^ {\infty} (e ^ {t} - 3) e ^ {- 0. 5 t ^ {2}} \mathrm{d} t \\ = \frac {1}{\sqrt {2 \pi}} \int_ {\ln (3)} ^ {\infty} e ^ {t - 0. 5 t ^ {2}} \mathrm{d} t - \frac {3}{\sqrt {2 \pi}} \int_ {\ln (3)} ^ {\infty} e ^ {- 0. 5 t ^ {2}} \mathrm{d} t \\ = \frac {e ^ {0 . 5}}{\sqrt {2 \pi}} \int_ {\ln (3)} ^ {\infty} e ^ {- 0. 5 (t - 1) ^ {2}} \mathrm{d} t - 3 (1 - N (\ln (3))) \\ = \frac {e ^ {0 . 5}}{\sqrt {2 \pi}} \int_ {\ln (3) - 1} ^ {\infty} e ^ {- 0. 5 t ^ {2}} \mathrm{d} t - 3 (1 - N (\ln (3))) \\ = e ^ {0. 5} (1 - N (\ln (3) - 1)) - 3 (1 - N (\ln (3))). \\ \end{array}
$$

6. Find $\mathbf { E } \left\lceil e ^ { ( B _ { 1 } + B _ { 3 } ) t } \right\rceil$ and determine the distribution of $B _ { 1 } + B _ { 3 }$ . (Hint: A random variable $X \ \sim \ N ( \mu , \sigma ^ { 2 } )$ if and only if its moment generating function $M _ { X } ( t ) =$ $\mathbf { E } \left[ e ^ { t X } \right]$ is equal to $e ^ { \mu t + { \frac { 1 } { 2 } } \sigma ^ { 2 } t ^ { 2 } }$ . The sum of two independent normal distributions is still normal.)

# Solution.

Let $Z = B _ { 3 } - B _ { 1 } \sim N ( 0 , 2 )$ . Then Z and $B _ { 1 }$ are independent,

$$
\mathbf {E} \big [ e ^ {(B _ {1} + B _ {3}) t} \big ] = \mathbf {E} \big [ e ^ {(2 B _ {1} + Z) t} \big ] = \mathbf {E} \big [ e ^ {2 B _ {1} t} \big ] \mathbf {E} \big [ e ^ {Z t} \big ] = e ^ {2 t ^ {2}} e ^ {t ^ {2}} = e ^ {3 t ^ {2}}.
$$

Therefore, $B _ { 1 } + B _ { 3 } \sim N ( 0 , 6 )$ .