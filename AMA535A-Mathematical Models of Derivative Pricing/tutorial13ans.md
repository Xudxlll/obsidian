# Tutorial Thirteen

1. Consider the Black-Scholes formula for perpetual American put option striking at K = 45. If r = 10%, ω = 50%, and the stock price is 18, shall you exercise the option? Give your reason.

# Solution.

The maximum exercise price is determined by

$$
S _ {e} ^ {*} = \frac {2 r K}{2 r + \sigma^ {2}} = \frac {2 * 0 . 1 * 4 5}{2 * 0 . 1 + 0 . 5 ^ {2}} = 2 0.
$$

Since $1 8 < S _ { e } ^ { * } .$ , one shall exercise the option.

2. Let $\begin{array} { r } { m _ { t } = \operatorname* { m i n } _ { s \in [ 0 , t ] } B _ { s } } \end{array}$ . Determine $\mathbf { P } ( B _ { 2 } \geqslant 3 , m _ { 2 } < - 2 )$ .

# Solution.

By the formula

$$
\mathbf {P} (B _ {T} \geqslant x, m _ {T} \leqslant y) = \mathbf {P} (B _ {T} \leqslant 2 y - x), y <   0, y \leqslant x,
$$

we have

$$
\mathbf {P} (B _ {2} \geqslant 3, m _ {2} <   - 2) = \mathbf {P} (B _ {2} \leqslant - 7) = N (- 7 / \sqrt {2}).
$$

3. Determine the distribution of

$$
\int_ {t} ^ {T} (B _ {r} - B _ {t}) \mathrm{d} r.
$$

(Hint: Express the integral as a stochastic integral and apply Q4 in Tutorial Ten.)

# Solution.

Apply Itô’s lemma,

$$
\mathrm{d} (r B _ {r}) = r \mathrm{d} B _ {r} + B _ {r} \mathrm{d} r,
$$

so

$$
T B _ {T} = t B _ {t} + \int_ {t} ^ {T} r \mathrm{d} B _ {r} + \int_ {t} ^ {T} B _ {r} \mathrm{d} r,
$$

Therefore,

$$
\begin{array}{l} \int_ {t} ^ {T} \left(B _ {r} - B _ {t}\right) \mathrm{d} r = \int_ {t} ^ {T} B _ {r} \mathrm{d} r - (T - t) B _ {t} \\ = T B _ {T} - t B _ {t} - \int_ {t} ^ {T} r \mathrm{d} B _ {r} - (T - t) B _ {t} \\ = T (B _ {T} - B _ {t}) - \int_ {t} ^ {T} r \mathrm{d} B _ {r} \\ = \int_ {t} ^ {T} T \mathrm{d} B _ {r} - \int_ {t} ^ {T} r \mathrm{d} B _ {r} \\ = \int_ {t} ^ {T} (T - r) \mathrm{d} B _ {r}. \\ \end{array}
$$

By Q4 in Tutorial Ten, the right hand side follows

$$
N \left(0, \int_ {t} ^ {T} (T - r) ^ {2} \mathrm{d} r\right),
$$

so

$$
\int_ {t} ^ {T} (B _ {r} - B _ {t}) \mathrm{d} r \sim N \left(0, \frac {(T - t) ^ {3}}{3}\right).
$$

4. For any $a > 0$ , let $\tilde { B } _ { t } = B _ { t + a } - B _ { a }$ and $\tilde { \mathcal { F } } _ { t } = \mathcal { F } _ { t + a }$ . Show that $\{ \tilde { B } _ { t } , \ t \geqslant 0 \}$ is a standard Brownian motion under the information $\{ \tilde { \mathcal { F } } _ { t } , ~ t \geqslant 0 \}$ .

# Solution.

The assertion follows from the following properties.

• Clearly, $\tilde { B } _ { 0 } = B _ { a } - B _ { a } = 0$ and $\tilde { B } _ { t } = B _ { t + a } - B _ { a }$ is continuous in t.   
• For any $0 \leqslant s < t , \tilde { B } _ { t } - \tilde { B } _ { s } = B _ { t + a } - B _ { s + a }$ follows $N ( 0 , t - s )$ .   
• For any $0 \leqslant s < t , \tilde { B } _ { t } - \tilde { B } _ { s } = B _ { t + a } - B _ { s + a }$ is independent of the information $\mathcal { F } _ { s + a } = \tilde { \mathcal { F } } _ { s }$ .

5. (Hard) For $0 \leqslant a < b ,$ , let $m _ { a , b } = \operatorname* { m i n } _ { t \in [ a , b ] } B _ { t }$ . Determine its distribution.

# Solution.

Let $\tilde { B } _ { t } = B _ { t + a } - B _ { a }$ and $\tilde { \mathcal { F } } _ { t } = \mathcal { F } _ { t + a }$ . Using the previous result, for any $x \in \mathbb { R }$

$$
\begin{array}{l} \mathbf {P} \left(m _ {a, b} \leqslant x\right) = \mathbf {E} \left[ \mathbf {P} \left(m _ {a, b} \leqslant x \mid B _ {a}\right) \right] \\ = \mathbf {E} \left[ \mathbf {P} \left(\min _ {t \in [ a, b ]} (B _ {t} - B _ {a}) \leqslant x - B _ {a} \mid B _ {a}\right) \right] \\ = \int_ {- \infty} ^ {\infty} \mathbf {P} \left(\min _ {t \in [ a, b ]} \left(B _ {t} - B _ {a}\right) \leqslant x - y \mid B _ {a} = y\right) \frac {1}{\sqrt {2 \pi a}} e ^ {- \frac {y ^ {2}}{2 a}} d y \\ = \int_ {- \infty} ^ {\infty} \mathbf {P} \left(\min _ {t \in [ a, b ]} (B _ {t} - B _ {a}) \leqslant x - y\right) \frac {1}{\sqrt {2 \pi a}} e ^ {- \frac {y ^ {2}}{2 a}} d y \\ = \int_ {- \infty} ^ {\infty} \mathbf {P} \left(\min _ {s \in [ 0, b - a ]} \tilde {B} _ {s} \leqslant x - y\right) \frac {1}{\sqrt {2 \pi a}} e ^ {- \frac {y ^ {2}}{2 a}} d y \\ = \int_ {- \infty} ^ {x} \frac {1}{\sqrt {2 \pi a}} e ^ {- \frac {y ^ {2}}{2 a}} d y + \int_ {x} ^ {\infty} \mathbf {P} \left(| \tilde {B} _ {b - a} | \geqslant y - x\right) \frac {1}{\sqrt {2 \pi a}} e ^ {- \frac {y ^ {2}}{2 a}} d y \\ = \int_ {- \infty} ^ {x / \sqrt {a}} \frac {1}{\sqrt {2 \pi}} e ^ {- \frac {z ^ {2}}{2}} d z + \int_ {x} ^ {\infty} 2 \mathbf {P} (\tilde {B} _ {b - a} \leqslant x - y) \frac {1}{\sqrt {2 \pi a}} e ^ {- \frac {y ^ {2}}{2 a}} d y \\ = N \left(\frac {x}{\sqrt {a}}\right) + 2 \int_ {x} ^ {\infty} N \left(\frac {x - y}{\sqrt {b - a}}\right) \frac {1}{\sqrt {2 \pi a}} e ^ {- \frac {y ^ {2}}{2 a}} d y \\ = N \left(\frac {x}{\sqrt {a}}\right) + 2 \int_ {0} ^ {\infty} N \left(\frac {- z}{\sqrt {b - a}}\right) \frac {1}{\sqrt {2 \pi a}} e ^ {- \frac {z ^ {2} + 2 x z + x ^ {2}}{2 a}} d z. \\ \end{array}
$$