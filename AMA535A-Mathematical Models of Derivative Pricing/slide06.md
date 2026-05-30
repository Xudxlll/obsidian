# AMA535: Mathematics of Derivative Pricing AMA535A: Mathematical Models of Derivative Pricing

XU, Zuo Quan

The Hong Kong Polytechnic University

# No-Arbitrage Argument

# What is Arbitrage?

# Arbitrage Opportunity

An arbitrage opportunity is a trading strategy on some [t, T ] that:

• Requires zero initial investment: ⇧(t) = 0;   
• Guarantees non-negative payoff: $\Pi ( T ) \geqslant 0 ;$   
• Has a strictly positive probability of gain: $\mathbb { P } ( \Pi ( T ) > 0 ) > 0 ;$   
where ⇧(s) is the portfolio value at time s.

# Summery

Arbitrage: Make money out of nothing, without risk.

How to find an arbitrage?

Slogan: buy low, sell high!

# Assumptions

The underlying stock price $S _ { t }$ is always positive and can take any positive value in the future.   
The stock pays no dividends during the option’s lifetime (unless otherwise stated).   
Vanilla Options: European call $C _ { E }$ ; European put $P _ { E }$ ; American call $C _ { A }$ ; American put $P _ { A }$ .

# European Call: Upper Bound

# Theorem 1

At any time t before maturity T , the price of a vanilla European call is less than the underlying stock price: $C _ { E } ( t ) < S _ { t }$ .

# Proof.

Suppose $C _ { E } ( t ) \geqslant S _ { t }$ . Portfolio: short one call, long one stock, long cash $\varepsilon = C _ { E } ( t ) - S _ { t } \geqslant 0$ . Initial value:

$$
\Pi (t) = S _ {t} - C _ {E} (t) + \varepsilon = 0.
$$

At T :

$$
\Pi (T) = S _ {T} - C _ {E} (T) + \varepsilon e ^ {r (T - t)} = \min \{S _ {T}, K \} + \varepsilon e ^ {r (T - t)} > 0.
$$

Arbitrage exists contradiction.

# European Options: Strike Price Spread

# Theorem 2

For $0 < K _ { 1 } < K _ { 2 }$ , one has

$$
0 <   C _ {E} (t, K _ {1}) - C _ {E} (t, K _ {2}) <   (K _ {2} - K _ {1}) e ^ {- r (T - t)},
$$

$$
0 <   P _ {E} (t, K _ {2}) - P _ {E} (t, K _ {1}) <   (K _ {2} - K _ {1}) e ^ {- r (T - t)}.
$$

#

Construct portfolios exploiting price differences. If bounds are violated, arbitrage exists.

# European Options: Strike Price Spread

# Proof.

Suppose $C _ { E } ( t , K _ { 1 } ) \leqslant C _ { E } ( t , K _ { 2 } )$ . Portfolio: long a call striking at $K _ { 1 }$ , long cash $\varepsilon = C _ { E } ( t , K _ { 2 } ) - C _ { E } ( t , K _ { 1 } )$ , short a call striking at $K _ { 2 }$ . Initial value: $\Pi ( t ) = C _ { E } ( t , K _ { 1 } ) - C _ { E } ( t , K _ { 2 } ) + \varepsilon = 0$ . At T ,

$$
\Pi (T) = C _ {E} (T, K _ {1}) - C _ {E} (T, K _ {2}) + \varepsilon e ^ {r (T - t)}
$$

$$
\geqslant (S _ {T} - K _ {1}) ^ {+} - (S _ {T} - K _ {2}) ^ {+}
$$

$$
= \left\{ \begin{array}{l l} 0, & \text { if } \quad S _ {T} \leqslant K _ {1}; \\ S _ {T} - K _ {1}, & \text { if } \quad K _ {1} <   S _ {T} <   K _ {2}; \\ K _ {2} - K _ {1}, & \text { if } \quad S _ {T} \geqslant K _ {2}, \end{array} \right. \geqslant 0.
$$

Also, $\Pi ( T ) > 0$ when $S _ { T } \geqslant K _ { 2 }$ . Arbitrage exists  contradiction.

![](images/4659db96d8fffde0d50e2d69940fda36de6c9ca6d78246c210d1aeb3b4789308.jpg)

# European Options: Strike Price Spread

# Proof.

Suppose $C _ { E } ( t , K _ { 1 } ) - C _ { E } ( t , K _ { 2 } ) \geqslant ( K _ { 2 } - K _ { 1 } ) e ^ { - r ( T - t ) }$ . Portfolio: long a call striking at $K _ { 2 }$ , long cash $\varepsilon = C _ { E } ( t , K _ { 1 } ) - C _ { E } ( t , K _ { 2 } )$ , short a call striking at $K _ { 1 }$ . Initial value: $\Pi ( t ) = C _ { E } ( t , K _ { 2 } ) -$ $C _ { E } ( t , K _ { 1 } ) + \varepsilon = 0$ . At T ,

$$
\begin{array}{l} \Pi (T) = C _ {E} (T, K _ {2}) - C _ {E} (T, K _ {1}) + \varepsilon e ^ {r (T - t)} \\ \geqslant (S _ {T} - K _ {2}) ^ {+} - (S _ {T} - K _ {1}) ^ {+} + (K _ {2} - K _ {1}) \\ = \left\{ \begin{array}{l l} K _ {2} - K _ {1}, & \text { if } \quad S _ {T} \leqslant K _ {1}; \\ K _ {2} - S _ {T}, & \text { if } \quad K _ {1} <   S _ {T} <   K _ {2}; \\ 0, & \text { if } \quad S _ {T} \geqslant K _ {2}, \end{array} \right. \geqslant 0. \\ \end{array}
$$

Also, $\Pi ( T ) > 0$ when $S _ { T } \leqslant K _ { 1 }$ . Arbitrage exists contradiction.

# Put-Call Parity (with Dividend)

# Theorem 3 (Put-Call Parity)

If the stock pays dividend D (valued at T ), then

$$
C _ {E} (t, K) + K e ^ {- r (T - t)} = S _ {t} - D e ^ {- r (T - t)} + P _ {E} (t, K).
$$

# Put-Call Parity (with Dividend)

# Proof.

Suppose $C _ { E } ( t , K ) + K e ^ { - r ( T - t ) } > S _ { t } - D e ^ { - r ( T - t ) } + P _ { E } ( t , K )$

Portfolio: long a stock, long a put, long cash $\varepsilon = C _ { E } ( t , K ) - S _ { t } -$ $P _ { E } ( t , K )$ , short a call. Initial value:

$$
\Pi (t) = S _ {t} + P _ {E} (t, K) - C _ {E} (t, K) + \varepsilon = 0.
$$

At T ,

$$
\begin{array}{l} \Pi (T) = S _ {T} + D + (K - S _ {T}) ^ {+} - (S _ {T} - K) ^ {+} + \varepsilon e ^ {r (T - t)} \\ = D + K + \varepsilon e ^ {r (T - t)} > 0. \\ \end{array}
$$

Arbitrage exists contradiction.

# European Call: Monotonicity in Time

# Theorem 4

For two European calls with maturities $T _ { 1 } < T _ { 2 }$ , one has

$$
C _ {E} (t, T _ {1}) <   C _ {E} (t, T _ {2}) \quad f o r t \leqslant T _ {1}.
$$

# Idea

Longer maturity provides more optionality; otherwise, arbitrage exist

# European Put: Monotonicity in Time

# Theorem 5

For two European puts with maturities $T _ { 1 } < T _ { 2 }$ and zero interest rate, one has

$$
P _ {E} (t, T _ {1}) <   P _ {E} (t, T _ {2}) \quad f o r t \leqslant T _ {1}.
$$

# Exercise

Prove the result and discuss the case when interest rate is not zero.

# American Options: Early Exercise

• An American option can be exercised at any time up to and including maturity.   
• The optimal exercise time can be determined systematically.   
At maturity T , American and European options have the same payoff:

$$
C _ {A} (T) = C _ {E} (T) = (S _ {T} - K) ^ {+}, P _ {A} (T) = P _ {E} (T) = (K - S _ {T}) ^ {+}.
$$

# Exercise

Show that American option’s value at any time is not less than its intrinsic value:

$$
C _ {A} (t) \geqslant (S _ {t} - K) ^ {+}, P _ {A} (t) \geqslant (K - S _ {t}) ^ {+}.
$$

# Bounds for American Call

# Theorem 6

For a non-dividend-paying stock, one has

$$
S _ {t} - K e ^ {- r (T - t)} <   C _ {A} (t) <   S _ {t}.
$$

# Exercise

Prove the bounds for American call.

# Merton’s Theorem

# Theorem 7 (Merton’s Theorem)

If the underlying stock pays no dividends, one has

$$
C _ {A} (t) = C _ {E} (t).
$$

# Sketch

Early exercise is never optimal for calls without dividends.

# Exercise

What happens if the underlying stock pays dividends?

# Bounds for American Put

# Theorem 8

For all t, one has

$$
P _ {A} (t) <   K.
$$

# Sketch

Otherwise, arbitrage exists by exercising the put and receiving more than strike.

# Exercise

Are American and European puts always equal? Why or why not?

# Spread Bounds for American Options

# Theorem 9

For $0 < K _ { 1 } < K _ { 2 }$ , one has

$$
0 <   C _ {A} (t, K _ {1}) - C _ {A} (t, K _ {2}) <   K _ {2} - K _ {1},
$$

$$
0 <   P _ {A} (t, K _ {2}) - P _ {A} (t, K _ {1}) <   K _ {2} - K _ {1}.
$$

# Sketch

Use European option bounds and Merton’s theorem.

# Exercise

Prove the result for American puts.