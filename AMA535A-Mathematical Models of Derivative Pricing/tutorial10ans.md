# Tutorial Ten

1. Given a smooth deterministic function $f ( t , x )$ , determine the Itô process for $f ( t , B _ { t } ^ { 2 } )$ . Solution.

Let $g ( t , x ) = f ( t , x ^ { 2 } )$ . Then $g _ { t } ( t , x ) = f _ { t } ( t , x ^ { 2 } ) , g _ { x } ( t , x ) = 2 x f _ { x } ( t , x ^ { 2 } )$ and $g _ { x x } ( t , x ) =$ $4 x ^ { 2 } f _ { x x } ( t , x ^ { 2 } ) + 2 f _ { x } ( t , x ^ { 2 } )$ . Therefore, by Itô’s lemma,

$$
\begin{array}{l} \mathrm{d} f (t, B _ {t} ^ {2}) = \mathrm{d} g (t, B _ {t}) = \left(g _ {t} (t, B _ {t}) + \frac {1}{2} g _ {x x} (t, B _ {t})\right) \mathrm{d} t + g _ {x} (t, B _ {t}) \mathrm{d} B _ {t} \\ = \left(f _ {t} (t, B _ {t} ^ {2}) + 2 B _ {t} ^ {2} f _ {x x} (t, B _ {t} ^ {2}) + f _ {x} (t, B _ {t} ^ {2})\right) \mathrm{d} t + 2 B _ {t} f _ {x} (t, B _ {t} ^ {2}) \mathrm{d} B _ {t}. \\ \end{array}
$$

2. Find the quadratic variation process for $B _ { t } ^ { 3 }$ .

# Solution.

Let $f ( x ) = x ^ { 3 }$ . Then Itô’s lemma gives

$$
\mathrm{d} f (B _ {t}) = \frac {1}{2} f ^ {\prime \prime} (B _ {t}) \mathrm{d} t + f ^ {\prime} (B _ {t}) \mathrm{d} B _ {t} = 3 B _ {t} \mathrm{d} t + 3 B _ {t} ^ {2} \mathrm{d} B _ {t}.
$$

Therefore, the quadratic variation process of $B _ { t } ^ { 3 }$ is

$$
\langle B ^ {3} \rangle_ {t} = \int_ {0} ^ {t} 9 B _ {s} ^ {4} \mathrm{d} s.
$$

3. Let $X _ { t } = B _ { t } – 2 t$ . Find a non-constant function $f ( x )$ such that $f ( X _ { t } )$ is a martingale. Solution.

Notice that d $X _ { t } = - 2 \mathrm { d } t + \mathrm { d } B _ { t }$ . By Itô’s lemma,

$$
\begin{array}{l} \mathrm{d} f (X _ {t}) = f ^ {\prime} (X _ {t}) \mathrm{d} X _ {t} + \frac {1}{2} f ^ {\prime \prime} (X _ {t}) \mathrm{d} t \\ = \left(- 2 f ^ {\prime} (X _ {t}) + \frac {1}{2} f ^ {\prime \prime} (X _ {t})\right) \mathrm{d} t + f ^ {\prime} (X _ {t}) \mathrm{d} B _ {t}. \\ \end{array}
$$

So $f ( X _ { t } )$ is a martingale if and only if

$$
- 2 f ^ {\prime} (X _ {t}) + \frac {1}{2} f ^ {\prime \prime} (X _ {t}) = 0.
$$

This is an ordinary differential equation, whose solution is

$$
f (x) = c e ^ {4 x}.
$$

4. Let $f ( t )$ be a deterministic function and $\begin{array} { r } { X _ { t } = \int _ { 0 } ^ { t } f ( s ) \mathrm { d } B _ { s } } \end{array}$ . Determine the distribution of $X _ { t }$ . (Hint: compute its moment generating function to determine its distribution.)

# Solution.

Let $Y _ { t } = g ( X _ { t } )$ , where $g ( x ) = e ^ { \lambda x }$ . Then $Y _ { t } = e ^ { \lambda X _ { t } }$ . Note $g _ { x } ( x ) = \lambda e ^ { \lambda x } = \lambda g ( x )$ and $g _ { x x } ( x ) = \lambda ^ { 2 } e ^ { \lambda x } = \lambda ^ { 2 } g ( x )$ . Note d $X _ { t } = f ( t ) \mathrm { d } B _ { t }$ , applying Itô’s Lemma,

$$
\begin{array}{l} \mathrm{d} Y _ {t} = \mathrm{d} g (X _ {t}) \\ = g _ {x} \left(X _ {t}\right) \mathrm{d} X _ {t} + \frac {1}{2} g _ {x x} \left(X _ {t}\right) f ^ {2} (t) \mathrm{d} t \\ = \lambda g (X _ {t}) \mathrm{d} X _ {t} + \frac {1}{2} \lambda^ {2} g (X _ {t}) f ^ {2} (t) \mathrm{d} t \\ = \lambda Y _ {t} \mathrm{d} X _ {t} + \frac {1}{2} \lambda^ {2} Y _ {t} f ^ {2} (t) \mathrm{d} t \\ = \lambda Y _ {t} f (t) \mathrm{d} B _ {t} + \frac {1}{2} \lambda^ {2} Y _ {t} f ^ {2} (t) \mathrm{d} t. \\ \end{array}
$$

Taking expectation,

$$
\mathrm{d} \mathbf {E} [ Y _ {t} ] = \mathbf {E} \left[ \frac {1}{2} \lambda^ {2} f ^ {2} (t) Y _ {t} \right] \mathrm{d} t = \frac {1}{2} \lambda^ {2} f ^ {2} (t) \mathbf {E} [ Y _ {t} ] \mathrm{d} t.
$$

Denote $h ( t ) = \mathbf { E } [ Y _ { t } ]$ , the above equation reads

$$
h ^ {\prime} (t) = \frac {1}{2} \lambda^ {2} f ^ {2} (t) h (t).
$$

Solving this ODE, we deduce

$$
h (t) = h (0) e ^ {\int_ {0} ^ {t} \frac {1}{2} \lambda^ {2} f ^ {2} (s) \mathrm{d} s} = e ^ {\int_ {0} ^ {t} \frac {1}{2} \lambda^ {2} f ^ {2} (s) \mathrm{d} s}.
$$

Thus,

$$
\mathbf {E} \left[ e ^ {\lambda X _ {t}} \right] = \mathbf {E} [ Y _ {t} ] = h (t) = e ^ {\frac {1}{2} \lambda^ {2} \int_ {0} ^ {t} f ^ {2} (s) \mathrm{d} s}.
$$

This means the moment generating function of $X _ { t }$ is $e ^ { \frac { 1 } { 2 } \lambda ^ { 2 } \int _ { 0 } ^ { t } f ^ { 2 } ( s ) \mathrm { d } s }$ , so $X _ { t }$ is normally distributed with mean 0 and variance $\textstyle \int _ { 0 } ^ { t } f ^ { 2 } ( s )$ ds.

5. Suppose d $r _ { t } = a ( b - r _ { t } ) \mathrm { d } t + \sigma \sqrt { r _ { t } } \mathrm { d } B _ { t }$ . Find $\mathbf { E } [ r _ { t } ]$ and $\mathbf { V a r } ( r _ { t } )$ .

Solution.

Taking expectation, we have

$$
\mathrm{d} \mathbf {E} [ r _ {t} ] = a (b - \mathbf {E} [ r _ {t} ]) \mathrm{d} t.
$$

Let $\boldsymbol { h } ( t ) = \mathbf { E } [ \boldsymbol { r } _ { t } ]$ . Then $h ^ { \prime } ( t ) = a ( b - h ( t ) )$ . Solving this ODE gives

$$
h (t) = \mathbf {E} [ r _ {t} ] = b + (r _ {0} - b) e ^ {- a t}.
$$

Applying Itô’s lemma to $g ( r _ { t } )$ with $g ( x ) = x ^ { 2 }$ , we obtain

$$
\mathrm{d} \left(r _ {t} ^ {2}\right) = 2 r _ {t} \mathrm{d} r _ {t} + \frac {1}{2} * 2 * \sigma^ {2} r _ {t} \mathrm{d} t = 2 r _ {t} (a (b - r _ {t}) \mathrm{d} t + \sigma \sqrt {r _ {t}} \mathrm{d} B _ {t}) + \sigma^ {2} r _ {t} \mathrm{d} t
$$

$$
= \left((2 a b + \sigma^ {2}) r _ {t} - 2 a r _ {t} ^ {2}\right) \mathrm{d} t + 2 \sigma r _ {t} \sqrt {r _ {t}} \mathrm{d} B _ {t}.
$$

Taking expectation, we have

$$
\mathrm{d} \mathbf {E} \left[ r _ {t} ^ {2} \right] = \left(\left(2 a b + \sigma^ {2}\right) \mathbf {E} \left[ r _ {t} \right] - 2 a \mathbf {E} \left[ r _ {t} ^ {2} \right]\right) \mathrm{d} t.
$$

After subtracting

$$
\mathrm{d} \left((\mathbf {E} [ r _ {t} ]) ^ {2}\right) = 2 \mathbf {E} [ r _ {t} ] \mathrm{d} \mathbf {E} [ r _ {t} ] = (2 a b \mathbf {E} [ r _ {t} ] - 2 a (\mathbf {E} [ r _ {t} ]) ^ {2}) \mathrm{d} t,
$$

we deduce

$$
\mathrm{d} \mathbf {V a r} (r _ {t}) = \mathrm{d} (\mathbf {E} [ r _ {t} ^ {2} ]) - \mathrm{d} ((\mathbf {E} [ r _ {t} ]) ^ {2}) = (\sigma^ {2} \mathbf {E} [ r _ {t} ] - 2 a \mathbf {V a r} (r _ {t})) \mathrm{d} t.
$$

Write $f ( t ) = \mathbf { V } \mathbf { a r } ( r _ { t } )$ . Then

$$
\mathrm{d} f (t) = (\sigma^ {2} \mathbf {E} [ r _ {t} ] - 2 a f (t)) \mathrm{d} t,
$$

or

$$
\mathrm{d} (e ^ {2 a t} f (t)) = e ^ {2 a t} \mathrm{d} f (t) + 2 a f (t) e ^ {2 a t} \mathrm{d} t = \sigma^ {2} e ^ {2 a t} {\bf E} [ r _ {t} ] \mathrm{d} t = (\sigma^ {2} b e ^ {2 a t} + (r _ {0} - b) \sigma^ {2} e ^ {a t}) \mathrm{d} t.
$$

Integrating from 0 to t yields

$$
e ^ {2 a t} f (t) = f (0) + \int_ {0} ^ {t} (\sigma^ {2} b e ^ {2 a s} + (r _ {0} - b) \sigma^ {2} e ^ {a s}) \mathrm{d} s = \frac {\sigma^ {2} b}{2 a} (e ^ {2 a t} - 1) + \frac {\sigma^ {2} (r _ {0} - b)}{a} (e ^ {a t} - 1).
$$

Hence,

$$
\mathbf {V a r} (r _ {t}) = f (t) = \frac {\sigma^ {2} b}{2 a} (1 - e ^ {- 2 a t}) + \frac {\sigma^ {2} (r _ {0} - b)}{a} (e ^ {- a t} - e ^ {- 2 a t}).
$$