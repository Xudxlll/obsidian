# Lecture 7: Convertible Bonds

Guanghua Lian

The Hong Kong Polytechnic University

# Contents

1 Pricing with constant interest rate 2

1.1 Delta hedging . . 2   
1.2 Conversion region and optimal conversion strategy . . 3

2 A binomial model and link to the continuous time model 3

2.1 A binomial model . . 3   
2.2 Link to the continuous time mode . . 3

3 Call and put features 4

3.1 Derivation: BTM 4   
3.2 Soft call or put 5

4 Dilution 6

5 Two-factor modeling: Pricing with stochastic interest rate 7   
6 Convertible bonds with credit risk 8

6.1 The pricing of a risky bond 8   
6.2 The pricing of convertible bonds with credit risk . 9

A convertible bond has the characteristics of a regular bond but with the extra feature that the bond may, at a time of the holders choosing, be exchanged for a specified asset. This exchange is called “conversion”. Since the conversion feature makes the convertible bond similar mathematically to American options, we expect that its pricing model is analogous to that of American options.

# 1 Pricing with constant interest rate

We continue to use S to mean the underlying asset price that follows the geometric Brownian motion:

$$
\frac {d S _ {t}}{S _ {t}} = \mu d t + \sigma d W _ {t}.
$$

Suppose that the maturity date is T and the convertible bond can be converted into n of the underlying. To introduce the ideas behind pricing convertibles, we will start by assuming that interest rate is constant during the life of the bond and there are not coupons.

# 1.1 Delta hedging

Since the bond value depends on the asset value, we have

$$
V _ {t} = V (S _ {t}, t).
$$

Construct a portfolio at time t.

$$
\Pi_ {t} = V _ {t} - \Delta S _ {t}.
$$

We assume that we hold this portfolio from t to t + dt during which conversion is prohibited. Then

$$
\begin{array}{l} d \Pi_ {t} = d V _ {t} - \Delta d S _ {t} - q \Delta S _ {t} d t \\ { = } { \left[ \frac { \partial V } { \partial t } + \frac { 1 } { 2 } \sigma ^ { 2 } S _ { t } ^ { 2 } \frac { \partial ^ { 2 } V } { \partial S ^ { 2 } } \right] d t + \frac { \partial V } { \partial S } d S _ { t } - \Delta d S _ { t } - q \Delta S _ { t } d t } \\ = \left[ \frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} S _ {t} ^ {2} \frac {\partial^ {2} V}{\partial S ^ {2}} \right] d t - q S _ {t} \frac {\partial V}{\partial S} d t \\ \leq r \Pi d t \\ \end{array}
$$

where we have chosen $\begin{array} { r } { \Delta = { \frac { \partial V } { \partial S } } } \end{array}$ . It follows

$$
\mathcal {L} V = \frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} S ^ {2} \frac {\partial^ {2} V}{\partial S ^ {2}} + (r - q) S \frac {\partial V}{\partial S} - r V \leq 0.
$$

Since the bond may be converted into n assets we have the constraint

$$
V (S, t) \geq n S.
$$

As in the case of American options, we can deduce that one of these two inequalities must hold with equality at any point of the solution domain $\{ S > 0 , t \in [ 0 , T ) \}$ . That is

$$
\begin{array}{l} - \mathcal {L} V = 0 \text {   if   } V (S, t) > n S \\ - \mathcal {L} V \geq 0 \text {   if   } V (S, t) = n S \\ \end{array}
$$

i.e.

$$
\min \left\{- \mathcal {L} V, V - n S \right\} = 0 \tag {1}
$$

in $S > 0 , t \in [ 0 , T )$ .

Scaling the principal to \$1, the final condition is

$$
V (S, T) = \max \{1, n S \}.
$$

Remark: If a coupon K is paid at time $t _ { c } ,$ , then we should add the jump condition across the coupon date

$$
V (S, t _ {c} ^ {-}) = V (S, t _ {c} ^ {+}) + K.
$$

# 1.2 Conversion region and optimal conversion strategy

The solution region $( 0 , + \infty ) \times [ 0 , T )$ is divided into a conversion region (CR) and a holding region (HR):

$$
\mathrm{CR} = \{(S, t) \in (0, + \infty) \times [ 0, T): V (S, t) = n S \}
$$

$$
\mathrm{HR} = \{(S, t) \in (0, + \infty) \times [ 0, T): V (S, t) > n S \}
$$

It turns out that there is a boundary $S ^ { * } ( t )$ , known as the optimal conversion boundary, such that

$$
\mathrm{CR} = \left\{(S, t) \in (0, + \infty) \times [ 0, T): S \geq S ^ {*} (t) \right\}.
$$

This defines an optimal conversion strategy:

(1) The holder should immediately convert the stock to the underlying stock once $S ^ { * } ( t )$ （2 is hit.   
(2) The holder should not do conversion if $S < S ^ { * } ( t )$

# 2 A binomial model and link to the continuous time model

# 2.1 A binomial model

$$
V (S, t - \delta t) = \max \left\{e ^ {- r \Delta t} [ p V (S u, t) + (1 - p) V (S d, t) ], n S \right\}
$$

in $S > 0 , t \leq T$ , with $V ( S , T ) = \operatorname* { m a x } \{ 1 , n S \}$ , where

$$
u = \frac {1}{d} = e ^ {\sigma \sqrt {\delta t}}, p = \frac {e ^ {(r - q) \delta t} - d}{u - d}.
$$

# 2.2 Link to the continuous time mode

The model can be rewritten as

$$
\begin{array}{l} 0 = V (S, t - \delta t) - \max \left\{e ^ {- r \Delta t} (p V (S u, t) + (1 - p) V (S d, t)), n S \right\} \\ = \min \left\{V (S, t - \delta t) - e ^ {- r \Delta t} (p V (S u, t) + (1 - p) V (S d, t)), V (S, t - \delta t) - n S \right\}, \\ \end{array}
$$

which is equivalent to

$$
\min \left\{\frac {1}{\delta t} \left[ V (S, t - \delta t) - e ^ {- r \Delta t} (p V (S u, t) + (1 - p) V (S d, t)) \right], V (S, t - \delta t) - n S \right\} = 0.
$$

Using Taylor expansion, we have

$$
\min \left\{- \mathcal {L} V + O (\delta t), V (S, t) - n S + O (\delta t) \right\} = 0.
$$

Sending $\delta t \to 0$ , we have

$$
\min \left\{- \mathcal {L} V, V (S, t) - n S \right\} = 0.
$$

# 3 Call and put features

The convertible bond permits the holder to exchange the bond for a certain number of underlying asset at any time of their choosing. Convertible bonds often also have a call feature which gives the issuing company the right to purchase back the bond at any time (or during specified periods) for a specified amount $M _ { C }$ . So

$$
V \leq M _ {C}.
$$

Some convertible bonds incorporate a put feature. This right permits the holder of the bond to return it to the issuing company for an amount $M _ { P }$ . Then

$$
V \geq M _ {P}.
$$

Both $M _ { C }$ and $M _ { P }$ can be time dependent. All this constraints can be easily incorporated to the pricing models. For example, if we assume that there is only a call feature with an amount $M _ { C }$ , then

$$
n S \leq V \leq M _ {C}.
$$

(1) is modified as

$$
\max \left\{\min \left\{- \mathcal {L} V, V - n S \right\}, V - M _ {C} \right\} = 0 \tag {2}
$$

in $\textstyle 0 < S < { \frac { M _ { C } } { n } } , t \in [ 0 , T )$ , with the final and boundary conditions

$$
V (S, T) = \min \left\{\max \{1, n S \}, M _ {C} \right\}.
$$

$$
V \left(\frac {M _ {C}}{n}, t\right) = M _ {C}.
$$

# 3.1 Derivation: BTM

It is clear that

$$
M _ {C} \geq V \geq n S,
$$

from which we deduce

$$
S \leq \frac {M _ {C}}{n}
$$

and

$$
V \left(\frac {M _ {C}}{n}, t\right) = M _ {C}.
$$

Then the BTM can be written as

$$
V (S, t - \Delta t) = \min \left\{\max \left(e ^ {- r \Delta t} \left[ p V (S u, t) + (1 - p) V (S d, t) \right], n S\right), M _ {C} \right\}.
$$

It follows

$$
V (S, t - \Delta t) - \min \left\{\max \left(e ^ {- r \Delta t} \left[ p V (S u, t) + (1 - p) V (S d, t) \right], n S\right), M _ {C} \right\} = 0
$$

or

$$
\begin{array}{l} \max \left(\min \left(\frac {V (S , t - \Delta t) - e ^ {- r \Delta t} [ p V (S u , t) (1 - p) V (S d , t) ]}{\Delta t}, \right. \right. \\ + \quad V (S, t - \Delta t) - n S), V (S, t - \Delta t) - M _ {C}) = 0 \\ \end{array}
$$

Noting

$$
\frac {V (S , t - \Delta t) - e ^ {- r \Delta t} [ p V (S u , t) + (1 - p) V (S d , t) ]}{\Delta t} \rightarrow - \mathcal {L} V \mathrm{as} \Delta t \rightarrow 0,
$$

we achieve the desired model.

A remark: the equation can be rewritten as

$$
\begin{array}{l} - \mathcal {L} V = 0 \text {   if   } n S <   V <   M _ {C} \\ - \mathcal {L} V \geq 0 \text {   if   } V = n S \\ - \mathcal {L} V \leq 0 \text {   if   } V = M _ {C}, \\ \end{array}
$$

which can be derived by delta hedging as well, that is

$$
\begin{array}{l} d \Pi = d V - \Delta d S \leq r \Pi d t \text {if} V = n S; \\ d \Pi = d V - \Delta d S \geq r \Pi d t \text {if} V = M _ {C}. \\ \end{array}
$$

For put feature, we have

$$
V \geq \max \left(M _ {P}, n S\right).
$$

# 3.2 Soft call or put

Soft call constraint restricts the issuer to arbitrarily exercise the call. For example, the issuing company may call back the bond at a predetermined price $M _ { C }$ only when the underlying asset stays above a given barrier H more than 10 days during the past 20 days. Usually the holder has the priority to exercise the conversion right upon call and

$$
\frac {1 0 0}{X} H > > M _ {C}.
$$

As a result, a soft call often implies a forcing conversion.

Consider the pricing at (S, t) . To price the soft call feature, the financial industry often introduces an equivalent call boundary $\overline { H }$ :

$$
\begin{array}{l} \mathrm{Prob} \{\overline {{H}} \text {is reached:} S _ {t} = S \} \\ = \operatorname{Prob} \left\{S _ {u} \geq H \text {   satisfying   10   out   of   } 2 0: S _ {t} = S \right\}, \\ \end{array}
$$

Then we impose the following boundary condition at $S = { \overline { { H } } }$ :

$$
V (\overline {{H}}, t) = \frac {1 0 0}{X} \overline {{H}}.
$$

RMI bond team proposes an alternative way to define an equivalent call boundary $\widetilde { H }$ :

$$
\widetilde {H} = \widehat {E} \left[ S _ {u}: u = \inf \left\{\tau : S _ {\tau} \geq H \mathrm{satisfying10outof20,} S _ {t} = S \right\} \right]
$$

Similarly we can consider the soft put feature.

# 4 Dilution

In reality, the conversion of the bond into the underlying stock requires the firm to issue n new shares. This contrasts with the early exercise of an American option which leaves the number of shares unchanged.

Notations:

The firm’s value: S, there are N shares.

Equityholders: E, there are N shares.

Bondholders: V, there are m shares.

After conversion, $E = S .$

Before conversion, $N S = N E + m V ,$ that is,

$$
E = \frac {N S - m V}{N}.
$$

As such, before conversion, the firm’s value is $N S _ { t - }$ ; After conversion, $\left( N + n m \right) S _ { t + }$ . The total worth of the firm remains unchanged upon conversion:

$$
N S _ {t -} = (N + n m) S _ {t +},
$$

that is

$$
S _ {t +} = \frac {N}{N + n m} S _ {t -}.
$$

At time t, the conversion price should be

$$
n S _ {t +} = \frac {N}{N + n m} n S _ {t -}.
$$

We will use the firm’s value as the underlying. Let $V ( S , t )$ be the value of the convertible bond before conversion. Then

$$
V (S, t) \geq \frac {N}{N + n m} n S. \tag {3}
$$

The factor $\frac { N } { N + n m }$ N+nm is known as the dilution factor. In the limit $n m / N  0$ we return to $V \geq n S$ .

On the other hand, we must also have

$$
E := \frac {N S - m V}{N} \geq 0,
$$

that is

$$
V \leq \frac {N}{m} S,
$$

which means that the company is allowed to declare bankruptcy if the bond becomes too valuable. In summary,

$$
\frac {N}{N + n m} n S \leq V \leq \frac {N}{m} S.
$$

Noticing

$$
{\frac {N}{N + n m}} n S = {\frac {N}{{\frac {N}{n}} + m}} S <   {\frac {N}{m}} S,
$$

the pricing model is

$$
\max \left\{\min \left\{- \mathcal {L} V, V - \frac {N}{N + n m} n S \right\}, V - \frac {N}{m} S \right\} = 0
$$

in $S > 0 , t \in [ 0 , T )$ , with

$$
V (S, T) = \min \left(\max \left(1, \frac {N}{N + n m} n S\right), \frac {N}{m} S\right).
$$

# 5 Two-factor modeling: Pricing with stochastic interest rate

The life-span of a typical convertible is much longer than that for a traded option. It is therefore safer to price it using a stochastic interest rate model. When interest rates are stochastic, the convertible bond has a value of the form

$$
V = V (S, r, t).
$$

We continue to assume that the risk neutral price of the underlying asset is governed by

$$
\frac {d S _ {t}}{S _ {t}} = (r - q) d t + \sigma d \widehat {W} _ {1 t}
$$

and the risk-neutral short-term interest rate by

$$
d r = (u - \lambda \omega) d t + \omega d \widehat {W} _ {2 t}
$$

with $E ( d \widehat { W } _ { 1 } d \widehat { W } _ { 2 } ) = \rho d t$ . Then we can derive the pricing equation:

$$
\left\{ \begin{array}{l l} \min \left\{- L V, V - n S \right\} = 0 \\ V (S, r, T) = \max \left(1, n S\right) \end{array} \right.
$$

in $S > 0 , r > 0 , t < T _ { \cdot }$ , where

$$
\begin{array}{l} L V = \frac {\partial V}{\partial t} + \frac {1}{2} \sigma^ {2} S ^ {2} \frac {\partial^ {2} V}{\partial S ^ {2}} + \rho \sigma S \omega \frac {\partial^ {2} V}{\partial S \partial r} + \frac {1}{2} \omega^ {2} \frac {\partial^ {2} V}{\partial r ^ {2}} \\ + (r - q) S \frac {\partial V}{\partial S} + (u - \lambda \omega) \frac {\partial V}{\partial r} - r V. \\ \end{array}
$$

# 6 Convertible bonds with credit risk

Reference: Ayache, Forsyth and Vetzal (2003): The valuation of convertible bonds with credit risk, Journal of Derivatives, 11, 9-29.

Assume default risk is diversifiable. Let the probability of default in the time period t to $t + d t$ , conditional on no-default in [0, t], be ${ \bf \nabla } p _ { t } d t$ , where $p _ { t } = p ( S _ { t } , t )$ is a deterministic hazard rate.

# 6.1 The pricing of a risky bond

Let $B ( S , t )$ denote the price of a risky corporate bond. Construct the standard hedging portfolio

$$
\Pi = B _ {t} - \beta S _ {t}.
$$

In the absence of default, if we choose $\begin{array} { r } { \beta = \frac { \partial B } { \partial S } } \end{array}$ , the usual arguments give

$$
d \Pi_ {t} = \left[ \frac {\partial B}{\partial t} + \frac {\sigma^ {2} S _ {t} ^ {2}}{2} \frac {\partial^ {2} B}{\partial S ^ {2}} \right] d t.
$$

Assume that:

1) The probability of default in $t  t + d t$ is ${ \bf \nabla } p _ { t } d t$

2) The value of the bond immediately after default is RK, where $0 \leq R \leq 1$ is the recovery factor. It is possible to make various assumptions about K. For example, for coupon bearing bonds, it is often assumed that K equals the face value F . For zero coupon bonds, we could assume that $K = B$ , the pre-default value.

3) The stock price $S _ { t }$ is unchanged on default.

Then we have

$$
\begin{array}{l} \widehat {E} \left[ d \Pi_ {t} \right] = (1 - p _ {t} d t) \left[ \frac {\partial B}{\partial t} + \frac {\sigma^ {2} S _ {t} ^ {2}}{2} \frac {\partial^ {2} B}{\partial S ^ {2}} \right] d t + p _ {t} d t (R K - B _ {t}) \\ = \left[ \frac {\partial B}{\partial t} + \frac {\sigma^ {2} S _ {t} ^ {2}}{2} \frac {\partial^ {2} B}{\partial S ^ {2}} \right] d t - p _ {t} (B _ {t} - R K) d t + o (d t). \\ \end{array}
$$

The assumption that default risk is diversifiable implies

$$
\widehat {E} (d \Pi_ {t}) = r (t) \Pi_ {t} d t.
$$

It follows

$$
\frac {\partial B}{\partial t} + \frac {\sigma^ {2} S ^ {2}}{2} \frac {\partial^ {2} B}{\partial S ^ {2}} + r (t) S \frac {\partial B}{\partial S} - (r (t) + p (S, t)) B + p (S, t) R K = 0.
$$

If we assume that $K = B$ and $p = p ( t )$ , then the solution for a zero coupon bond with face value F payable at $t = T$ satisifes

$$
\frac {\partial B}{\partial t} + \frac {\sigma^ {2} S ^ {2}}{2} \frac {\partial^ {2} B}{\partial S ^ {2}} + r (t) S \frac {\partial B}{\partial S} - [ r (t) + p (t) (1 - R) ] B = 0
$$

in $S > 0 , t < T$ with $B \left( S , T \right) = F .$ The solution is

$$
B (t) = F \exp \left[ - \int_ {t} ^ {T} [ r (u) + p (u) (1 - R) ] d u \right],
$$

which corresponds to the intuitive idea of a spread $s = p ( 1 - R )$ .

If we assume that the stock price $S _ { t }$ jumps to zero in the case of default (keeping in mind $\Pi _ { t } = B _ { t } - \beta S _ { t } )$ , then

$$
\begin{array}{l} \widehat {E} (d \Pi_ {t}) = (1 - p _ {t} d t) \left[ \frac {\partial B}{\partial t} + \frac {\sigma^ {2} S _ {t} ^ {2}}{2} \frac {\partial^ {2} B}{\partial S ^ {2}} \right] d t + p _ {t} d t (R K - B _ {t}) - \beta (0 - S _ {t}) p _ {t} d t \\ { = } { \left[ \frac { \partial B } { \partial t } + \frac { \sigma ^ { 2 } S _ { t } ^ { 2 } } { 2 } \frac { \partial ^ { 2 } B } { \partial S ^ { 2 } } \right] d t - p _ { t } d t ( B _ { t } - R K - \beta S _ { t } ) + o ( d t ) . } \\ \end{array}
$$

Following the same steps as above with $\begin{array} { r } { \beta = \frac { \partial B } { \partial S } } \end{array}$ , we obtain

$$
\frac {\partial B}{\partial t} + \frac {\sigma^ {2} S ^ {2}}{2} \frac {\partial^ {2} B}{\partial S ^ {2}} + (r (t) + p) S \frac {\partial B}{\partial S} - (r (t) + p) B + p R K = 0.
$$

Note that in this case p appears in the drift term as well as in the discounting term. Even in this relatively simple case of a risky corporate bond, different assumptions about the behavior of the stock price in the event of default will change our valuation. While this is perhaps an obvious point, it is worth remembering that in some popular existing models for convertible bonds no explicit assumptions are made regarding what happens to the stock price upon default.

# 6.2 The pricing of convertible bonds with credit risk

In the beginning, to avoid complications at this stage, we assume there are no put or call features and that conversion is only allowed at the terminal time or in the event of default. Let $S _ { t + }$ be the stock price immediately after default, and $S _ { t - }$ − be the stock price right before default. We will assume that

$$
S _ {t +} = S _ {t -} (1 - \eta), \tag {4}
$$

where $0 \leq \eta \leq 1$ . We will refer to the case where $\eta = 1$ as the “total default” case (the stock price jumps to zero), and we will call the case where $\eta = 0$ the “partial default” case (the issuing firm defaults but the stock price does not jump anywhere).

As usual, we construct the hedging portfolio

$$
\Pi_ {t} = V _ {t} - \beta S _ {t},
$$

where $V _ { t } = V \left( S _ { t } , t \right)$ . If there was no credit risk, i.e. $p = 0$ , then choosing $\begin{array} { r } { \beta = \frac { \partial V } { \partial S } } \end{array}$ and applying standard arguments gives

$$
d \Pi_ {t} = \left[ \frac {\partial V}{\partial t} + \frac {\sigma^ {2} S _ {t} ^ {2}}{2} \frac {\partial^ {2} V}{\partial S ^ {2}} \right] d t.
$$

Now, consider the case where the hazard rate p is nonzero. We make the following assumptions:

1) Upon default, the stock price jumps according to equation (4).   
2) Upon default, the convertible bond holders have the option of receiving (a) the amount $R K , \operatorname { o r } \left( \mathrm { b } \right)$ shares worth n $S _ { t + } = n S _ { t - } ( 1 { - } \eta )$ . So, they obtain max $( n S _ { t - } ( 1 - \eta ) , R K )$ .

Under these assumptions, the change in value of the hedging portfolio during $\tau  t + d t$ is

$$
\begin{array}{l} \widehat {E} (d \Pi) = (1 - p d t) \left[ \frac {\partial V}{\partial t} + \frac {\sigma^ {2} S _ {t -} ^ {2}}{2} \frac {\partial^ {2} V}{\partial S ^ {2}} \right] d t + p d t [ (\max (n S _ {t -} (1 - \eta), R K) - V _ {t}) - \beta (S _ {t +} - S _ {t -}) ] p d t \\ = \left[ \frac {\partial V}{\partial t} + \frac {\sigma^ {2} S _ {t -} ^ {2}}{2} \frac {\partial^ {2} V}{\partial S ^ {2}} \right] d t + p d t \left(\eta S _ {t -} \frac {\partial V}{\partial S} - V\right) + p d t \max \left(n S _ {t -} (1 - \eta), R K\right) + o (d t). \\ = r \left(V _ {t} - S _ {t -} \frac {\partial V}{\partial S}\right) d t. \\ \end{array}
$$

We then obtain

$$
\frac {\partial V}{\partial t} + \frac {\sigma^ {2} S ^ {2}}{2} \frac {\partial^ {2} V}{\partial S ^ {2}} + (r + p \eta) S \frac {\partial V}{\partial S} - (r + p) V + p \max (n S (1 - \eta), R K) = 0. \tag {5}
$$

Note that $r + p \eta$ appears in the drift term and $r + p$ appears in the discounting term. In the case that $R = 0 , \eta = 1$ , which is the total default model with no recovery, the final result is especially simple.

Define

$$
L V = \frac {\partial V}{\partial t} + \frac {\sigma^ {2} S ^ {2}}{2} \frac {\partial^ {2} V}{\partial S ^ {2}} + (r + p \eta - q) S \frac {\partial V}{\partial S} - (r + p) V
$$

We can write equation (5) for the case where the stock pays a proportional dividend q as

$$
L V + p \max (n S (1 - \eta), R K) = 0.
$$

We are now in a position to consider the complete problem for convertible bonds with risky debt. Let $M _ { c }$ and $M _ { p }$ be the call value and put value, respectively $( M _ { c } > M _ { p } )$ .

If $M _ { c } \le n S$ , then $V = n S$ .

If $M _ { c } > n S$ , then

$$
\begin{array}{l} L V + p \max (n S (1 - \eta), R K) = 0 \text {for} \max (M _ {p}, n S) <   V <   M _ {c}, \\ - L V - p \max (n S (1 - \eta), R K) \geq 0 \text {for} V = \max (M _ {p}, n S), \\ - L V - p \max (n S (1 - \eta), R K) \leq 0 \text {for} V = M _ {c} \\ \end{array}
$$