# Tutorial Six

1. Consider a two-step binomial tree with six-month each step for the price of a stock paying no dividend. Suppose the stock price at time 0 is \$80. Assume the stock may go up 25% or down 20% each step and the risk-free interest rate is 10% with continuous compounding.

(a) Find the risk-neutral probability p and calculate its value.   
(b) Price a vanilla American call option on the stock with strike price \$100 maturing in one year.   
(c) Price a vanilla European put option on the stock with strike price \$100 maturing in one year.   
(d) Do the above two options satisfy the put-call parity? Explain.

# Solution.

Note $u = 1 + 2 5 \% = 1 . 2 5$ and $d = 1 - 2 0 \% = 0 . 8$ . The stock price at maturity will be $S _ { u u } = 8 0 * 1 . 2 5 ^ { 2 } = 1 2 5 , S _ { u d } = 8 0 * 1 . 2 5 * 0 . 8 = 8 0 , S _ { d d } = 8 0 * 0 . 8 ^ { 2 } = 5 1 . 2$ .

(a) Note $\Delta t = 0 . 5$ , the risk-neutral probability is

$$
p = \frac {e ^ {r \Delta t} - d}{u - d} = \frac {e ^ {10\% * 0 . 5} - 0 . 8}{1 . 2 5 - 0 . 8} = 55.84 \%.
$$

(b) The stock pays no dividend, so by Merton’s Theorem, the vanilla American call option is the same as its European counterpart. The vanilla American call option value at maturity date will be

$$
f _ {u u} = (S _ {u u} - K) ^ {+} = (1 2 5 - 1 0 0) ^ {+} = 2 5,
$$

$$
f _ {u d} = (S _ {u d} - K) ^ {+} = (8 0 - 1 0 0) ^ {+} = 0,
$$

$$
f _ {d d} = (S _ {d d} - K) ^ {+} = (5 1. 2 - 1 0 0) ^ {+} = 0.
$$

The value of the vanilla American call option now is

$$
C _ {A} = C _ {E} = e ^ {- 2 r \Delta t} (p ^ {2} f _ {u u} + 2 p (1 - p) f _ {u d} + (1 - p) ^ {2} f _ {d d})
$$

$$
= e ^ {- 10 \%} (0. 5 5 8 4 ^ {2} * 2 5) = 7. 0 5 3 4.
$$

(c) The vanilla European put option value at maturity date will be

$$
f _ {u u} = (K - S _ {u u}) ^ {+} = (1 0 0 - 1 2 5) ^ {+} = 0,
$$

$$
f _ {u d} = (K - S _ {u d}) ^ {+} = (1 0 0 - 8 0) ^ {+} = 2 0,
$$

$$
f _ {d d} = (K - S _ {d d}) ^ {+} = (1 0 0 - 5 1. 2) ^ {+} = 4 8. 8.
$$

The value of the vanilla European put option now is

$$
\begin{array}{l} P _ {E} = e ^ {- 2 r \Delta t} (p ^ {2} f _ {u u} + 2 p (1 - p) f _ {u d} + (1 - p) ^ {2} f _ {d d}) \\ = e ^ {- 10 \%} (2 * 0. 5 5 8 4 * (1 - 0. 5 5 8 4) * 2 0 + (1 - 0. 5 5 8 4) ^ {2} * 4 8. 8) = 1 7. 5 3 5 8. \\ \end{array}
$$

(d) Note

$$
P _ {E} + S = 1 7. 5 3 5 8 + 8 0 = 9 7. 5 3 5 8
$$

$$
C _ {E} + K e ^ {- r T} = 7. 0 5 3 4 + 1 0 0 * e ^ {- 1 0 \%} = 9 7. 5 3 5 8,
$$

so the put-call parity holds. This is because the vanilla American call option is the same as its European counterpart.

2. Consider a two-step binomial tree with three-month each step for the price of a stock paying no dividend. Suppose the stock price is \$100 now. The stock price will either go up \$20% or down \$20% each step. The risk-neutral probability is 60%.

(a) Determine the interest rate per annum with continuous compounding.   
(b) Pricing a European option maturing in six-month with payoff function $g ( S ) =$ $( \ln ^ { 2 } ( S ) - 2 0 ) ^ { + }$ .   
(c) Pricing an American option maturing in six-month with payoff function $g ( S ) =$ $( 2 2 - \ln ^ { 2 } ( S ) ) ^ { + }$ .   
(d) Determine the probability to early exercise in the risk-neutral world for the above American option.

# Solution.

(a) We have $u = 1 + 2 0 \% = 1 . 2$ and $d = 1 - 2 0 \% = 0 . 8$ . The risk-neutral probability is given by

$$
p = \frac {e ^ {r \Delta t _ {1}} - d}{u - d} = \frac {e ^ {r * 0 . 2 5} - 0 . 8}{1 . 2 - 0 . 8} = 60
$$

$$
\mathrm{So} r = 16 \% .
$$

(b) The stock price at maturity will be

$$
S _ {u u} = 1 0 0 * 1. 2 ^ {2} = 1 4 4,
$$

$$
S _ {u d} = S * 1. 2 * 0. 8 = 9 6,
$$

$$
S _ {d d} = 1 0 0 * 0. 8 ^ {2} = 6 4.
$$

The corresponding values of the option at maturity will be

$$
f _ {u u} = g \left(S _ {u u}\right) = \left(\ln^ {2} (1 4 4) - 2 0\right) ^ {+} = 4. 6 9 9 0,
$$

$$
f _ {u d} = g (S _ {u d}) = (\ln^ {2} (9 6) - 2 0) ^ {+} = 0. 8 3 3 3,
$$

$$
f _ {d d} = g (S _ {d d}) = (\ln^ {2} (6 4) - 2 0) ^ {+} = 0.
$$

The option price is

$$
\begin{array}{l} f = e ^ {- r T} (p ^ {2} f _ {u u} + 2 p (1 - p) f _ {u d} + (1 - p) ^ {2} f _ {d d}) \\ = e ^ {- 16 \% * 0.5} \left(0.6 ^ {2} * 4.6990 + 2 * 0.6 * (1 - 0.6) * 0.8333 + (1 - 0.6) ^ {2} * 0\right) = 1.9308. \\ \end{array}
$$

(c) The corresponding values of the option at maturity will be

$$
f _ {u u} = g (S _ {u u}) = (2 2 - \ln^ {2} (1 4 4)) ^ {+} = 0,
$$

$$
f _ {u d} = g (S _ {u d}) = (2 2 - \ln^ {2} (9 6)) ^ {+} = 1. 1 6 6 7,
$$

$$
f _ {d d} = g (S _ {d d}) = (2 2 - \ln^ {2} (6 4)) ^ {+} = 4. 7 0 3 7.
$$

The option values in three-month will be

$$
\begin{array}{l} f _ {u} = \max \left\{\left(g \left(S _ {u}\right), e ^ {- r \Delta t} \left(p * f _ {u u} + (1 - p) f _ {u d}\right) \right. \right\} \\ = \max \left\{\left(2 2 - \ln^ {2} (1 2 0)\right) ^ {+}, e ^ {- 0. 1 6 * 0. 2 5} \left(0. 6 * 0 + (1 - 0. 6) * 1. 1 6 6 7\right) \right\} \\ = \max \{0, 0. 4 4 8 4 \} = 0. 4 4 8 4, \\ f _ {d} = \max \{(g (S _ {d}), e ^ {- r \Delta t} (p * f _ {u d} + (1 - p) f _ {d d}) \} \\ = \max \left\{\left(2 2 - \ln^ {2} (8 0)\right) ^ {+}, e ^ {- 0. 1 6 * 0. 2 5} \left(0. 6 * 1. 1 6 6 7 + (1 - 0. 6) * 4. 7 0 3 7\right) \right\} \\ = \max \{2. 7 9 7 8, 2. 4 8 0 3 \} = 2. 7 9 7 8. \\ \end{array}
$$

So the current option price is

$$
\begin{array}{l} f = \max \{(g (S), e ^ {- r \Delta t} (p * f _ {u} + (1 - p) f _ {d}) \} \\ = \max \left\{\left(2 2 - \ln^ {2} (1 0 0)\right) ^ {+}, e ^ {- 0. 1 6 * 0. 2 5} \left(0. 6 * 0. 4 4 8 4 + (1 - 0. 6) * 2. 7 9 7 8\right) \right\} \\ = \max \{0. 7 9 2 4, 1. 3 3 3 7 \} = 1. 3 3 3 7. \\ \end{array}
$$

(d) From above calculation, we see that the option will be early exercised if the stock price drops to 80. The corresponding probability is $1 - p = 4 0 \%$ .