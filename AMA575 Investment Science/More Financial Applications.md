# More Financial Applications

# Optimal Liquidation Problem

To pose the optimal execution problem, we need to describe the number of shares that agent is holding (inventory), the dynamics of the mid-price, and how the agent’s market orders affect the mid-price:

• $\nu = \left( \nu _ { t } \right) _ { \{ 0 \leq t \leq T \} }$ is the trading rate, the speed at which the agent is liquidating or acquiring shares,   
• $Q ^ { \nu } = \left( Q _ { t } ^ { \nu } \right) \{ 0 \leq t \leq T \}$ is the agent’s inventory, which is clearly affected by how fast she trades,   
• $S ^ { \nu } = \left( S _ { t } ^ { \nu } \right) \left\{ 0 \leq t \leq T \right\}$ is the mid-price process,   
• $\hat { S } ^ { \nu } = \left( \hat { S } _ { t } ^ { \nu } \right) \left\{ 0 \leq t \leq T \right\}$ corresponds to the price process at which the agent can sell or purchase the asset, i.e. the execution price,   
• $X ^ { \nu } = \left( X _ { t } ^ { \nu } \right) _ { \{ 0 \leq t \leq T \} }$ is the agent’s cash process resulting from the agent’s execution strategy.

# Optimal Liquidation Problem

Whether liquidating or acquiring, the agent’s controlled inventory process is given in terms of her trading rate as follows:

$$
d Q _ {t} ^ {\nu} = \pm \nu_ {t} d t, \quad Q _ {0} ^ {\nu} = q \tag {6.1a}
$$

while the mid-price is assumed to satisfy the SDE

$$
d S _ {t} ^ {\nu} = \pm g (\nu_ {t}) d t + \sigma d W _ {t}, \quad S _ {0} ^ {\nu} = S \tag {6.1b}
$$

where

• $W = \left( W _ { t } \right) \{ 0 \leq t \leq T \}$ is a standard Brownian motion, and   
• $g : \mathbb { R } _ { + } \to \mathbb { R } _ { + }$ denotes the permanent price impact

# Optimal Liquidation Problem

The execution price satisfies the SDE

$$
\hat {S} _ {t} ^ {\nu} = S _ {t} ^ {\nu} \pm \left(\frac {1}{2} \Delta + f (\nu_ {t})\right), \quad \hat {S} _ {0} ^ {\nu} = \hat {S} \tag {6.1c}
$$

where

• $f : \mathbb { R } _ { + } \to \mathbb { R } _ { + }$ denotes the temporary price impact   
• $\Delta \geq 0$ is the bid-ask spread, assumed here to be a constant.

Equations (6.1a, 6.1b, and 6.1c) apply to both liquidation and acquisition problems, where the sign ± changes depending on whether the problem is that of liquidating (−) or acquiring (+) shares.

# Optimal Liquidation Problem

We start by discussing how an agent uses only MOs to optimally liquidate shares between t = 0 and T . We assume that the agents own trades do not affect the mid-price of the asset thus the stock’s mid-price is as in (6.1b) with $g \left( \nu _ { t } \right) = 0$ .

On the other hand, the agent’s trades have temporary impact on her own execution price because these MOs walk the LOB. We assume that the temporary impact is linear in the speed of trading so $f \left( \nu _ { t } \right) = k \nu _ { t }$ with $k > 0$ in (6.1c) and recall that the speed of trading $\nu _ { t }$ is what the agent controls.

For simplicity, we assume that the bid-ask spread $\Delta = 0$ , or equivalently, that $S _ { t }$ represents the best bid price. Finally, we also assume that the agent is adamant that all N shares are liquidated by time T .

# Optimal Liquidation Problem

The agent’s objective is to choose the rate at which she liquidates N shares so that she obtains the maximum amount of revenue from the sale, and her strategy must be such that all shares are liquidated by time T , i.e. cannot reach expiry with any inventory left. In other words the agent wishes to find, among all admissible liquidation strategies ν, the one that minimises the execution cost

$$
E C ^ {\nu} = \mathfrak {N S} _ {0} - \mathbb {E} \left[ \int_ {0} ^ {T} \hat {S} _ {t} ^ {\nu} \nu_ {t} d t \right]
$$

which is equivalent to maximising the expected revenues from the target sale of the N shares.

# Optimal Liquidation Problem

Thus the agent’s value function is

$$
H (t, S, q) = \sup _ {\nu \in \mathcal {A}} \mathbb {E} _ {t, S, q} \left[ \int_ {t} ^ {T} \left(S _ {u} - k \nu_ {u}\right) \nu_ {u} d u \right]
$$

where $\mathbb { E } _ { t , S , q } [ \cdot ]$ denotes expectation conditional on $S _ { t } = S$ and $Q _ { t } = q$ , and A is the set of admissible strategies: ${ \mathcal { F } } .$ -predictable non-negative bounded strategies. This constraint excludes repurchasing of shares and keeps the liquidation rate finite.

To solve this optimal control problem, we use the dynamic programming principle (DPP), which suggests that the value function satisfies the HJB equation

$$
\partial_ {t} H + \frac {1}{2} \sigma^ {2} \partial_ {S S} H + \sup _ {\nu} \left\{(S - k \nu) \nu - \nu \partial_ {q} H \right\} = 0 \tag {6.4}
$$

# Optimal Liquidation Problem

The agent requires that the optimal strategy liquidates all the inventory by time T , thus the value function reflects this by penalizing any terminal inventory that is not zero. So we require

$$
H (T, S, q) \stackrel {t \rightarrow T} {\longrightarrow} - \infty , \quad \text { for } \quad q > 0
$$

and

$$
H (T, S, 0) \stackrel {t \rightarrow T} {\longrightarrow} 0
$$

The first order condition applied to equation (6.4) shows that it attains a supremum at

$$
\nu^ {*} = \frac {1}{2 k} (S - \partial_ {q} H) \tag {6.5}
$$

# Optimal Liquidation Problem

which is the optimal trading speed in feedback control form. Upon substitution into the HJB equation, we obtain the non-linear partial differential equation

$$
\partial_ {t} H + \frac {1}{2} \sigma^ {2} \partial_ {S S} H + \frac {1}{4 k} (S - \partial_ {q} H) ^ {2} = 0 \tag {6.6}
$$

for the value function.

# Optimal Liquidation Problem

To guess an ansatz for the above equation, it is helpful to look at the boundary conditions. We know that if the strategy reaches the terminal date with a non-zero inventory, the value function must become arbitrarily large and negative − because the optimal strategy must ensure that all shares are liquidated. We propose that the value function be written in terms of the book value of the current inventory

(marked-to-market using the mid-price as reference) plus the excess value due to optimally liquidating the remaining shares, i.e.

$$
H (t, S, q) = q S + h (t, q) \tag {6.7}
$$

where $h ( t , q )$ is still to be determined, though we know that it must blow up as t approaches T .

# Optimal Liquidation Problem

Substituting this ansatz into the equation (6.6), we arrive at the following equation for $h ( t , q )$

$$
\partial_ {t} h + \frac {1}{4 k} \left(\partial_ {q} h\right) ^ {2} = 0
$$

Focusing on this non-linear PDE for h, we see that writing a separation of variables in the form $h ( t , q ) = q ^ { 2 } h _ { 2 } ( t )$ allows us to factor out q and obtain a simple non-linear ODE for $h _ { 2 } ( t )$ :

$$
\partial_ {t} h _ {2} + \frac {1}{k} (h _ {2}) ^ {2} = 0 \tag {6.8}
$$

which we solve by integrating between t and T to obtain

$$
h _ {2} (t) = \left(\frac {1}{h _ {2} (T)} - \frac {1}{k} (T - t)\right) ^ {- 1}
$$

# Optimal Liquidation Problem

To satisfy the terminal inventory condition $Q _ { T } ^ { \nu ^ { * } } = 0 ,$ , and also ensure that the correction $h ( t , q )$ to the book value of the outstanding shares that need to be liquidated is negative, we must have

$$
h _ {2} (t) \rightarrow - \infty \quad \text { as } \quad t \rightarrow T \tag {6.10}
$$

Returning to solving the optimal problem, we have that

$$
h _ {2} (t) = - k (T - t) ^ {- 1}
$$

# Optimal Liquidation Problem

We can then use the ansatz (6.7) to reduce (6.5) to

$$
\nu_ {t} ^ {*} = - \frac {1}{k} h _ {2} (t) Q _ {t} ^ {\nu^ {*}} \tag {6.9}
$$

then integrate $d Q _ { t } ^ { \nu ^ { * } } = - \nu _ { t } ^ { * }$ dt over [0, t] to obtain the inventory profile along the optimal strategy:

$$
\int_ {0} ^ {t} \frac {d Q _ {t} ^ {\nu^ {*}}}{Q _ {t} ^ {\nu^ {*}}} = \int_ {0} ^ {t} \frac {h _ {2} (s)}{k} d s \Rightarrow Q _ {t} ^ {\nu^ {*}} = \frac {(T - t)}{T} \mathfrak {N}
$$

# Optimal Liquidation Problem

So the optimal inventory to hold is

$$
\boxed {Q _ {t} ^ {\nu^ {*}} = \left(1 - \frac {t}{T}\right) \mathfrak {N}} \tag {6.11}
$$

and the optimal speed of trading is

$$
\boxed {\nu_ {t} ^ {*} = \frac {\mathfrak {N}}{T}} \tag {6.12}
$$

This final result for the optimal trading speed is quite simple: the shares must be liquidated at a constant rate.

# Optimal Acquisition Problem

The problem now is to acquire (not liquidate) N shares by time T , starting with $Q _ { 0 } ^ { \nu } = 0$ . As in the previous section the agent’s MOs walk the LOB so her execution price is described by (6.1c) with

$$
f (\nu) = k \nu , k > 0.
$$

Although the agent’s objective is to complete the acquisition program by time T , she allows for strategies that fall short of this target, $Q _ { T } ^ { \nu } < \mathfrak { N } ,$ , and in this case she must execute a buy MO for the remaining amount and pick up an additional penalty. This terminal inventory penalty is parameterised by $\alpha > 0$ , which includes the cost of walking the book at T and any other additional penalties that the agent must incur for the execution of the trade at the terminal date.

# Optimal Acquisition Problem

Thus, the agent’s expected costs from strategy $\nu _ { t }$ is

$$
E C ^ {\nu} = \mathbb {E} \left[ \underbrace {\int_ {t} ^ {T} \hat {S} _ {u} ^ {\nu} \nu_ {u} d u} _ {\text { Terminal   Cash }} + \underbrace {\left(\mathfrak {N} - Q _ {T} ^ {\nu}\right) S _ {T}} _ {\text { Terminal   execution   at   mid }} + \underbrace {\alpha \left(\mathfrak {N} - Q _ {T} ^ {\nu}\right) ^ {2}} _ {\text { Terminal   Penalty }} \right] \tag {6.13}
$$

In the liquidation problem, the agent seeks a strategy that ensures all shares are liquidated by T and the expected costs arise exclusively from continuous trading. Now, the agent can reach T short of her target, but this generates the additional terms that incorporate that sale plus the penalty to purchase the remaining shares at the terminal date.

# Optimal Acquisition Problem

To simplify notation, we introduce a new stochastic process

$Y = \left( Y _ { t } \right) _ { 0 < t < T }$ to denote the shares remaining to be purchased between t and the end of the trading horizon T :

$$
Y _ {t} ^ {\nu} = \mathfrak {N} - Q _ {t} ^ {\nu}, \quad \text { so   that } \quad d Y _ {t} ^ {\nu} = - \nu_ {t} d t
$$

and write the value function as

$$
H (t, S, y) = \inf _ {\nu \in \mathcal {A}} \mathbb {E} _ {t, S, y} \left[ \int_ {t} ^ {T} \hat {S} _ {u} ^ {\nu} \nu_ {u} d u + Y _ {T} ^ {\nu} S _ {T} + \alpha \left(Y _ {T} ^ {\nu}\right) ^ {2} \right]
$$

Applying the DPP, we expect that the value function should satisfy the HJB equation

$$
0 = \partial_ {t} H + \frac {1}{2} \sigma^ {2} \partial_ {S S} H + \inf _ {\nu} \left\{(S + k \nu) \nu - \nu \partial_ {y} H \right\} \tag {6.14}
$$

with terminal condition ${ \cal H } ( \bar { \cal T } , S , y ) = y S + \alpha y ^ { 2 }$ .

# Optimal Acquisition Problem

Solving for the first order condition, the optimal speed of trading in feedback form is given by

$$
\nu^ {*} = \frac {1}{2 k} \left(\partial_ {y} H - S\right) \tag {6.15}
$$

and upon substitution into the DPE above, we obtain

$$
\partial_ {t} H + \frac {1}{2} \sigma^ {2} \partial_ {S S} H - \frac {1}{4 k} (\partial_ {y} H - S) ^ {2} = 0
$$

# Optimal Acquisition Problem

To solve this equation, we can write the value function in terms of the book value of the assets remaining to be acquired and the excess value function from optimally acquiring these shares. From looking at the terminal condition, and the way y enters into the DPE, we hypothesise that the excess value function can be written in terms of a quadratic function in y. The corresponding ansatz is

$$
H (t, S, y) = y S + h _ {0} (t) + h _ {1} (t) y + h _ {2} (t) y ^ {2} \tag {6.16}
$$

where $h _ { 2 } ( t ) , h _ { 1 } ( t ) , h _ { 0 } ( t )$ are, yet to be determined, deterministic functions of time. Recalling that the value function at the terminal date T is ${ \cal H } ( \bar { \cal T } , S , y ) = y S + \alpha y ^ { 2 }$ , then

$$
h _ {2} (T) = \alpha \quad \mathrm{and} \quad h _ {1} (T) = h _ {0} (T) = 0.
$$

# Optimal Acquisition Problem

Moreover, upon substituting the ansatz into the above non-linear PDE we find that

$$
0 = \left\{\partial_ {t} h _ {2} - \frac {1}{k} h _ {2} ^ {2} \right\} y ^ {2} + \left\{\partial_ {t} h _ {1} - \frac {1}{2 k} h _ {2} h _ {1} \right\} y + \left\{\partial_ {t} h _ {0} - \frac {1}{4 k} h _ {1} ^ {2} \right\}
$$

since this equation must be valid for each y, each term in braces must individually vanish. This provides us with three equations for the three functions $h _ { 0 } , h _ { 1 }$ and $h _ { 2 }$ . Due to the terminal condition $h _ { 1 } ( T ) = 0$ , we see that the solution we get for $h _ { 1 }$ (by setting the second term in braces to zero) is $h _ { 1 } ( t ) = 0$ .

# Optimal Acquisition Problem

Similarly, due to the terminal condition $h _ { 0 } ( T ) = 0$ , we see that the solution we get for $h _ { 0 }$ (by setting the third term in braces to zero, and knowing that $h _ { 1 } ( t ) = 0 )$ is $h _ { 0 } ( t ) = 0$ . Indeed we could have begun with the ansatz $H ( t , S , y ) = y S + h _ { 2 } ( t ) y ^ { 2 }$ and have ended up with the same equation for $h _ { 2 }$ . The final equation (obtained by setting the first term in braces to zero) allows us to obtain $h _ { 2 } ( t )$ and in this case, since $h _ { 2 } ( T ) = \alpha$ , we obtain the non-trivial solution

$$
h _ {2} (t) = \left(\frac {1}{k} (T - t) + \frac {1}{\alpha}\right) ^ {- 1}
$$

# Optimal Acquisition Problem

Putting this together with the ansatz for the value function we find that the optimal trading speed is

$$
\nu_ {t} ^ {*} = \left((T - t) + \frac {k}{\alpha}\right) ^ {- 1} Y _ {t} ^ {\nu^ {*}} \tag {6.17}
$$

Here we see that as the terminal penalty parameter $\alpha \to \infty$ the acquisition rate converges to that of TWAP. Similarly, the smaller the value of $\alpha ,$ all else being equal, the slower the acquisition rate will be. Furthermore, in the limiting case $\alpha  0$ , the optimal strategy is not to purchase any shares until the terminal date is reached, at which point all N shares are purchased. In this limiting case, there are no costs of walking the book at date T , so it is optimal to purchase all the inventory at the end. In general, however, we expect that $\alpha \gg k$ .

# Optimal Acquisition Problem

As before, we can solve for the optimal inventory path explicitly by integrating $d Y _ { t } ^ { \nu ^ { * } } = - \nu _ { t } ^ { * }$ dt over [0, t ], i.e. by solving

$$
d Y _ {t} ^ {\nu^ {*}} = - \left((T - t) + \frac {k}{\alpha}\right) ^ {- 1} Y _ {t} ^ {\nu^ {*}} d t
$$

for $Y _ { t } ^ { \nu ^ { * } }$ . Recalling that $Y _ { t } ^ { \nu } = \mathfrak { N } - Q _ { t } ^ { \nu }$ , it is straightforward to obtain the optimal inventory path as

$$
\boxed {Q _ {t} ^ {\nu^ {*}} = \frac {t}{T + \frac {k}{\alpha}} \Re} \tag {6.18}
$$

# Optimal Acquisition Problem

From this equation we can see that for any finite $\alpha > 0$ and finite $k > 0$ , it is always optimal to leave some shares to be executed at the terminal date, and the fraction of shares left to execute at the end decreases with the relative price impact at the terminal date, $k / \alpha$ .

To obtain the optimal speed of acquisition, we substitute for $Q _ { t } ^ { \nu ^ { * } }$ into the expression for $\nu _ { t } ^ { * }$ , so that

$$
\boxed {\nu_ {t} ^ {*} = \frac {\mathfrak {N}}{T + \frac {k}{\alpha}}} \tag {6.19}
$$

# Liquidation with Permanent Price Impact

The agent continues to use only MOs to liquidate a total of N shares, but now her trades have both a temporary and a permanent price impact. The mid-price dynamics are given by (6.1b) with drift $g \left( \nu _ { t } \right) > 0$ , which enters the equation with negative sign because the agent’s sell trades exert a permanent downward pressure, and the execution price by (6.1c) with $f \left( \nu _ { t } \right) > 0$ , which enters the equation with a negative sign because the sell trades have an adverse temporary impact. Here we assume that if the agent’s strategy reaches the terminal date T with inventory left, then she must execute an MO to reach N for a total revenue of $Q _ { T } ^ { \nu } \left( S _ { T } ^ { \nu } - \alpha Q _ { T } ^ { \nu } \right)$ , where $\alpha \geq 0$ is the terminal liquidation penalty parameter.

# Liquidation with Permanent Price Impact

The agent’s objective is to minimise the execution cost

$$
E C ^ {\nu} = \mathfrak {N S} _ {0} - \mathbb {E} \left[ \underbrace {X _ {T} ^ {\nu}} _ {\text {Terminal Cash}} + Q _ {T} ^ {\nu} \left(\underbrace {S _ {T} ^ {\nu}} _ {\text {Midprice}} - \underbrace {\alpha Q _ {T} ^ {\nu}} _ {\text {Penalty per Share}}\right) \right]
$$

where the process corresponding to the investor’s wealth $X _ { t } ^ { \nu }$ is as in (6.2).

# Liquidation with Permanent Price Impact

In this problem, we also introduce another element into the model: a running inventory penalty of the form $\phi \int _ { t } ^ { T } \left( Q _ { u } ^ { \nu } \right) ^ { 2 }$ with $\phi \geq 0$ . This running inventory penalty is not (and should not be considered) a financial cost to the agent’s strategy. The parameter $\phi$ allows us to incorporate the agent’s urgency for executing the trade. The higher the value of $\phi$ , the quicker the optimal strategy liquidates the shares, as it increases the penalty for the late liquidation of shares and incentivises strategies that front load the liquidation of inventory.

# Liquidation with Permanent Price Impact

Then, the agent’s performance criterion is

$$
H ^ {\nu} (t, x, S, q) = \mathbb {E} _ {t, x, S, q} \left[ \underbrace {X _ {\mathcal {I}} ^ {\nu}} _ {\text { Terminal   Cash }} + \underbrace {Q _ {T} ^ {\nu} \left(S _ {T} ^ {\nu} - \alpha Q _ {T} ^ {\nu}\right)} _ {\text { Terminal   Execution }} - \underbrace {\phi \int_ {t} ^ {T} \left(Q _ {u} ^ {\nu}\right) ^ {2} d u} _ {\text { Inventory }} \right] \tag {6.20}
$$

and the value function

$$
H (t, x, S, q) = \sup _ {\nu \in \mathcal {A}} H ^ {\nu} (t, x, S, q)
$$

# Liquidation with Permanent Price Impact

The DPP implies that the value function should satisfy the HJB equation

$$
\begin{array}{l} 0 = \left(\partial_ {t} + \frac {1}{2} \sigma^ {2} \partial_ {S S}\right) H - \phi q ^ {2} \\ + \sup _ {\nu} \left\{\left(\nu (S - f (\nu)) \partial_ {x} - g (\nu) \partial_ {S} - \nu \partial_ {q}\right) H \right\} \end{array} \tag {6.21}
$$

subject to the terminal condition $H ( \boldsymbol { T } , \boldsymbol { x } , \boldsymbol { S } , \boldsymbol { q } ) = \boldsymbol { x } + \boldsymbol { S } \boldsymbol { q } - \alpha \boldsymbol { q } ^ { 2 }$

# Liquidation with Permanent Price Impact

We use the simplifying assumption that permanent and temporary price im- pact functions are linear in the speed of trading, i.e. $f ( \nu ) = k \nu$ and $g ( \nu ) = b \nu$ for finite constants $k \geq 0$ and $b \geq 0$ . The first order condition allows us to obtain the optimal speed of trading in feedback control form as

$$
\nu^ {*} = \frac {1}{2 k} \frac {\left(S \partial_ {x} - b \partial_ {S} - \partial_ {q}\right) H}{\partial_ {x} H} \tag {6.22}
$$

# Liquidation with Permanent Price Impact

Upon substituting the optimal feedback control into the DPE, it reduces to

$$
0 = \left(\partial_ {t} + \frac {1}{2} \sigma^ {2} \partial_ {S S}\right) H - \phi q ^ {2} + \frac {1}{4 k} \frac {\left[ (S \partial_ {x} - b \partial_ {S} - \partial_ {q}) H \right] ^ {2}}{\partial_ {x} H}
$$

By inspecting the terminal condition $H ( \boldsymbol { T } , \boldsymbol { x } , \boldsymbol { S } , \boldsymbol { q } ) = \boldsymbol { x } + \boldsymbol { S } \boldsymbol { q } - \alpha \boldsymbol { q } ^ { 2 }$ , it suggests the ansatz

$$
H (t, x, S, q) = x + S q + h (t, S, q) \tag {6.23}
$$

where h, with terminal condition $h ( T , S , q ) = - \alpha q ^ { 2 }$ , is yet to be determined. The first term of the ansatz is the accumulated cash of the strategy, the second is the marked-to-market book value (at midprice) of the remaining inventory, and h is the extra value stemming from optimally liquidating the rest of the shares.

# Liquidation with Permanent Price Impact

Using this ansatz in the equation above and simplifying, we find the following non-linear PDE for h :

$$
0 = \left(\partial_ {t} + \frac {1}{2} \sigma^ {2} \partial_ {S S}\right) h - \phi q ^ {2} + \frac {1}{4 k} \left[ b (q + \partial_ {S} h) + \partial_ {q} h \right] ^ {2}
$$

since the above PDE contains no explicit dependence on S and the terminal condition is independent of S, it follows that $\partial _ { S } h ( t , S , q ) = 0$ , and we can write $h ( t , S , q ) = h ( t , q )$ . The equation then simplifies even further to

$$
0 = \partial_ {t} h (t, q) - \phi q ^ {2} + \frac {1}{4 k} [ b q + \partial_ {q} h (t, q) ] ^ {2}
$$

# Liquidation with Permanent Price Impact

Furthermore, the optimal control in feedback form from (6.22) takes on the much more compact form

$$
\nu^ {*} = - \frac {1}{2 k} (\partial_ {q} h (t, q) + b q) \tag {6.24}
$$

In this form, it appears that the solution admits a separation of variables $h ( t , q ) = h _ { 2 } ( t ) q ^ { 2 }$ where $h _ { 2 } ( t )$ satisfies the non-linear ODE (recall that the subscript 2 represents that this function is the coefficient of $q ^ { 2 } )$

$$
0 = \partial_ {t} h _ {2} - \phi + \frac {1}{k} \left[ h _ {2} + \frac {1}{2} b \right] ^ {2} \tag {6.25}
$$

subject to the terminal condition $h _ { 2 } ( T ) = - \alpha$

# Liquidation with Permanent Price Impact

This ODE is of Riccati type and can be integrated exactly. First, let $\begin{array} { r } { h _ { 2 } ( t ) = - \frac { 1 } { 2 } b + \chi ( t ) } \end{array}$ , then re-arranging the ODE we obtain

$$
\frac {\partial_ {t} \chi}{k \phi - \chi^ {2}} = \frac {1}{k}
$$

subject to $\chi ( T ) = { \textstyle { \frac { 1 } { 2 } } } b - \alpha$ .

# Liquidation with Permanent Price Impact

Next, integrating both sides of the above over [t, T ] yields

$$
\log \frac {\sqrt {k \phi} + \chi (T)}{\sqrt {k \phi} - \chi (T)} - \log \frac {\sqrt {k \phi} + \chi (t)}{\sqrt {k \phi} - \chi (t)} = 2 \gamma (T - t)
$$

so that

$$
\chi (t) = \sqrt {k \phi} \frac {1 + \zeta e ^ {2 \gamma (T - t)}}{1 - \zeta e ^ {2 \gamma (T - t)}}
$$

where

$$
\gamma = \sqrt {\frac {\phi}{k}} \text {   and   } \zeta = \frac {\alpha - \frac {1}{2} b + \sqrt {k \phi}}{\alpha - \frac {1}{2} b - \sqrt {k \phi}} \tag {6.26}
$$

# Liquidation with Permanent Price Impact

At this point the solution of the DPE is fully determined and the optimal speed of trading can now be explicitly shown in terms of the state variables rather than in feedback form. Specifically, from ( 6.24), the optimal speed to trade at is

$$
\boxed {\nu_ {t} ^ {*} = \gamma \frac {\zeta e ^ {\gamma (T - t)} + e ^ {- \gamma (T - t)}}{\zeta e ^ {\gamma (T - t)} - e ^ {- \gamma (T - t)}} Q _ {t} ^ {\nu^ {*}}} \tag {6.27}
$$

Interestingly, the optimal speed to trade is still proportional to the investor’s current inventory level, as we found in the previous simpler models, but now the proportionality factor depends non-linearly on time.

# Liquidation with Permanent Price Impact

From this expression, it is also possible to obtain the agent’s inventory $Q _ { t } ^ { \nu ^ { * } }$ that results from following this strategy. Recall that the agent’s inventory satisfies $d Q _ { t } ^ { \nu } = - \nu _ { t } d t$ , hence

$$
d Q _ {t} ^ {\nu^ {*}} = \frac {\chi (t)}{k} Q _ {t} ^ {\nu^ {*}} d t \quad \text { so   that } \quad Q _ {t} ^ {\nu^ {*}} = \mathfrak {N} \exp \left\{\int_ {0} ^ {t} \frac {\chi (s)}{k} d s \right\}
$$

# Liquidation with Permanent Price Impact

To obtain the inventory along the optimal strategy we first solve the integral

$$
\begin{array}{l} \int_ {0} ^ {t} \frac {\chi (s)}{k} d s = \frac {1}{k} \int_ {0} ^ {t} \sqrt {k \phi} \frac {1 + \zeta e ^ {2 \gamma (T - s)}}{1 - \zeta e ^ {2 \gamma (T - s)}} d s \\ = \gamma \int_ {0} ^ {t} \frac {e ^ {- 2 \gamma (T - s)}}{e ^ {- 2 \gamma (T - s)} - \zeta} d s + \gamma \int_ {0} ^ {t} \frac {\zeta e ^ {2 \gamma (T - s)}}{1 - \zeta e ^ {2 \gamma (T - s)}} d s \\ = \log \left. \left(e ^ {- \gamma (T - s)} - \zeta e ^ {\gamma (T - s)}\right) \right| _ {0} ^ {t} \\ = \log \frac {\zeta e ^ {\gamma (T - t)} - e ^ {- \gamma (T - t)}}{\zeta e ^ {\gamma T} - e ^ {- \gamma T}} \\ \end{array}
$$

# Liquidation with Permanent Price Impact

Hence

$$
\boxed {Q _ {t} ^ {\nu^ {*}} = \frac {\zeta e ^ {\gamma (T - t)} - e ^ {- \gamma (T - t)}}{\zeta e ^ {\gamma T} - e ^ {- \gamma T}} \mathfrak {N}}
$$

Substituting this expression into (6.27) allows us to write the optimal speed to trade as a simple deterministic function of time

$$
\nu_ {t} ^ {*} = \gamma \frac {\zeta e ^ {\gamma (T - t)} + e ^ {- \gamma (T - t)}}{\zeta e ^ {\gamma T} - e ^ {- \gamma T}} \mathfrak {N}
$$

# Liquidation with Permanent Price Impact

In the limit in which the quadratic liquidation penalty goes to infinity, i.e. as α → +∞, we get ζ → 1. Then, the optimal inventory to hold and the optimal speed to trade simplify to

$$
Q _ {t} ^ {\nu^ {*}} \xrightarrow [ \alpha \to + \infty ]{} \frac {\sinh (\gamma (T - t))}{\sinh (\gamma T)} \mathfrak {N}
$$

and

$$
\nu_ {t} ^ {*} \xrightarrow [ \alpha \to + \infty ]{} \gamma \frac {\cosh (\gamma (T - t))}{\sinh (\gamma T)} \mathfrak {N}
$$

Both of these expressions are independent of b. For other values of α the relationship between α and the permanent price impact parameter b is more complex and we look at it after considering some numerical examples.