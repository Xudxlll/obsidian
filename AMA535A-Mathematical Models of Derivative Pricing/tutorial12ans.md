# Tutorial Twelve

1. Suppose the Black-Scholes framework holds. Suppose S = 100, T - t = 1, $\sigma = 20\%$ , K = 100, $r = 10\%$ per annum with continuous compounding.

(a) Calculate the vanilla European call and put option prices by the Black-Scholes formulae.   
(b) Verify the put call parity.   
(c) Calculate the put potion price by a three-step binomial-tree model.

# SOLUTION.

(a) The Black-Scholes formulae are

$$
\begin{array}{l} C _ {E} (t, x) = x N \left(d _ {1}\right) - K e ^ {- r (T - t)} N \left(d _ {2}\right), \\ P _ {E} (t, x) = K e ^ {- r (T - t)} N (- d _ {2}) - x N (- d _ {1}), \\ \end{array}
$$

where

$$
\begin{array}{l} N (x) = \frac {1}{\sqrt {2 \pi}} \int_ {- \infty} ^ {x} e ^ {- \frac {1}{2} z ^ {2}} \mathrm{d} z, \\ d _ {1} = \frac {\ln (x / K) + (r + \frac {1}{2} \sigma^ {2}) (T - t)}{\sigma \sqrt {T - t}}, \\ d _ {2} = \frac {\ln (x / K) + (r - \frac {1}{2} \sigma^ {2}) (T - t)}{\sigma \sqrt {T - t}} = d _ {1} - \sigma \sqrt {T - t}. \\ \end{array}
$$

We have $d_{1}=0.6$ , $d_{2}=0.4$ , $N(d_{1})=0.7257$ , $N(d_{2})=0.6554$ , so $C_{E}(t,100)=13.27$ and $P_{E}(t,100)=3.75$ .

(b) The put call parity is

$$
C _ {E} (t, x) + K e ^ {- r (T - t)} = P _ {E} (t, x) + x.
$$

(c) Note $\Delta t = 1/3$ , $\sigma = 20\%$ , so $u = e^{\sigma \sqrt{\Delta t}} = e^{20\% \sqrt{1/3}} = 1.1224$ and $d = 1/u = 0.89095$ . The risk-neutral probability is

$$
p = \frac {e ^ {r \Delta t} - d}{u - d} = \frac {e ^ {10\% * 1 / 3} - 0 . 8 9 0 9 5}{1 . 1 2 2 4 - 0 . 8 9 0 9 5} = 61.76 \%.
$$

The stock prices at maturity will be

$$
\begin{array}{l} S _ {u u u} = 1 0 0 * 1. 2 2 1 4 ^ {3} = 1 4 1. 3 9 8, \quad S _ {u u d} = S _ {u} = 1 1 2. 2 4, \\ S _ {u d d} = S _ {d} = 8 9. 0 9 5, \quad S _ {d d d} = 1 0 0 * 0. 8 1 8 7 3 ^ {3} = 7 0. 7 2 2. \\ \end{array}
$$

The put option values at maturity will be

$$
f _ {u u u} = (K - S _ {u u u}) ^ {+} = (1 0 0 - 1 4 1. 3 9 8) ^ {+} = 0,
$$

$$
f _ {u u d} = (K - S _ {u u d}) ^ {+} = (1 0 0 - 1 1 2. 2 4) ^ {+} = 0,
$$

$$
f _ {u d d} = (K - S _ {u d d}) ^ {+} = (1 0 0 - 8 9. 0 9 5) ^ {+} = 1 0. 9 0 5,
$$

$$
f _ {d d d} = (K - S _ {d d d}) ^ {+} = (1 0 0 - 7 0. 7 2 2) ^ {+} = 2 9. 2 7 8.
$$

The value now is

$$
P _ {E} = e ^ {- 3 r \Delta t} (p ^ {3} f _ {u u u} + 3 p ^ {2} (1 - p) f _ {u u d} + 3 p (1 - p) ^ {2} f _ {u d d} + (1 - p) ^ {3} f _ {d d d})
$$

$$
= 4. 1 5 5.
$$

2. (a) Using risk-neutral valuation method to find the value at time $t$ of a forward contract with the payoff function $f(S) = \ln (S) - K$ ;

(b) Show that the value satisfies the Black-Scholes PDE.

(c) Determine the option's $\Delta$ , $\Gamma$ and $\rho$ .

# SOLUTION.

(a) In the risk-neutral world, the stock price follows

$$
\mathrm{d} S _ {t} = r S _ {t} \mathrm{d} t + \sigma S _ {t} \mathrm{d} B _ {t} ^ {Q},
$$

where $B_{t}^{Q}$ is a standard Brownian motion in the risk-neutral world. By Itô's Lemma,

$$
\mathrm{d} \left(\ln (S _ {t})\right) = \left(r - \sigma^ {2} / 2\right) \mathrm{d} t + \sigma \mathrm{d} B _ {t} ^ {Q}.
$$

$$
\ln (S _ {T}) - \ln (S _ {t}) = \int_ {t} ^ {T} (r - \sigma^ {2} / 2) \mathrm{d} s + \sigma \mathrm{d} B _ {s}
$$

$$
= \left(r - \frac {1}{2} \sigma^ {2}\right) (T - t) + \sigma \left(B _ {T} ^ {Q} - B _ {t} ^ {Q}\right).
$$

By the risk-neutral valuation method, the value is given by the discounted

expectation of the payoff in the risk-neutral world, that is

$$
\begin{array}{l} V (t, x) = \mathbf {E} ^ {Q} [ e ^ {- r (T - t)} f (S _ {T}) | S _ {t} = x ] \\ = \mathbf {E} ^ {Q} [ e ^ {- r (T - t)} (\ln (S _ {T}) - K) | S _ {t} = x ] \\ = \mathbf {E} ^ {Q} \left[ e ^ {- r (T - t)} \left(\ln \left(S _ {t}\right) + \left(r - \frac {1}{2} \sigma^ {2}\right) (T - t) + \sigma \left(B _ {T} ^ {Q} - B _ {t} ^ {Q}\right) - K\right) \mid S _ {t} = x \right] \\ = \mathbf {E} ^ {Q} \left[ e ^ {- r (T - t)} \left(\ln (x) + \left(r - \frac {1}{2} \sigma^ {2}\right) (T - t) + \sigma \left(B _ {T} ^ {Q} - B _ {t} ^ {Q}\right) - K\right) \mid S _ {t} = x \right] \\ = e ^ {- r (T - t)} \left(\ln (x) + \left(r - \frac {1}{2} \sigma^ {2}\right) (T - t) - K + \mathbf {E} ^ {Q} \left[ \sigma \left(B _ {T} ^ {Q} - B _ {t} ^ {Q}\right) | S _ {t} = x \right]\right) \\ = e ^ {- r (T - t)} \left(\ln (x) + \left(r - \frac {1}{2} \sigma^ {2}\right) (T - t) - K + \mathbf {E} ^ {Q} \left[ \sigma \left(B _ {T} ^ {Q} - B _ {t} ^ {Q}\right) \right]\right) \\ = e ^ {- r (T - t)} \left(\ln (x) + \left(r - \frac {1}{2} \sigma^ {2}\right) (T - t) - K\right). \\ \end{array}
$$

where $E^{Q}$ means the expectation is taken in the risk-neutral world.

(b) The Black-Scholes PDE is

$$
\frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} x ^ {2} \frac {\partial^ {2} V}{\partial x ^ {2}} + r x \frac {\partial V}{\partial x} - r V = 0.
$$

Direct calculation.

$$
V _ {t} (t, x) = r V - (r - \frac {1}{2} \sigma^ {2}) e ^ {- r (T - t)},
$$

$$
V _ {x} (t, x) = \frac {1}{x} e ^ {- r (T - t)},
$$

$$
V _ {x x} (t, x) = - \frac {1}{x ^ {2}} e ^ {- r (T - t)}.
$$

Therefore,

$$
\begin{array}{l} \frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} x ^ {2} \frac {\partial^ {2} V}{\partial x ^ {2}} + r x \frac {\partial V}{\partial x} - r V \\ = r V - (r - \frac {1}{2} \sigma^ {2}) e ^ {- r (T - t)} - \frac {1}{2} \sigma^ {2} e ^ {- r (T - t)} + r e ^ {- r (T - t)} - r V = 0. \\ \end{array}
$$

(c) We have

$$
\begin{array}{l} \Delta = V _ {x} (t, x) = \frac {1}{x} e ^ {- r (T - t)}, \\ \Gamma = V _ {x x} (t, x) = - \frac {1}{x ^ {2}} e ^ {- r (T - t)}, \\ \rho = V _ {r} (t, x) = (T - t) e ^ {- r (T - t)} \bigl (1 - \left(\ln (x) + (r - \frac {1}{2} \sigma^ {2}) (T - t) - K\right) \bigr). \\ \end{array}
$$

3. A stock is selling for 10 dollars in a market. The information of derivatives A, B and C written on the stock is given below.

<table><tr><td></td><td>A</td><td>B</td><td>C</td></tr><tr><td> $\Delta$ </td><td>0.50</td><td>0.2</td><td>-0.3</td></tr><tr><td> $\Gamma$ </td><td>0.30</td><td>0.25</td><td>0.1</td></tr><tr><td>Price in dollar</td><td>0.3</td><td>0.5</td><td>0.7</td></tr></table>

A portfolio consists of long position in 100 shares of A and 300 shares of C, and short position in 100 shares of B.

(a) How many shares of the stock should you buy or sell in order to make the portfolio $\Delta$ neutral?   
(b) Continued with (a). If the stock price goes up 3%, then what is the new value of the adjusted portfolio?

# SOLUTION.

(a) The $\Delta$ of the portfolio is

$$
\Delta = 1 0 0 * 0. 5 0 - 1 0 0 * 0. 2 + 3 0 0 * (- 0. 3) = - 6 0.
$$

The $\Delta$ of each stock is 1, so we need to buy 60 shares to make the portfolio $\Delta$ neutral.

(b) Note the $\Gamma$ of the stock is zero, so the $\Gamma$ of the adjusted portfolio is

$$
\Gamma = 1 0 0 * 0. 3 0 - 1 0 0 * 0. 2 5 + 3 0 0 * 0. 1 + 6 0 * 0 = 3 5.
$$

The value of the the adjusted portfolio is

$$
V = 1 0 0 * 0. 3 - 1 0 0 * 0. 5 + 3 0 0 * 0. 7 + 6 0 * 1 0 = 7 9 0.
$$

If the stock price goes up $\delta S = 10 * 3\% = 0.3$ dollar, then the value of the adjusted portfolio will change

$$
\delta V \approx \delta S * \Delta + \frac {1}{2} (\delta S) ^ {2} \Gamma = 0. 3 * 0 + \frac {1}{2} * (0. 3) ^ {2} * 3 5 = 1. 5 7 5.
$$

So the new value is approximately $V + \delta V = 790 + 1.575 = 791.575$ .