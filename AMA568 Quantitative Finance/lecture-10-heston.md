# The Heston Stochastic Volatility Model:

# From Dynamics and PDE to the Characteristic Function and COS Pricing

AMA568 / quantitative finance teaching notes

March 24, 2026

# Abstract

These notes introduce the Heston (1993) model for readers who are not assumed to know stochastic volatility pricing already. The storyline is: why constant volatility fails in markets, the risk-neutral SDEs, the associated pricing PDE, the characteristic function and its explicit solution, Fourier inversion and the Fourier–cosine (COS) series for European options, then connection to the volmodel-heston Python code. Optional figures and a Bitcoin implied-volatility calibration illustrate numerics.

# Contents

1 How to read these notes (no prior Heston background) 2   
2 Motivation: why not constant volatility? 2   
3 Risk-neutral dynamics and parameters 2   
4 The Heston pricing PDE 3   
5 Characteristic function: definition and role 3   
6 Explicit solution for the Heston characteristic function 3   
7 From the characteristic function to European option prices 4   
8 The Fourier–cosine (COS) series for option pricing 4   
9 Summary: mapping theory to volmodel-heston 5   
10 Illustrations from the code 5   
10.1 Simulated spot and volatility paths 5   
10.2 Flat Black–Scholes vs. Heston smile 5   
10.3 European prices and implied vol (integration pricer) 5   
10.4 COS vs. numerical integration . 7   
11 Market example: Bitcoin options and calibration (optional) 7   
11.1 Data 7   
11.2 Step 1 T , r, F 7   
11.3 Step 2 — Market σmkt(K) 7   
11.4 Step 3 — Parameters . 7   
11.5 Step 4 — Objective . 7

11.6 Step 5 — Optimiser 7   
11.7 Step 6 — Fitted values (last generator run) 8

12 Quick reference: example numbers and Black–Scholes comparison 8   
13 Assumptions, strengths, and limitations 9   
14 Repository scripts 9

# 1 How to read these notes (no prior Heston background)

You need: basic calculus, random variables, and the idea that a European option value solves a PDE in Black–Scholes (or at least that option prices come from an expectation under a risk-neutral measure). The path through this document is intentionally linear:

1. Motivation — flat Black–Scholes vs. smiles in data.   
2. Model — two coupled SDEs for spot and variance; parameter meanings.   
3. PDE — the partial differential equation that a smooth option value must satisfy inside the Heston world.   
4. Characteristic function — what it is and why it replaces knowing the whole density of ln $S _ { T }$ .   
5. Explicit $\varphi -$ Heston’s closed form (up to complex arithmetic).   
6. Pricing — brief Fourier inversion; then the COS cosine series.   
7. Code and pictures — mapping to heston.py / heston cos.py; figures and optional BTC calibration.

# 2 Motivation: why not constant volatility?

The Black–Scholes model assumes the underlying follows geometric Brownian motion with constant volatility σ. Then, for a fixed maturity, implied volatility (Backing out a σ from market option prices) would be the same for every strike—a flat smile. In practice one often sees a volatility smile or skew: implied vol varies with strike.

Takeaway. To respect the smile with a single model, one must relax constant volatility. The Heston model lets variance follow its own random process (mean-reverting, nonnegative), coupled to the stock. That extra structure is enough to produce realistic skews and to support industry-standard Fourier-based pricing of European options.

# 3 Risk-neutral dynamics and parameters

Let $S _ { t }$ be the spot price and $v _ { t }$ the instantaneous variance (so $\sqrt { v _ { t } }$ is volatility). Under an equivalent martingale measure $\mathbb { Q }$ , with constant short rate r and no dividends (for simplicity), the Heston model is

$$
\mathrm{d} S _ {t} = r S _ {t} \mathrm{d} t + \sqrt {v _ {t}} S _ {t} \mathrm{d} W _ {t} ^ {S}, \tag {1}
$$

$$
\mathrm{d} v _ {t} = \kappa (\theta - v _ {t}) \mathrm{d} t + \eta \sqrt {v _ {t}} \mathrm{d} W _ {t} ^ {v}, \tag {2}
$$

with instantaneous correlation $\langle \mathrm { d } W ^ { S } , \mathrm { d } W ^ { v } \rangle _ { t } = \rho \mathrm { d } t$ . Parameters (all assumed constant in the basic model):

• $\kappa > 0 \mathrm { : }$ : speed of mean reversion of variance toward its long-run level;   
• $\theta > 0$ : long-run variance (not volatility);   
• $\eta > 0 \colon$ : volatility of volatility (“vol-of-vol”);   
• $\rho \in [ - 1$ , 1]: correlation of stock and variance shocks (often $\rho < 0$ for equity skew);   
• $v _ { 0 } > 0 ;$ variance today.

Intuition. Equation (2) is a square-root (Cox–Ingersoll–Ross type) process: variance stays positive, fluctuates, but is pulled toward θ at rate κ. Equation (1) is like Black–Scholes except $\sqrt { v _ { t } }$ replaces constant $\sigma$ .

Pedagogical simulation. Simple path simulation must use correlated Brownian increments when $\rho \neq 0$ . Figure 1 (later) shows sample paths.

# 4 The Heston pricing PDE

Let ${ \cal U } ( S , v , t )$ be the time-t value of a European-style claim with maturity T , when the spot is S and variance is v. Under the same risk-neutral dynamics (no dividends), U satisfies a second-order parabolic PDE for $S > 0 , v > 0 , t < T$ :

$$
\frac {\partial U}{\partial t} + \frac {1}{2} v S ^ {2} \frac {\partial^ {2} U}{\partial S ^ {2}} + \rho \eta v S \frac {\partial^ {2} U}{\partial S \partial v} + \frac {1}{2} \eta^ {2} v \frac {\partial^ {2} U}{\partial v ^ {2}} + r S \frac {\partial U}{\partial S} + \kappa (\theta - v) \frac {\partial U}{\partial v} - r U = 0. (3)
$$

At expiry t = T , U equals the payoff $( \mathrm { e . g . ~ } ( S - K ) ^ { + }$ for a call).

Log-price form. With $x = \ln S$ and $V ( x , v , t ) = U ( e ^ { x } , v , t )$ , the equation becomes

$$
\frac {\partial V}{\partial t} + \frac {1}{2} v \frac {\partial^ {2} V}{\partial x ^ {2}} + \rho \eta v \frac {\partial^ {2} V}{\partial x \partial v} + \frac {1}{2} \eta^ {2} v \frac {\partial^ {2} V}{\partial v ^ {2}} + \left(r - \frac {1}{2} v\right) \frac {\partial V}{\partial x} + \kappa (\theta - v) \frac {\partial V}{\partial v} - r V = 0. (4)
$$

Why this matters for teaching. The SDE tells you how $( S _ { t } , v _ { t } )$ evolves; the PDE is the “infinitesimal pricing consistency” condition for any smooth claim value. In practice, European options under Heston are rarely priced by solving this PDE on a grid in $( S , v )$ for production (though PDE/finite-difference methods are used). Instead, one exploits the fact that the model is affine: the PDE leads to an explicitly known characteristic function, and prices follow by Fourier methods (next sections).

# 5 Characteristic function: definition and role

Define the log-moneyness at maturity relative to today’s spot S0:

$$
X _ {T} := \ln \frac {S _ {T}}{S _ {0}}.
$$

The (risk-neutral) characteristic function of $X _ { T }$ is the complex-valued function

$$
\varphi (u) := \mathbb {E} ^ {\mathbb {Q}} \left[ e ^ {i u X _ {T}} \right], \quad u \in \mathbb {R}, \tag {5}
$$

and more generally for u in a strip in the complex plane where the expectation exists. For each real $u , \varphi ( u )$ is the Fourier transform of the density of $X _ { T }$ (up to conventions).

Why traders and quants care. If you know $\varphi$ on a grid in u, you can recover option prices by inverse Fourier transforms (integrate $\varphi$ against a known weight). You do not need a closed formula for the density of $S _ { T }$ itself. For Heston, $\varphi$ is available in closed form (Section 6).

Convention. Different papers move $e ^ { i u \ln S _ { 0 } }$ , use $e ^ { i u \ln S _ { T } }$ , or shift to $Y = \ln S _ { T }$ ; always check the definition when comparing formulas. Our code heston.py implements $\varphi$ exactly as in (5) for $X _ { T } = \ln ( S _ { T } / S _ { 0 } )$ .

# 6 Explicit solution for the Heston characteristic function

The Heston model is affine in $( x , v )$ with x = ln S. Seeking a solution of the form $\mathbb { E } [ e ^ { i u X _ { T } } \mid x _ { t } =$ $x , v _ { t } = v ]$ leads to exponentials linear in v and x. For maturity $\tau : = T - t$ and $x _ { t } = \ln ( S _ { t } / S _ { 0 } )$ at time t, one obtains the affine representation

$$
\mathbb {E} \big [ e ^ {i u X _ {T}} \mid x _ {t} = x, v _ {t} = v \big ] = \exp \big (C (u, \tau) + D (u, \tau) v + i u x \big).
$$

${ \mathrm { A t ~ } } t = 0 { \mathrm { ~ w e ~ h a v e ~ } } x = 0 { \mathrm { ~ a n d ~ } } v = v _ { 0 } , { \mathrm { ~ s o ~ } } \varphi ( u ) = \exp ( C ( u , T ) + D ( u , T ) v _ { 0 } ) .$

Formulas (same structure as Heston.charfun). Fix $u \in \mathbb { C }$ in the domain where the square root and logarithm below use their standard analytic branches (numerical codes must handle this carefully; see Albrecher et al. for “little Heston trap” variants). Write $\tau = T$ for time to maturity from $t = 0$ . Define

$$
d (u) = \sqrt {\left(\kappa - i \rho \eta u\right) ^ {2} + \eta^ {2} \left(u ^ {2} + i u\right)}, \tag {6}
$$

$$
g (u) = \frac {\kappa - i \rho \eta u - d (u)}{\kappa - i \rho \eta u + d (u)}. \tag {7}
$$

Then the characteristic function implemented in heston.py can be written as

$$
\varphi (u) = \exp \left(i u r \tau + \frac {v _ {0}}{\eta^ {2}} \frac {(1 - e ^ {- d (u) \tau}) (\kappa - i \rho \eta u - d (u))}{1 - g (u) e ^ {- d (u) \tau}} + \frac {\kappa \theta}{\eta^ {2}} \Big (\tau (\kappa - i \rho \eta u - d (u)) - 2 \ln \frac {1 - g (u) e ^ {- d (u) \tau}}{1 - g (u)} \Big)\right). \tag {8}
$$

Mapping to the code. In HestonParam, ${ \mathrm { 1 m } } = \kappa , { \mathrm { m u } } = \theta , { \mathrm { e t a } } = \eta , { \mathrm { r h } } { \mathrm { 0 } } = \rho ,$ , and sigma = v0. The method charfun(u) evaluates (8) with τ = maturity and $r = { \tt r i s k f r e e }$ .

# 7 From the characteristic function to European option prices

There is no elementary formula like Black–Scholes $N ( d _ { 1 } ) , N ( d _ { 2 } )$ for the Heston call. Instead, one uses $\varphi$ in one of two broad ways:

(A) One-dimensional integration (Fourier inversion). Heston (1993) expresses the call as combinations of probabilities $P _ { 1 } , P _ { 2 }$ that are recovered from integrals of $\varphi$ against oscillatory weights. Our module heston integration price.py prices the call as

$$
C = S _ {0} P _ {1} - K e ^ {- r T} P _ {2},
$$

with $P _ { 1 } , P _ { 2 }$ computed by scipy.integrate.quad using a stable two-component characteristic function (Albrecher et al.). Puts follow from put–call parity: $P = C - S _ { 0 } + K e ^ { - r T }$ .

(B) Fourier–cosine (COS) series. Expand the density of $X _ { T }$ on a truncated interval $[ a , b ]$ in cosines; coefficients are obtained from $\varphi .$ . The next section gives the series used in heston cos.py.

# 8 The Fourier–cosine (COS) series for option pricing

Fang and Oosterlee (2008–2009) approximate the density $f _ { X } ( x )$ of $X _ { T } = \ln ( S _ { T } / S _ { 0 } )$ on a finite interval $[ a , b ]$ by a cosine expansion:

$$
f _ {X} (x) \approx \sum_ {k = 0} ^ {N - 1} A _ {k} \cos \left(\omega_ {k} (x - a)\right), \quad x \in [ a, b ], \tag {9}
$$

where $\omega _ { k } = k \pi / ( b - a )$ and the prime on sums below means the $k = 0$ term is halved.

Coefficients from $\varphi .$ For many models (including Heston), the $A _ { k }$ follow from the characteristic function: schematically, $A _ { k }$ is proportional to $\operatorname { R e } \{ \varphi ( \omega _ { k } ) e ^ { - i \omega _ { k } a } \}$ (see Fang–Oosterlee for the exact discrete-cosine connection). In code, only combinations $\varphi ( \omega _ { k } ) e ^ { - i \omega _ { k } a }$ enter the price directly.

Truncation $[ a , b ]$ . The interval must contain most of the probability mass of $X _ { T }$ . Our Heston.cos restriction() returns $( a , b )$ using the first two cumulants of $\ln ( S _ { T } )$ under the model and a fixed multiple L of the standard deviation (see heston.py).

Payoff cosine coefficients $V _ { k }$ . For a European call with strike K, write payoff in x = ln $( S _ { T } / S _ { 0 } )$ as $( S _ { 0 } e ^ { x } - K ) ^ { + }$ . The COS method uses closed-form integrals of this payoff against $\cos ( \omega _ { k } ( x - a ) ) { \mathrm { ~ o n ~ } } [ a , b ] ;$ ; denote these by $V _ { k }$ (in code, chi call). Similarly for puts (chi put).

Call price as a cosine series. Let $\omega _ { k } = k \pi / ( b - a ) , \tau = T$ , and $\sum ^ { \prime }$ halve the k = 0 term. The implementation in heston cos. cos price matches

$$
C \approx e ^ {- r \tau} \frac {b - a}{2} \sum_ {k = 0} ^ {\prime} \mathrm{Re} \bigl \{\varphi (\omega_ {k}) e ^ {- i \omega_ {k} a} V _ {k} \bigr \}. \tag {10}
$$

The put can be priced by the same formula with put coefficients, or (as in our code by default) by put–call parity with the COS call so call and put stay consistent for the same $[ a , b ]$ and N .

Accuracy and cost. Error decays typically very fast in N if $[ a , b ]$ is wide enough. COS is often much faster than repeated numerical integration in u for many strikes (e.g. calibration loops).

# 9 Summary: mapping theory to volmodel-heston

<table><tr><td>Concept</td><td>Location in code</td></tr><tr><td>Parameters (κ,θ,η,ρ,ν0)</td><td>HestonParam: lm, mu, eta, rho, sigma</td></tr><tr><td>PDE / SDE</td><td>Not discretised; informs CF theory</td></tr><tr><td>φ(u) for XT = ln(ST/S0)</td><td>Heston.charfun</td></tr><tr><td>COS interval [a,b]</td><td>Heston.cos_restriction</td></tr><tr><td>COS call (10)</td><td>heston_cos.cos_call_price</td></tr><tr><td>Integration pricer C = S0P1 - Ke-rTP2</td><td>heston_integration_price</td></tr><tr><td>Black-76 implied vol</td><td>black76.py</td></tr></table>

# 10 Illustrations from the code

Regenerate figures and calibration macros with:

```batch
cd volmodel-heston
python generate_heston_lecture_figures.py 
```

# 10.1 Simulated spot and volatility paths

Figure 1: sample paths under (1)–(2) (log-Euler, correlated Brownian increments).

# 10.2 Flat Black–Scholes vs. Heston smile

Figure 2: constant Black–76 vol (ATM) vs. Heston smile from COS prices inverted with Black– 76.

# 10.3 European prices and implied vol (integration pricer)

Figure 3: plot heston options.py using heston integration price.py.

![](images/8f2bbd0cb0ad575c4721487735f481e680b2e48565877d54eda9136977c8fa5f.jpg)

Figure 1: Four simulated paths: spot $S _ { t }$ (top) and volatility $\sqrt { v _ { t } }$ (bottom).   
![](images/1e08116bf9e9ac77a2e8d3d651b7516a876294149c9b471dab7133adb7e71742.jpg)

Figure 2: Constant Black–76 vol vs. Heston implied vol (COS pricer).   
![](images/ae5cb0a19a83cfd2f291c71704068d79c853d2d862bb28c5beb71702e580b1c8.jpg)  
Figure 3: Heston calls, puts, and Black–76 implied vol vs. strike.

# 10.4 COS vs. numerical integration

Figure 4: error relative to high-N COS and timings. The integration pricer uses a different CF convention (Albrecher); see report heston validation.tex.

S=100,T=0.5,r=0.03|strikes 65.0,35.0]|Integrationuses Albrecher CF;reference uses heston.py CF(COs N=2048).

![](images/6e501809920ba6cd368d3f979caa9b9aa660b57faf1d8408ebf9711665a581a4.jpg)

<details>
<summary>line</summary>

| Strike K | Cost (COS) | RMSE (COS) | RMSE (int) |
| -------- | ---------- | ---------- | ---------- |
| 70       | 0.5        | 0.932e-07  | 2.91e-01   |
| 80       | 0.4        | 0.932e-07  | 2.91e-01   |
| 90       | 0.2        | 0.932e-07  | 2.91e-01   |
| 100      | 0.1        | 0.932e-07  | 2.91e-01   |
| 110      | 0.0        | 0.932e-07  | 2.91e-01   |
| 120      | 0.0        | 0.932e-07  | 2.91e-01   |
| 130      | 0.0        | 0.932e-07  | 2.91e-01   |
</details>

![](images/b5d9c8bdda1c18989b2c316c16308c4c07191654bb38ee3d4ce1dc75f4561d73.jpg)

<details>
<summary>bar</summary>

| Method | Seconds (total for all strikes) |
| --- | --- |
| COS N=2048 (reference) | 0.015 |
| Integration (quad × 2) | 0.08 |
| COS N=128 | 0.005 |
</details>

Figure 4: COS vs. integration: price error and wall time.

# 11 Market example: Bitcoin options and calibration (optional)

Single-maturity calibration of Heston to mid implied volatilities from data/BTC\_20260327\_ 20260310.csv; code in fit heston market data.py.

# 11.1 Data

Each row: strike with call/put bid/ask implied vols. One chooses T , F , r; the loader builds mid IVs on a moneyness window (see that file for details).

# 11.2 Step 1 — T , r, F

Defaults: $T = 1 7 / 3 6 5 , F = 6 9 0 2 8 . 0 0 ~ { \mathrm { U S D } } , r = 0 , S _ { 0 } \approx 6 9 0 2 8 . 0 0 .$

# 11.3 Step 2 — Market $\sigma ^ { \mathrm { m k t } } ( K )$

OTM-style bid/ask handling; 32 strikes after filters.

# 11.4 Step 3 — Parameters

$\pmb { \xi } = ( \kappa , \theta , \eta , \rho , v _ { 0 } ) ^ { \top }$ with box constraints in code.

# 11.5 Step 4 — Objective

For each trial ξ: COS call price → Black–76 IV; minimise $\begin{array} { r } { \sum _ { i } ( \sigma _ { i } ^ { \mathrm { m d l } } - \sigma _ { i } ^ { \mathrm { m k t } } ) ^ { 2 } } \end{array}$ .

# 11.6 Step 5 — Optimiser

L-BFGS-B, multiple starts.

# 11.7 Step 6 — Fitted values (last generator run)

$$
\kappa = 8. 6 4 1 5 3 3, \theta = 0. 3 0 4 3 0 3, \eta = 1. 5 8 3 4 9 8, \rho = - 0. 5 4 9 7 4 2, v _ {0} = 0. 1 6 2 2 0 0.
$$

SSR = 7.791228e + 00, RMSE ≈ 0.493433, max |residual| ≈ 0.909900, COS terms 96, optimiser OK = no, iterations = 13.

BTC options - BTC\_20260327\_20260310.csv (T≈ 17.0 days,F=69,028)   
![](images/49bbbaae1eeb3cd5ffe43edb742b3eac128cf1e8ef69955d1f8e4b9a9e2a598a.jpg)

(a) Mid market IV vs. fitted Heston smile.   
![](images/1af58fcc17fe38f063d4771ef8f88d077d66d9d06425419cabb6b333b3491fa7.jpg)

<details>
<summary>scatter</summary>

| Strike (USD) | Model IV - market mid |
| ------------ | --------------------- |
| 40000        | 0.0                   |
| 45000        | -0.8                  |
| 47000        | -0.9                  |
| 50000        | -0.8                  |
| 52000        | -0.7                  |
| 55000        | -0.7                  |
| 57000        | -0.6                  |
| 60000        | -0.6                  |
| 62000        | 0.1                   |
| 64000        | 0.0                   |
| 65000        | -0.1                  |
| 66000        | -0.1                  |
| 68000        | -0.1                  |
| 70000        | -0.1                  |
| 72000        | -0.1                  |
| 74000        | -0.1                  |
| 76000        | -0.1                  |
| 78000        | -0.1                  |
| 80000        | -0.1                  |
| 82000        | -0.5                  |
| 85000        | -0.5                  |
| 88000        | -0.5                  |
| 90000        | -0.6                  |
| 92000        | -0.6                  |
| 95000        | -0.6                  |
| 98000        | -0.6                  |
| 102000       | -0.6                  |
</details>

(b) IV residuals.   
Figure 5: Bitcoin slice (BTC 20260327 20260310.csv).

# 12 Quick reference: example numbers and Black–Scholes comparison

<table><tr><td>Symbol</td><td>Example (classroom / integration tests)</td></tr><tr><td> $S_0, K, r, T$ </td><td>100, 100, 0.05, 1</td></tr><tr><td> $\kappa, \theta, \eta, \rho, v_0$ </td><td>2, 0.05, 0.3, -0.5, 0.05</td></tr></table>

<table><tr><td>Aspect</td><td>Black-Scholes</td><td>Heston</td></tr><tr><td>Volatility</td><td>Constant</td><td>Stochastic CIR-type variance</td></tr><tr><td>Smile</td><td>Flat σimpl</td><td>Skew/smile possible</td></tr><tr><td>European call</td><td>Closed form</td><td>Semi-analytic: φ + integral or COS</td></tr><tr><td>Parameters</td><td>Few</td><td>(κ,θ,η,ρ,v0)</td></tr></table>

# 13 Assumptions, strengths, and limitations

Assumptions. Frictionless markets, no arbitrage, constant r, often zero dividends in the basic presentation; parameters constant over time.

Strengths. Captures stochastic volatility and mean reversion; fast COS pricing; standard building block for extensions (jumps, time-dependent parameters).

Limitations. Calibration can be ill-posed; short maturities may be hard; model risk; Fellertype conditions on parameters for strictly positive variance in continuous time.

# 14 Repository scripts

```shell
python generate_heston_lecture_figures.py # figures +
calibration_macros.tex
python test_heston.py
python plot_heston_options.py
python plot_cos_vs_integration.py
python fit_heston_market_data.py --data-dir ../data \
--csv BTC_20260327_20260310.csv --plot figures_lecture/btc_fit_only .png 
```

Technical validation: report\_heston\_validation.tex.

# References

• Heston, S. L. (1993). A closed-form solution for options with stochastic volatility.   
• Albrecher, H., Mayer, P., Schoutens, W., Tistaert, J. (2006). The little Heston trap.   
• Fang, F., Oosterlee, C. W. (2008, 2009). COS method for option pricing.