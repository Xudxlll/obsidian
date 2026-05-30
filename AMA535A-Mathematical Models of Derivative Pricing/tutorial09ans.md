# Tutorial Nine

1. Determine

$$
\mathbf {E} \left[ \left(\int_ {0} ^ {T} \int_ {0} ^ {t} B _ {s} \mathrm{d} B _ {s} \mathrm{d} B _ {t}\right) ^ {2} \right].
$$

Solution.

Let $\begin{array} { r } { X _ { t } = \int _ { 0 } ^ { t } B _ { s } \mathrm { d } B _ { s } } \end{array}$ . By Itô’s isometry,

$$
\mathbf {E} \left[ X _ {t} ^ {2} \right] = \mathbf {E} \left[ \left(\int_ {0} ^ {t} B _ {s} \mathrm{d} B _ {s}\right) ^ {2} \right] = \int_ {0} ^ {t} \mathbf {E} \left[ B _ {s} ^ {2} \right] \mathrm{d} s = \int_ {0} ^ {t} s \mathrm{d} s = \frac {1}{2} t ^ {2}.
$$

By Itô’s isometry again,

$$
\begin{array}{l} \mathbf {E} \left[ \left(\int_ {0} ^ {T} \int_ {0} ^ {t} B _ {s} \mathrm{d} B _ {s} \mathrm{d} B _ {t}\right) ^ {2} \right] = \mathbf {E} \left[ \left(\int_ {0} ^ {T} X _ {t} \mathrm{d} B _ {t}\right) ^ {2} \right] \\ = \int_ {0} ^ {T} {\bf E} \left[ X _ {t} ^ {2} \right] \mathrm{d} t = \int_ {0} ^ {T} \frac {1}{2} t ^ {2} \mathrm{d} t = \frac {1}{6} T ^ {3}. \\ \end{array}
$$

2. Determine

$$
\mathbf {E} \left[ \left(\int_ {0} ^ {T} \sqrt {| B _ {t} |} \mathrm{d} B _ {t}\right) ^ {2} \right].
$$

Solution.

By Itô’s isometry

$$
\mathbf {E} \left[ \left(\int_ {0} ^ {T} \sqrt {| B _ {t} |} \mathrm{d} B _ {t}\right) ^ {2} \right] = \int_ {0} ^ {T} \mathbf {E} [ | B _ {t} | ] \mathrm{d} t.
$$

Notice $B _ { t } \sim N ( 0 , t )$ , so $\begin{array} { r } { \frac { B _ { t } } { \sqrt { t } } \sim N ( 0 , 1 ) } \end{array}$ and

$$
\begin{array}{l} \mathbf {E} [ | B _ {t} | ] = \sqrt {t} \mathbf {E} \left[ \left| \frac {B _ {t}}{\sqrt {t}} \right| \right] \\ = \sqrt {t} \int_ {- \infty} ^ {\infty} \frac {1}{\sqrt {2 \pi}} | x | e ^ {- x ^ {2} / 2} \mathrm{d} x = \frac {2 \sqrt {t}}{\sqrt {2 \pi}} \int_ {0} ^ {\infty} x e ^ {- x ^ {2} / 2} \mathrm{d} x = \frac {2 \sqrt {t}}{\sqrt {2 \pi}}. \\ \end{array}
$$

Therefore,

$$
\mathbf {E} \left[ \left(\int_ {0} ^ {T} \sqrt {| B _ {t} |} \mathrm{d} B _ {t}\right) ^ {2} \right] = \int_ {0} ^ {T} \frac {2 \sqrt {t}}{\sqrt {2 \pi}} \mathrm{d} t = \frac {4}{3 \sqrt {2 \pi}} T ^ {3 / 2}.
$$

3. Find the variance of $B _ { 1 } + B _ { 3 } - B _ { 5 } + B _ { 7 } - B _ { 9 } + B _ { 1 0 } + B _ { 1 2 }$ . (Hint: write it as a stochastic integral)

Solution.

Note that

$$
B _ {1} + B _ {3} - B _ {5} + B _ {7} - B _ {9} + B _ {1 0} + B _ {1 2}
$$

$$
= B _ {1 2} - B _ {1 0} + 2 \left(B _ {1 0} - B _ {9}\right) + \left(B _ {9} - B _ {7}\right) + 2 \left(B _ {7} - B _ {5}\right)
$$

$$
+ \left(B _ {5} - B _ {3}\right) + 2 \left(B _ {3} - B _ {1}\right) + 3 \left(B _ {1} - B _ {0}\right).
$$

Let

$$
f (t) = \left\{ \begin{array}{l l} 3, & \quad \text {if} 0 \leqslant t \leqslant 1; \\ 2, & \quad \text {if} 1 <   t \leqslant 3; \\ 1, & \quad \text {if} 3 <   t \leqslant 5; \\ 2, & \quad \text {if} 5 <   t \leqslant 7; \\ 1, & \quad \text {if} 7 <   t \leqslant 9; \\ 2, & \quad \text {if} 9 <   t \leqslant 1 0; \\ 1, & \quad \text {if} t > 1 0. \end{array} \right.
$$

Then

$$
B _ {1} + B _ {3} - B _ {5} + B _ {7} - B _ {9} + B _ {1 0} + B _ {1 2}
$$

$$
= B _ {1 2} - B _ {1 0} + 2 \left(B _ {1 0} - B _ {9}\right) + \left(B _ {9} - B _ {7}\right) + 2 \left(B _ {7} - B _ {5}\right)
$$

$$
+ \left(B _ {5} - B _ {3}\right) + 2 \left(B _ {3} - B _ {1}\right) + 3 \left(B _ {1} - B _ {0}\right)
$$

$$
= \int_ {0} ^ {1 2} f (t) \mathrm{d} B _ {t}
$$

Therefore,

$$
\operatorname{Var} \left(B _ {1} + B _ {3} - B _ {5} + B _ {7} - B _ {9} + B _ {1 0} + B _ {1 2}\right)
$$

$$
= \operatorname{Var} \left(\int_ {0} ^ {1 2} f (t) \mathrm{d} B _ {t}\right) = \mathbf {E} \left[ \left(\int_ {0} ^ {1 2} f (t) \mathrm{d} B _ {t}\right) ^ {2} \right]
$$

$$
= \int_ {0} ^ {1 2} \mathbf {E} [ f ^ {2} (t) ] \mathrm{d} t = \int_ {0} ^ {1 2} f ^ {2} (t) \mathrm{d} t
$$

$$
= \int_ {0} ^ {1} f ^ {2} (t) \mathrm{d} t + \int_ {1} ^ {3} f ^ {2} (t) \mathrm{d} t + \int_ {3} ^ {5} f ^ {2} (t) \mathrm{d} t + \int_ {5} ^ {7} f ^ {2} (t) \mathrm{d} t
$$

$$
+ \int_ {7} ^ {9} f ^ {2} (t) \mathrm{d} t + \int_ {9} ^ {1 0} f ^ {2} (t) \mathrm{d} t + \int_ {1 0} ^ {1 2} f ^ {2} (t) \mathrm{d} t
$$

$$
= \int_ {0} ^ {1} 3 ^ {2} \mathrm{d} t + \int_ {1} ^ {3} 2 ^ {2} \mathrm{d} t + \int_ {3} ^ {5} 1 ^ {2} \mathrm{d} t + \int_ {5} ^ {7} 2 ^ {2} \mathrm{d} t
$$

$$
+ \int_ {7} ^ {9} 1 ^ {2} \mathrm{d} t + \int_ {9} ^ {1 0} 2 ^ {2} \mathrm{d} t + \int_ {1 0} ^ {1 2} 1 ^ {2} \mathrm{d} t = 3 5.
$$

4. The correlation between the two Brownian motions $\{ B _ { t } , t \geqslant 0 \}$ and $\{ \overline { { B } } _ { t } , t \geqslant 0 \}$ is

⇢. Determine

$$
\mathbf {E} \left[ \overline {{B}} _ {T} * \int_ {0} ^ {T} B _ {t} ^ {2} \mathrm{d} B _ {t} \right].
$$

# Solution.

We have

$$
\begin{array}{l} \mathbf {E} \left[ \overline {{B}} _ {T} * \int_ {0} ^ {T} B _ {t} ^ {2} \mathrm{d} B _ {t} \right] = \mathbf {E} \left[ \int_ {0} ^ {T} 1 \mathrm{d} \overline {{B}} _ {t} * \int_ {0} ^ {T} B _ {t} ^ {2} \mathrm{d} B _ {t} \right] \\ = \rho \int_ {0} ^ {T} {\bf E} \left[ 1 * B _ {t} ^ {2} \right] \mathrm{d} t = \rho \int_ {0} ^ {T} t \mathrm{d} t = \frac {1}{2} \rho T ^ {2}. \\ \end{array}
$$

5. Suppose d $r _ { t } = a ( b - r _ { t } ) \mathrm { d } t + \sigma \sqrt { r _ { t } } \mathrm { d } B _ { t }$ . Determine $\mathbf { E } [ r _ { t } ]$

# Solution.

Taking expectation, we have

$$
\mathrm{d} \mathbf {E} [ r _ {t} ] = a (b - \mathbf {E} [ r _ {t} ]) \mathrm{d} t.
$$

Let $\boldsymbol { h } ( t ) ~ = ~ \mathbf { E } [ \boldsymbol { r } _ { t } ]$ . Then $h ^ { \prime } ( t ) \ = \ a ( b - h ( t ) )$ or $( h ( t ) - b ) ^ { \prime } = - a ( h ( t ) - b )$ , so $( \log ( h ( t ) - b ) ) ^ { \prime } = - a$ . Integrating both sides gives $h ( t ) - b = ( h ( 0 ) - b ) e ^ { - a t }$ or

$$
h (t) = \mathbf {E} [ r _ {t} ] = b + (r _ {0} - b) e ^ {- a t}.
$$

6. Determine

$$
\mathbf {E} \left[ \int_ {0} ^ {9} B _ {t} \mathrm{d} B _ {t} * \int_ {3} ^ {2 0} B _ {t - 2} \mathrm{d} B _ {t} \right].
$$

# Solution.

Let

$$
f (t) = \left\{ \begin{array}{l l} B _ {t}, & t \leqslant 9; \\ 0, & t > 9, \end{array} \right. \quad \text { and } \quad g (t) = \left\{ \begin{array}{l l} B _ {t - 2}, & 3 <   t \leqslant 2 0; \\ 0, & \text { otherwise }. \end{array} \right.
$$

Then

$$
\begin{array}{l} \mathbf {E} \left[ \int_ {0} ^ {9} B _ {t} \mathrm{d} B _ {t} * \int_ {3} ^ {2 0} B _ {t - 2} \mathrm{d} B _ {t} \right] = \mathbf {E} \left[ \int_ {0} ^ {2 0} f (t) \mathrm{d} B _ {t} * \int_ {0} ^ {2 0} g (t) \mathrm{d} B _ {t} \right] \\ = \int_ {0} ^ {2 0} \mathbf {E} [ f (t) g (t) ] \mathrm{d} t = \int_ {3} ^ {9} \mathbf {E} [ B _ {t} B _ {t - 2} ] \mathrm{d} t \\ = \int_ {3} ^ {9} (t - 2) \mathrm{d} t = 2 4. \\ \end{array}
$$