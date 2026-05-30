# Tutorial Five

1. Let $P _ { E } ( K _ { i } , T _ { i } )$ be the current price of a vanilla European put option on a nondividend paying stock striking at $K _ { i }$ maturing at $T _ { i } , i = 1 , 2$ . The two options are otherwise identical. Let r be continuously compounded interest rate. Show that $P _ { E } ( K _ { 1 } , T _ { 1 } ) < P _ { E } ( K _ { 2 } , T _ { 2 } ) { \mathrm { ~ i f ~ } } 0 < K _ { 1 } e ^ { - r T _ { 1 } } < K _ { 2 } e ^ { - r T _ { 2 } }$ and $0 < T _ { 1 } < T _ { 2 }$ .

# Solution.

Suppose $P _ { E } ( K _ { 1 } , T _ { 1 } ) ~ \geqslant ~ P _ { E } ( K _ { 2 } , T _ { 2 } )$ . Consider the following portfolio at present: long in the second option, short in the first one, and long in cash $\varepsilon = P _ { E } ( K _ { 1 } , T _ { 1 } ) -$ $P _ { E } ( K _ { 2 } , T _ { 2 } ) \ge 0$ . Then the current value of the portfolio is

$$
\Pi (0) = - P _ {E} \left(K _ {1}, T _ {1}\right) + P _ {E} \left(K _ {2}, T _ {2}\right) + \varepsilon = 0.
$$

There are two possible cases:

• The first option is exercised by the holder at $T _ { 1 }$ . Then the portfolio will be: long in a stock, the second option and cash ", debt $K _ { 1 }$ . At $T _ { 2 }$ the value of the portfolio will be

$$
\Pi (T _ {2}) = S _ {T _ {2}} + (K _ {2} - S _ {T _ {2}}) ^ {+} + \varepsilon - K _ {1} e ^ {r (T _ {2} - T _ {1})} \geqslant S _ {T _ {2}} + (K _ {2} - S _ {T _ {2}}) - K _ {1} e ^ {r (T _ {2} - T _ {1})} > 0.
$$

The first option is not exercised at $T _ { 1 }$ . Then the portfolio will be: long in the second option and cash ", whose value is nonnegative.

Note that $\Pi ( T _ { 2 } )$ is nonnegative all the time and can be positive sometime. This leads to an arbitrage opportunity.

2. Three vanilla American call options written on a non-dividend-paying stock are identical except for their strike prices which are \$10, \$20, \$40, respectively. Suppose their present prices are $\$ 6$ , \$n, \$3 in the market, respectively. If n is an integer, find its value and prove your claim.

# Solution.

The stock pays no dividend, so by Merton’s Theorem, the vanilla American call options are the same as their European counterparts. Because the call option price should be decreasing with respective to its strike price, so $3 < n < 6$ . So $n = 4$ or 5 as it is an integer.

Suppose $n = 5$ . Make a portfolio: Long in 2 options striking at 10 and 1 striking at 40, short in 3 striking at 20. Then the initial value of this portfolio is $2 ^ { * } 6 + 3 \substack { - 3 ^ { * } 5 = 0 }$ .

At maturity date, the value will be

$$
2 (S _ {T} - 1 0) ^ {+} + (S _ {T} - 4 0) ^ {+} - 3 (S _ {T} - 2 0) ^ {+} = \left\{ \begin{array}{l l} 0, & S _ {T} \leqslant 1 0; \\ 2 (S _ {T} - 1 0), & 1 0 <   S _ {T} \leqslant 2 0; \\ 4 0 - S _ {T}, & 2 0 <   S _ {T} <   4 0; \\ 0, & S _ {T} \geqslant 4 0, \end{array} \right.
$$

which will be always nonnegative and positive when $1 0 < S _ { T } < 4 0$ . This leads to an arbitrage opportunity. So we conclude that $n = 4$ .

3. Suppose a vanilla European call option price is \$5 higher than its put counterpart. Their strike price is \$105 and they are both one-year to maturity. The non-dividend paying underlying stock price is \$100 now. What is the one-year zero rate?

# Solution.

Let $r _ { 1 }$ be the one-year zero rate with continuous compounding. Then by the put-call parity, we have

$$
1 0 0 = 5 + 1 0 5 e ^ {- r _ {1}}.
$$

Therefore $r _ { 1 } = 1 0 . 0 \%$ with continuously compounding.

4. Suppose two vanilla American put options are identical except for the strike prices $0 < K _ { 1 } < K _ { 2 }$ . Please use no-arbitrate argument to show that, at any time t before maturity T ,

$$
P _ {A} (t, K _ {2}) - P _ {A} (t, K _ {1}) <   K _ {2} - K _ {1}.
$$

# Solution.

Suppose $P _ { A } ( t , K _ { 2 } ) - P _ { A } ( t , K _ { 1 } ) \geqslant K _ { 2 } - K _ { 1 }$ . Consider a portfolio at time t: long in the option striking at $K _ { 1 }$ and cash $\varepsilon = P _ { A } ( t , K _ { 2 } ) - P _ { A } ( t , K _ { 1 } ) \geqslant K _ { 2 } - K _ { 1 }$ , short in the option striking at $K _ { 2 }$ . The value of this portfolio at time t is

$$
\Pi (t) = P _ {A} (t, K _ {1}) - P _ {A} (t, K _ {2}) + \varepsilon = 0.
$$

If the option striking at $K _ { 2 }$ is exercised at sometime $\tau \in [ t , T ]$ by its holder, we chose to exercise the option striking at $K _ { 1 }$ at the same time. Then the portfolio becomes long in cash $K _ { 1 } - K _ { 2 }$ and ", and its value after exercising becomes

$$
\Pi (\tau) = K _ {1} - K _ {2} + \varepsilon \geqslant 0.
$$

If the option striking at $K _ { 2 }$ is never exercised. Then the portfolio at maturity

becomes long in the option striking at $K _ { 1 }$ and cash ", whose value is

$$
\Pi (T) = P _ {A} (T, K _ {1}) + \varepsilon = (K _ {1} - S _ {T}) ^ {+} + \varepsilon \geqslant 0.
$$

Because in both cases $\Pi ( T ) \geqslant 0$ , and $\mathbf P ( \Pi ( T ) > 0 ) \geqslant \mathbf P ( K _ { 1 } > S _ { T } ) > 0$ , this is an arbitrage portfolio.

5. Suppose three vanilla American put options are identical except for the strike prices $K _ { i } , i = 1 , 2 , 3$ . Please use no-arbitrate argument to show that, at any time t before maturity $T$ ,

$$
3 P _ {A} (t, K _ {2}) <   P _ {A} (t, K _ {1}) + 2 P _ {A} (t, K _ {3}),
$$

provided $3 K _ { 2 } = K _ { 1 } + 2 K _ { 3 }$ .

# Solution.

Suppose $3 P _ { A } ( t , K _ { 2 } ) \geqslant P _ { A } ( t , K _ { 1 } ) + 2 P _ { A } ( t , K _ { 3 } )$ . Consider a portfolio at time t: long in one option striking at $K _ { 1 }$ , two options striking at $K _ { 3 } ,$ , and cash $\varepsilon = 3 P _ { A } ( t , K _ { 2 } ) -$ $P _ { A } ( t , K _ { 1 } ) + 2 P _ { A } ( t , K _ { 3 } ) \geq 0$ , short in three options striking at $K _ { 2 }$ . The value of this portfolio at time t is

$$
\Pi (t) = P _ {A} (t, K _ {1}) + 2 P _ {A} (t, K _ {3}) - 3 P _ {A} (t, K _ {2}) + \varepsilon = 0.
$$

If the three options striking at $K _ { 2 }$ are exercised at sometime $\tau \in [ t , T ]$ by its holder, we chose to exercise the other options at the same time. Then the portfolio after exercising becomes long in cash $\varepsilon ,$ and its value is

$$
\Pi (\tau) = \varepsilon \geqslant 0.
$$

If the options striking at $K _ { 2 }$ are never exercised. Then the portfolio at maturity becomes long in the other options and cash ", whose value is

$$
\Pi (T) = P _ {A} (T, K _ {1}) + 2 P _ {A} (T, K _ {3}) + \varepsilon = (K _ {1} - S _ {T}) ^ {+} + 2 (K _ {3} - S _ {T}) ^ {+} + \varepsilon \geqslant 0.
$$

Because $\Pi ( T ) \geqslant 0$ in all cases, and $\mathbf P ( \Pi ( T ) > 0 ) \geqslant \mathbf P ( K _ { 1 } > S _ { T } ) > 0$ in the second case, this is an arbitrage portfolio.