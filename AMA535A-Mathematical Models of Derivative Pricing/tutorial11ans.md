# Tutorial Eleven

1. Let

$$
X _ {t} = B _ {t} ^ {3} - 3 \int_ {0} ^ {t} B _ {r} \mathrm{d} r.
$$

Show that $X _ { t }$ is a martingale by Itô’s lemma.

Solution.

Let $Y _ { t } = B _ { t } ^ { 3 }$ and $\begin{array} { r } { Z _ { t } = \int _ { 0 } ^ { t } B _ { r } } \end{array}$ dr. By Itô’s lemma, we have

$$
\mathrm{d} Y _ {t} = 3 B _ {t} ^ {2} \mathrm{d} B _ {t} + 3 B _ {t} \mathrm{d} t.
$$

Thus

$$
\mathrm{d} X _ {t} = \mathrm{d} Y _ {t} - 3 \mathrm{d} Z _ {t} = 3 B _ {t} ^ {2} \mathrm{d} B _ {t}.
$$

The drift is 0, hence $X _ { t }$ is a martingale.

2. Suppose $X _ { t }$ is a martingale and $\mathbf { E } [ X _ { t } ^ { 2 } ] < \infty$ . Show that $X _ { t } ^ { 2 } - \langle X \rangle$ t is a martingale.

Solution.

Because $X _ { t }$ is a martingale, we have $\mathrm { d } X _ { t } = \sigma ( t ) \mathrm { d } B _ { t }$ for some adapted process $\sigma ( t )$ . Let $f ( x ) = x ^ { 2 }$ . Then by Itô’s lemma,

$$
\mathrm{d} (X _ {t} ^ {2}) = \mathrm{d} f (X _ {t}) = f ^ {\prime} (X _ {t}) \mathrm{d} X _ {t} + \frac {1}{2} f ^ {\prime \prime} (X _ {t}) \mathrm{d} \langle X \rangle_ {t} = 2 X _ {t} \sigma (t) \mathrm{d} B _ {t} + \mathrm{d} \langle X \rangle_ {t}.
$$

It follows

$$
\mathrm{d} (X _ {t} ^ {2} - \langle X \rangle_ {t}) = 2 X _ {t} \sigma (t) \mathrm{d} B _ {t},
$$

hence $X _ { t } ^ { 2 } - \langle X \rangle _ { t }$ t is a martingale.

3. Determine

$$
\mathbf {E} \left[ \int_ {0} ^ {T} B _ {t} \mathrm{d} t * \int_ {0} ^ {T} t \mathrm{d} B _ {t} \right].
$$

Solution.

We have

$$
\mathbf {E} \left[ \int_ {0} ^ {T} B _ {t} \mathrm{d} t * \int_ {0} ^ {T} t \mathrm{d} B _ {t} \right] = \int_ {0} ^ {T} \mathbf {E} \left[ B _ {t} * \int_ {0} ^ {T} s \mathrm{d} B _ {s} \right] \mathrm{d} t.
$$

Let

$$
f (s) = \left\{ \begin{array}{l l} 1, & s \leqslant t; \\ 0, & s > t. \end{array} \right.
$$

Then

$$
B _ {t} = \int_ {0} ^ {T} f (s) \mathrm{d} B _ {s}.
$$

So

$$
\begin{array}{l} \mathbf {E} \left[ B _ {t} * \int_ {0} ^ {T} s \mathrm{d} B _ {s} \right] = \mathbf {E} \left[ \int_ {0} ^ {T} f (s) \mathrm{d} B _ {s} * \int_ {0} ^ {T} s \mathrm{d} B _ {s} \right] \\ = \int_ {0} ^ {T} \mathbf {E} [ f (s) s ] \mathrm{d} s = \int_ {0} ^ {T} f (s) s \mathrm{d} s = \int_ {0} ^ {t} s \mathrm{d} s = \frac {1}{2} t ^ {2}. \\ \end{array}
$$

Therefore,

$$
\mathbf {E} \left[ \int_ {0} ^ {T} B _ {t} \mathrm{d} t * \int_ {0} ^ {T} t \mathrm{d} B _ {t} \right] = \int_ {0} ^ {T} \mathbf {E} \left[ B _ {t} * \int_ {0} ^ {T} s \mathrm{d} B _ {s} \right] \mathrm{d} t = \int_ {0} ^ {T} \frac {1}{2} t ^ {2} \mathrm{d} t = \frac {1}{6} T ^ {3}.
$$

4. If

$$
\mathrm{d} X _ {t} = X _ {t} (r \mathrm{d} t + \sigma \mathrm{d} B _ {t}), \quad t \geqslant 0,
$$

and

$$
\mathrm{d} Y _ {t} = Y _ {t} (\mu \mathrm{d} t + \vartheta \mathrm{d} B _ {t}), \quad t \geqslant 0.
$$

Find the Itô process for $Z _ { t } = X _ { t } / Y _ { t }$ .

# Solution.

Let $g ( x , y ) = x / y . \mathrm { T h e n } g _ { x } = 1 / y , g _ { y } = - x / y ^ { 2 } , g _ { x x } = 0 , g _ { y y } = 2 x / y ^ { 3 } , g _ { x y } = - 1 / y ^ { 2 } .$ . Therefore,

$$
\begin{array}{l} \mathrm{d} Z _ {t} = \mathrm{d} g (X _ {t}, Y _ {t}) \\ = g _ {x} \left(X _ {t}, Y _ {t}\right) \mathrm{d} X _ {t} + g _ {y} \left(X _ {t}, Y _ {t}\right) \mathrm{d} Y _ {t} + \frac {1}{2} g _ {x x} \left(X _ {t}, Y _ {t}\right) X _ {t} ^ {2} \sigma^ {2} \mathrm{d} t \\ + \frac {1}{2} g _ {y y} (X _ {t}, Y _ {t}) Y _ {t} ^ {2} \vartheta^ {2} \mathrm{d} t + g _ {x y} (X _ {t}) X _ {t} Y _ {t} \sigma \vartheta \mathrm{d} t \\ = \frac {1}{Y _ {t}} \mathrm{d} X _ {t} - \frac {X _ {t}}{Y _ {t} ^ {2}} \mathrm{d} Y _ {t} + \frac {X _ {t}}{Y _ {t} ^ {3}} Y _ {t} ^ {2} \vartheta^ {2} \mathrm{d} t - \frac {1}{Y _ {t} ^ {2}} X _ {t} Y _ {t} \sigma \vartheta \mathrm{d} t \\ = \frac {X _ {t}}{Y _ {t}} (r \mathrm{d} t + \sigma \mathrm{d} B _ {t}) - \frac {X _ {t}}{Y _ {t}} (\mu \mathrm{d} t + \vartheta \mathrm{d} B _ {t}) + \frac {X _ {t}}{Y _ {t}} \vartheta^ {2} \mathrm{d} t - \frac {X _ {t}}{Y _ {t}} \sigma \vartheta \mathrm{d} t \\ = Z _ {t} \left(\left(r - \mu + \vartheta^ {2} - \sigma \vartheta\right) \mathrm{d} t + (\sigma - \vartheta) \mathrm{d} B _ {t}\right). \\ \end{array}
$$

5. Suppose

$$
\mathrm{d} X _ {t} ^ {i} = A _ {t} X _ {t} ^ {i} \mathrm{d} t + C _ {t} X _ {t} ^ {i} \mathrm{d} B _ {t},
$$

where $A _ { t }$ and $C _ { t }$ are two bounded adapted processes, $i = 1 , 2$ . Given $X _ { 0 } ^ { 1 } > X _ { 0 } ^ { 2 }$ , show that $X _ { t } ^ { 1 } > X _ { t } ^ { 2 }$ , for any $t > 0$ . (Hint: consider $X _ { t } ^ { 1 } - X _ { t } ^ { 2 } )$

# Solution.

Let $Z _ { t } = X _ { t } ^ { 1 } - X _ { t } ^ { 2 }$ . Then $Z _ { 0 } > 0$ and

$$
\mathrm{d} Z _ {t} = A _ {t} Z _ {t} \mathrm{d} t + C _ {t} Z _ {t} \mathrm{d} B _ {t}.
$$

Let

$$
Y _ {t} = \int_ {0} ^ {t} \left(\frac {1}{2} C _ {s} ^ {2} - A _ {s}\right) \mathrm{d} s - \int_ {0} ^ {t} C _ {s} \mathrm{d} B _ {s}.
$$

Then

$$
\mathrm{d} Y _ {t} = \left(\frac {1}{2} C _ {t} ^ {2} - A _ {t}\right) \mathrm{d} t - C _ {t} \mathrm{d} B _ {t}.
$$

Let $U _ { t } = g ( Y _ { t } )$ with $g ( x ) = e ^ { x }$ . Then $g ^ { \prime } ( x ) = e ^ { x }$ and $g ^ { \prime \prime } ( x ) = e ^ { x }$ . Applying Itô’s Lemma to $g ( Y _ { t } )$ , we have

$$
\begin{array}{l} \mathrm{d} U _ {t} = \mathrm{d} g (Y _ {t}) = g ^ {\prime} (Y _ {t}) \mathrm{d} Y _ {t} + \frac {1}{2} g ^ {\prime \prime} (Y _ {t}) \mathrm{d} \langle Y \rangle_ {t} = g (Y _ {t}) (\mathrm{d} Y _ {t} + \frac {1}{2} \mathrm{d} \langle Y \rangle_ {t}) \\ = U _ {t} \left(\left(\frac {1}{2} C _ {t} ^ {2} - A _ {t}\right) \mathrm{d} t - C _ {t} \mathrm{d} B _ {t} + \frac {1}{2} C _ {t} ^ {2} d t\right) = U _ {t} \left(\left(C _ {t} ^ {2} - A _ {t}\right) \mathrm{d} t - C _ {t} \mathrm{d} B _ {t}\right). \\ \end{array}
$$

Now apply bivariate Itô’s Lemma to $Z _ { t } U _ { t }$ ,

$$
\begin{array}{l} \mathrm{d} \left(Z _ {t} U _ {t}\right) = Z _ {t} \mathrm{d} U _ {t} + U _ {t} \mathrm{d} Z _ {t} + \mathrm{d} \langle Z, U \rangle_ {t} \\ = Z _ {t} U _ {t} \left(\left(C _ {t} ^ {2} - A _ {t}\right) \mathrm{d} t - C _ {t} \mathrm{d} B _ {t}\right) + U _ {t} \left(A _ {t} Z _ {t} \mathrm{d} t + C _ {t} Z _ {t} \mathrm{d} B _ {t}\right) - C _ {t} Z _ {t} U _ {t} C _ {t} \mathrm{d} t \\ = 0. \\ \end{array}
$$

This means

$$
Z _ {t} U _ {t} = Z _ {0} U _ {0} + \int_ {0} ^ {t} 0 \mathrm{d} s + \int_ {0} ^ {t} 0 \mathrm{d} B _ {s} = Z _ {0} > 0.
$$

Notice $U _ { t } > 0$ , so $Z _ { t } > 0$ . In fact $Z _ { t } = Z _ { 0 } / U _ { t } = Z _ { 0 } e ^ { - Y _ { t } }$ , hence

$$
Z _ {t} = Z _ {0} \exp \left(\int_ {0} ^ {t} \left(A _ {s} - \frac {1}{2} C _ {s} ^ {2}\right) \mathrm{d} s + \int_ {0} ^ {t} C _ {s} \mathrm{d} B _ {s}\right) > 0.
$$