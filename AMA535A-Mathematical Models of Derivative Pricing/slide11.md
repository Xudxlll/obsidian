# AMA535: Mathematics of Derivative Pricing AMA535A: Mathematical Models of Derivative Pricing

XU, Zuo Quan

The Hong Kong Polytechnic University

# Interest Rate Model

# Background

Let r denote the short rate. Let $\textstyle P ( t , T )$ be the price at time t of the zero-coupon bond with par value 1 and maturing at T . Then we have

$$
P (t, T) = \mathbb {E} ^ {Q} \left[ e ^ {- \int_ {t} ^ {T} r _ {s} \mathrm{d} s} \right].
$$

Here $\mathbb { E } ^ { Q }$ is the exception in the risk-neutral world.

Let $R ( t , T )$ be the yield-to-maturity of the bond, then

$$
R (t, T) = - \frac {1}{T - t} \ln \left(\mathbb {E} ^ {Q} \left[ e ^ {- \int_ {t} ^ {T} r _ {s} \mathrm{d} s} \right]\right).
$$

# One-Factor Equilibrium Model

In one-factor equilibrium model, the process for short rate r only involves one source of uncertainty. Usually the risk-neutral process for the short rate is described by an Itô process of the form

$$
\mathrm{d} r _ {t} = \mu (r _ {t}) \mathrm{d} t + \sigma (r _ {t}) \mathrm{d} B _ {t} ^ {Q}.
$$

The instantaneous drift $\mu$ and instantaneous standard deviation $\sigma$ are assumed to be functions of $r$ but independent of time.

# Rendleman and Bartter Model

In Rendleman and Bartter’s model, the risk-neutral process for r is

$$
\mathrm{d} r _ {t} = \mu r _ {t} \mathrm{d} t + \sigma r _ {t} \mathrm{d} B _ {t} ^ {Q}.
$$

The short rate behaves like a stock price is a natural starting point but is less ideal. One important difference between interest rate and stock price is that interest rates appear to be pulled back to some long-term average level over time. This phenomenon is known as mean reversion.

# Vasicek Model

In this model, the risk-neutral process for r is

$$
\mathrm{d} r _ {t} = a (b - r _ {t}) \mathrm{d} t + \sigma \mathrm{d} B _ {t} ^ {Q}.
$$

where a, b, and @ are constants. This model incorporates mean reversion.

# Vasicek Model

Ornstein - Uhlenbeck   
![](images/c65cc03598ac4b0de8c9c7ce0c3904739dcc0d3b02143765ab7d2eea49432fb7.jpg)

<details>
<summary>line</summary>

| x    | X₀=2   | X₀-N(μ-1)/2θ² | X₀=0   |
| ---- | ------ | ------------- | ------ |
| 0.0  | 2.0    | 1.1           | 0.0    |
| 0.5  | 1.6    | 1.1           | 0.4    |
| 1.0  | 1.4    | 1.2           | 0.7    |
| 1.5  | 1.3    | 1.3           | 0.9    |
| 2.0  | 1.2    | 1.3           | 1.0    |
</details>

# Vasicek Model

In this model, the zero-coupon price is determined by

$$
P (t, T) = A (t, T) e ^ {- B (t, T) r _ {t}},
$$

where $B ( t , T ) = T - t ,$ , and $A ( t , T ) = \exp ( \sigma ^ { 2 } ( T - t ) ^ { 3 } / 6 )$ when $a = 0$ , and

$$
A (t, T) = \exp \left(\frac {(B (t , T) + t - T) (a ^ {2} b - \sigma^ {2} / 2)}{a ^ {2}} - \frac {\sigma^ {2} B ^ {2} (t , T)}{4 a}\right),
$$

and

$$
B (t, T) = \frac {1 - e ^ {- a (T - t)}}{a},
$$

when $a \neq 0$ . Moreover, the bond yield is

$$
R (t, T) = - \frac {\ln A (t , T)}{T - t} + \frac {B (t , T)}{T - t} r _ {t}.
$$

The shape of it can be increasing, decreasing, or slightly humped.

# Cox, Ingersoll, and Ross Model

In Vasicek’s model the interest rate can become negative. Cox, Ingersoll, and Ross have proposed an alternative where the interest rate is always non-negative. The risk-neutral process for r in their model is

$$
\mathrm{d} r _ {t} = a (b - r _ {t}) \mathrm{d} t + \sigma \sqrt {r _ {t}} \mathrm{d} B _ {t} ^ {Q}.
$$

# Cox, Ingersoll, and Ross Model

In this model, the zero-coupon price is determined by

$$
P (t, T) = A (t, T) e ^ {- B (t, T) r _ {t}},
$$

where

$$
A (t, T) = \left(\frac {2 \gamma e ^ {(a + \gamma) (T - t) / 2}}{(\gamma + a) (e ^ {\gamma (T - t)} - 1) + 2 \gamma}\right) ^ {2 a b / \sigma^ {2}},
$$

and

$$
B (t, T) = \frac {2 (e ^ {\gamma (T - t)} - 1)}{(\gamma + a) (e ^ {\gamma (T - t)} - 1) + 2 \gamma}.
$$

Both in Vasicek model and CIR model, the long rate $R ( t , T )$ is linearly dependent on $r _ { t }$ . This means that the value of $r _ { t }$ determines the level of the term structure at time t. The shape of the term structure at time t is independent of $r _ { t }$ , but does depend on t.

# Background

The equilibrium models do not automatically fit today’s term structure of interest rates. A 1% error in the price of the underlying bond may lead to a 25% error in an option price.

No-arbitrage models are designed to be exactly consistent with today’s term structure of interest rates.

# Ho-Lee Model

Ho and Lee proposed the first no-arbitrage model of term structure in 1986. They presented it in the form of a binomial tree of bond price. The continuous limit of the model is

$$
\mathrm{d} r _ {t} = \theta (t) \mathrm{d} t + \sigma \mathrm{d} B _ {t} ^ {Q}.
$$

The ⇠ is a function of time chosen to ensure that the model fits the initial term structure. It defines the average direction that r moves at time t. The direction is independent of the level of r.

# Ho-Lee Model

The variable ⇠(t) can be calculated by

$$
\theta (t) = F _ {t} (0, t) + \sigma^ {2} t,
$$

where $F ( 0 , t )$ is the instantaneous forward rate for a maturity t seen at time zero.

In this model, the zero-coupon price is determined by

$$
P (t, T) = A (t, T) e ^ {- (T - t) r _ {t}},
$$

where

$$
\ln A (t, T) = \ln \frac {P (0 , T)}{P (0 , t)} + (T - t) F (0, t) - \frac {1}{2} \sigma^ {2} t (T - t) ^ {2}.
$$

# Hull-White Model

Hull and White explored extensions of the Vasicek model that provide an exact fit to the initial term structure. One of the extended model is

$$
\mathrm{d} r _ {t} = (\theta (t) - a r _ {t}) \mathrm{d} t + \sigma \mathrm{d} B _ {t} ^ {Q}.
$$

When ⇠ is a constant, it becomes Vasicek model and when a = 0, it becomes Ho-Lee model.

# Hull-White Model

The variable ⇠(t) can be calculated by

$$
\theta (t) = F _ {t} (0, t) + a F (0, t) + \frac {\sigma^ {2}}{2 a} (1 - e ^ {- 2 a t}).
$$

In this model, the zero-coupon price is determined by

$$
P (t, T) = A (t, T) e ^ {- B (t, T) r _ {t}},
$$

where

$$
\ln A (t, T) = \ln \frac {P (0 , T)}{P (0 , t)} + B (t, T) F (0, t) - \frac {\sigma^ {2}}{4 a ^ {3}} (e ^ {- a t} - e ^ {- a T}) ^ {2} (e ^ {2 a t} - 1),
$$

and

$$
B (t, T) = \frac {1 - e ^ {- a (T - t)}}{a}.
$$

# Black-Derman-Toy Model

The model was introduced by Black, Derman, and Toy. The model fits both the current term structure of interest rates (yield curve), and the volatility structure.

$$
\mathrm{d} \ln (r _ {t}) = (\theta (t) - \sigma^ {\prime} (t) \sigma^ {- 1} (t) \ln (r _ {t})) \mathrm{d} t + \sigma (t) \mathrm{d} B _ {t} ^ {Q}.
$$

If @(t) is a constant @, then it becomes

$$
\mathrm{d} \ln (r _ {t}) = \theta (t) \mathrm{d} t + \sigma \mathrm{d} B _ {t} ^ {Q}.
$$

# Option on Bond

We can evaluate options on zero-coupon bonds analytically. For the Vasicek, Ho-Lee, and Hull-White models, the price at time zero of a call option that matures at time $T _ { 1 }$ on a zero-coupon bond maturing at time $T _ { 2 } > T _ { 1 }$ is

$$
L P (0, T _ {2}) N \left(h _ {1}\right) - K P (0, T _ {1}) N \left(h _ {2}\right)
$$

Where L is the principle of the bond, K is the strike price, and

$$
h _ {1, 2} = \frac {\ln \left(\frac {L P (0 , T _ {2})}{K P (0 , T _ {1})}\right) \pm \frac {\sigma_ {p} ^ {2}}{2} T _ {1}}{\sigma_ {p} \sqrt {T _ {1}}}.
$$

In the case of Vasicek, and Hull-White models,

$$
\sigma_ {p} = \sigma \frac {1 - e ^ {- a (T _ {2} - T _ {1})}}{a} \sqrt {\frac {1 - e ^ {- 2 a T _ {1}}}{2 a T _ {1}}}.
$$

# Option on Bond

The corresponding price of a put option on the bond is

$$
K P (0, T _ {1}) N (- h _ {2}) - L P (0, T _ {2}) N (- h _ {1}).
$$