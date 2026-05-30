# Tutorial Eight

1. Let a be a real constant. Show that $e ^ { a B _ { t } - a ^ { 2 } t / 2 }$ is a martingale. We have for $s < t ,$

$$
\begin{array}{l} \mathbf {E} \Big [ e ^ {a B _ {t} - a ^ {2} t / 2} | \mathcal {F} _ {s} \Big ] = e ^ {a B _ {s} - a ^ {2} t / 2} \mathbf {E} \big [ e ^ {a (B _ {t} - B _ {s})} | \mathcal {F} _ {s} \big ] = e ^ {a B _ {s} - a ^ {2} t / 2} \mathbf {E} \big [ e ^ {a (B _ {t} - B _ {s})} \big ] \\ = e ^ {a B _ {s} - a ^ {2} t / 2} e ^ {a ^ {2} (t - s) / 2} = e ^ {a B _ {s} - a ^ {2} s / 2}, \\ \end{array}
$$

so $e ^ { a B _ { t } - a ^ { 2 } t / 2 }$ is a martingale.

2. Determine

$$
\mathbf {E} \left[ \left(\int_ {0} ^ {T} B _ {t} \mathrm{d} t\right) ^ {2} \right].
$$

# Solution.

Note that $\mathbf { E } [ B _ { u } * B _ { v } ] = \operatorname* { m i n } \{ u , v \}$ , so we have

$$
\begin{array}{l} \mathbf {E} \left[ \left(\int_ {0} ^ {T} B _ {t} \mathrm{d} t\right) ^ {2} \right] = \mathbf {E} \left[ \int_ {0} ^ {T} B _ {u} \mathrm{d} u * \int_ {0} ^ {T} B _ {v} \mathrm{d} v \right] \\ = \mathbf {E} \left[ \int_ {0} ^ {T} \int_ {0} ^ {T} B _ {u} * B _ {v} \mathrm{d} u \mathrm{d} v \right] \\ = \int_ {0} ^ {T} \int_ {0} ^ {T} \mathbf {E} \left[ B _ {u} * B _ {v} \right] \mathrm{d} u \mathrm{d} v \\ = \int_ {0} ^ {T} \int_ {0} ^ {T} \min \{u, v \} d u d v \\ = \int_ {0} ^ {T} \int_ {0} ^ {v} \min \{u, v \} d u d v + \int_ {0} ^ {T} \int_ {v} ^ {T} \min \{u, v \} d u d v \\ = \int_ {0} ^ {T} \int_ {0} ^ {v} u \mathrm{d} u \mathrm{d} v + \int_ {0} ^ {T} \int_ {v} ^ {T} v \mathrm{d} u \mathrm{d} v \\ = \int_ {0} ^ {T} \frac {1}{2} v ^ {2} \mathrm{d} v + \int_ {0} ^ {T} v (T - v) \mathrm{d} v = \frac {1}{3} T ^ {3}. \\ \end{array}
$$

3. Let $\tau = \operatorname* { i n f } \{ t \geqslant 0 : B _ { t } + 2 t \notin ( - 1 , 2 ) \}$ . Find $\mathbf { E } [ \tau ]$ . (Hint: $e ^ { a B _ { t } - a ^ { 2 } t / 2 }$ is a martingale for any constant a) Since $B _ { t }$ and $e ^ { - 4 B _ { t } - 8 t }$ are both martingales, by Doob’s optional stopping theorem, we have $\mathbf { E } [ B _ { \tau } ] = 0$ and

$$
1 = \mathbf {E} \left[ e ^ {- 4 B _ {\tau} - 8 \tau} \right] = \mathbf {P} (B _ {\tau} + 2 \tau = - 1) e ^ {4} + \mathbf {P} (B _ {\tau} + 2 \tau = 2) e ^ {- 8}.
$$

Because $\mathbf { P } ( B _ { \tau } + 2 \tau = - 1 ) + \mathbf { P } ( B _ { \tau } + 2 \tau = 2 ) = 1$ ,

$$
\mathbf {P} (B _ {\tau} + 2 \tau = - 1) = \frac {1 - e ^ {- 8}}{e ^ {4} - e ^ {- 8}}, \quad \mathbf {P} (B _ {\tau} + 2 \tau = 2) = \frac {e ^ {4} - 1}{e ^ {4} - e ^ {- 8}}.
$$

Therefore,

$$
2 \mathbf {E} [ \tau ] = \mathbf {E} \left[ B _ {\tau} + 2 \tau \right] = (- 1) * \mathbf {P} \left(B _ {\tau} + 2 \tau = - 1\right) + 2 * \mathbf {P} \left(B _ {\tau} + 2 \tau = 2\right)
$$

$$
= \frac {2 e ^ {4} - 3 + e ^ {- 8}}{e ^ {4} - e ^ {- 8}} = 1. 9 4 5,
$$

so $\mathbf { E } [ \tau ] = 0 . 9 7 2 5$ .

4. Given

$$
X _ {t} = B _ {t} ^ {3} - 3 \int_ {0} ^ {t} B _ {r} \mathrm{d} r.
$$

Show that $X _ { t }$ is a martingale.

Solution.

For any $s < t ,$ let $Z = B _ { t } - B _ { s }$ . Then $B _ { t } = B _ { s } + Z$ . So

$$
X _ {t} = (B _ {s} + Z) ^ {3} - 3 \int_ {0} ^ {t} B _ {r} \mathrm{d} r
$$

$$
= B _ {s} ^ {3} - 3 \int_ {0} ^ {s} B _ {r} \mathrm{d} r + 3 B _ {s} ^ {2} Z + 3 B _ {s} Z ^ {2} + Z ^ {3} - 3 \int_ {s} ^ {t} B _ {r} \mathrm{d} r
$$

$$
= X _ {s} + 3 B _ {s} ^ {2} Z + 3 B _ {s} Z ^ {2} + Z ^ {3} - 3 \int_ {s} ^ {t} B _ {r} \mathrm{d} r.
$$

We notice that Z and $F _ { s }$ are independent and $Z \sim N ( 0 , t - s )$ , so

$$
\begin{array}{l} \mathbf {E} [ X _ {t} - X _ {s} \mid \mathcal {F} _ {s} ] = \mathbf {E} \big [ 3 B _ {s} ^ {2} Z + 3 B _ {s} Z ^ {2} + Z ^ {3} \mid \mathcal {F} _ {s} \big ] - 3 \mathbf {E} \left[ \int_ {s} ^ {t} B _ {r} \mathrm{d} r \Bigg | \mathcal {F} _ {s} \right] \\ = 3 \mathbf {E} \left[ B _ {s} ^ {2} Z \mid \mathcal {F} _ {s} \right] + 3 \mathbf {E} \left[ B _ {s} Z ^ {2} \mid \mathcal {F} _ {s} \right] + \mathbf {E} \left[ Z ^ {3} \mid \mathcal {F} _ {s} \right] - 3 \int_ {s} ^ {t} \mathbf {E} \left[ B _ {r} \mid \mathcal {F} _ {s} \right] d r \\ = 3 B _ {s} ^ {2} \mathbf {E} [ Z \mid \mathcal {F} _ {s} ] + 3 B _ {s} \mathbf {E} \left[ Z ^ {2} \mid \mathcal {F} _ {s} \right] - 3 \int_ {s} ^ {t} B _ {s} \mathrm{d} r \\ = 3 B _ {s} ^ {2} \mathbf {E} [ Z ] + 3 B _ {s} \mathbf {E} \left[ Z ^ {2} \right] - 3 B _ {s} \int_ {s} ^ {t} 1 \mathrm{d} r \\ = 3 B _ {s} (t - s) - 3 B _ {s} (t - s) = 0. \\ \end{array}
$$

Hence $X _ { t }$ is a martingale.

5. Determine the mean and variance of $\begin{array} { r } { X = \int _ { 0 } ^ { T } B _ { t } ^ { 2 } \mathrm { d } t } \end{array}$ .

Solution.

We have

$$
\mathbf {E} [ X ] = \mathbf {E} \left[ \int_ {0} ^ {T} B _ {t} ^ {2} \mathrm{d} t \right] = \int_ {0} ^ {T} \mathbf {E} \left[ B _ {t} ^ {2} \right] \mathrm{d} t = \int_ {0} ^ {T} t \mathrm{d} t = \frac {1}{2} T ^ {2}.
$$

And

$$
\begin{array}{l} \mathbf {E} \left[ X ^ {2} \right] = \mathbf {E} \left[ \left(\int_ {0} ^ {T} B _ {t} ^ {2} \mathrm{d} t\right) ^ {2} \right] = \mathbf {E} \left[ \int_ {0} ^ {T} B _ {u} ^ {2} \mathrm{d} u * \int_ {0} ^ {T} B _ {v} ^ {2} \mathrm{d} v \right] \\ = \mathbf {E} \left[ \int_ {0} ^ {T} \int_ {0} ^ {T} B _ {u} ^ {2} * B _ {v} ^ {2} \mathrm{d} u \mathrm{d} v \right] = \int_ {0} ^ {T} \int_ {0} ^ {T} \mathbf {E} \left[ B _ {u} ^ {2} * B _ {v} ^ {2} \right] \mathrm{d} u \mathrm{d} v \\ = \int_ {0} ^ {T} \int_ {0} ^ {v} \mathbf {E} \left[ B _ {u} ^ {2} * B _ {v} ^ {2} \right] \mathrm{d} u \mathrm{d} v + \int_ {0} ^ {T} \int_ {v} ^ {T} \mathbf {E} \left[ B _ {u} ^ {2} * B _ {v} ^ {2} \right] \mathrm{d} u \mathrm{d} v. (*) \\ \end{array}
$$

If u $\geqslant v$ , let $Z = B _ { u } - B _ { v } \sim N ( 0 , u - v )$ . Then $Z$ and $B _ { v }$ are independent and

$$
\begin{array}{l} \mathbf {E} \left[ B _ {u} ^ {2} * B _ {v} ^ {2} \right] = \mathbf {E} \left[ (B _ {v} + Z) ^ {2} * B _ {v} ^ {2} \right] = \mathbf {E} \left[ (B _ {v} ^ {2} + 2 Z B _ {v} + Z ^ {2}) B _ {v} ^ {2} \right] \\ = \mathbf {E} \left[ B _ {v} ^ {4} \right] + 2 \mathbf {E} \left[ Z B _ {v} ^ {3} \right] + \mathbf {E} \left[ Z ^ {2} B _ {v} ^ {2} \right] \\ = \mathbf {E} \left[ B _ {v} ^ {4} \right] + 2 \mathbf {E} [ Z ] \mathbf {E} \left[ B _ {v} ^ {3} \right] + \mathbf {E} \left[ Z ^ {2} \right] \mathbf {E} \left[ B _ {v} ^ {2} \right] \\ = 3 v ^ {2} + (u - v) v = 2 v ^ {2} + u v, \\ \end{array}
$$

where we use the moment generating function for the normal distributions to get the second, third and fourth moments of $B _ { v }$ . Similar if $u < v$ , then $\mathbf { E } [ B _ { u } ^ { 2 } * B _ { v } ^ { 2 } ] =$ $2 u ^ { 2 } + u v$ . By equation (→),

$$
\begin{array}{l} \mathbf {E} \left[ X ^ {2} \right] = \int_ {0} ^ {T} \int_ {0} ^ {v} \mathbf {E} \left[ B _ {u} ^ {2} * B _ {v} ^ {2} \right] \mathrm{d} u \mathrm{d} v + \int_ {0} ^ {T} \int_ {v} ^ {T} \mathbf {E} \left[ B _ {u} ^ {2} * B _ {v} ^ {2} \right] \mathrm{d} u \mathrm{d} v \\ = \int_ {0} ^ {T} \int_ {0} ^ {v} (2 u ^ {2} + u v) \mathrm{d} u \mathrm{d} v + \int_ {0} ^ {T} \int_ {v} ^ {T} (2 v ^ {2} + u v) \mathrm{d} u \mathrm{d} v \\ = \int_ {0} ^ {T} \int_ {0} ^ {v} 2 u ^ {2} \mathrm{d} u \mathrm{d} v + \int_ {0} ^ {T} \int_ {v} ^ {T} 2 v ^ {2} \mathrm{d} u \mathrm{d} v + \int_ {0} ^ {T} \int_ {0} ^ {T} u v \mathrm{d} u \mathrm{d} v \\ = \int_ {0} ^ {T} \frac {2}{3} v ^ {3} \mathrm{d} v + \int_ {0} ^ {T} 2 v ^ {2} (T - v) \mathrm{d} v + \int_ {0} ^ {T} \frac {1}{2} T ^ {2} v \mathrm{d} v \\ = \frac {1}{6} T ^ {4} + \frac {2}{3} T ^ {4} - \frac {1}{2} T ^ {4} + \frac {1}{4} T ^ {4} = \frac {7}{1 2} T ^ {4}. \\ \end{array}
$$

Therefore,

$$
\mathbf {V a r} (X) = \mathbf {E} \left[ X ^ {2} \right] - (\mathbf {E} [ X ]) ^ {2} = \frac {7}{1 2} T ^ {4} - \frac {1}{4} T ^ {4} = \frac {1}{3} T ^ {4}.
$$