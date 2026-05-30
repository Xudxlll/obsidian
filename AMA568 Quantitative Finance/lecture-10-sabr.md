# Lecture Notes

SABR implied volatility (Hagan et al. 2002 lognormal expansion)

Implementation: pysabr in volmodel-sabr

Companion to volmodels.SABRModel

# Abstract

We summarise the SABR (“Stochastic Alpha Beta Rho”) model as used in this repository: parameters $( \alpha , \beta , \rho , \nu )$ , Hagan’s lognormal implied-volatility expansion, the calibration objective in SABRModel, optional shifted SABR, and a BTC slice example matching test all models.py.

# Contents

# 1 Model overview

SABR models the forward $F _ { t }$ and instantaneous volatility $\sigma _ { t }$ under a single factor:

$$
F _ {t} = \sigma_ {t} F _ {t} ^ {\beta} W _ {t}, \tag {1}
$$

$$
\sigma_ {t} = \nu   \sigma_ {t}   Z _ {t}, \qquad W _ {t}   Z _ {t} = \rho   t, \tag {2}
$$

with parameters: initial level $\alpha = \sigma _ { 0 }$ , CEV exponent $\beta \in [ 0 , 1 ]$ (often $0 , 1 / 2 , \mathrm { o r } 1 )$ ), correlation $\rho \in ( - 1 , 1 )$ , and vol-of-vol $\nu > 0$ .

European options are priced by inserting an effective Black (lognormal) implied volatility $\sigma _ { \mathrm { S L N } } ( K , F , T )$ into Black’s formula. Hagan et al. (2002) give closed-form asymptotic expansions; this codebase uses the lognormal (shifted lognormal) expansion from pysabr.

# 2 Hagan 2002 lognormal vol (as implemented)

Let k denote strike, f forward, T maturity, and assume β fixed. Write

$$
\zeta = \frac {\nu}{\alpha} (f k) ^ {\frac {1 - \beta}{2}} \ln \frac {f}{k}, \qquad x (\rho , \zeta) = \ln \left(\frac {\sqrt {1 - 2 \rho \zeta + \zeta^ {2}} + \zeta - \rho}{1 - \rho}\right).
$$

Define auxiliary terms (matching hagan 2002 lognormal sabr.py):

$$
d = (f k) ^ {\frac {1 - \beta}{2}},
$$

$$
a = \frac {(1 - \beta) ^ {2} \alpha^ {2}}{2 4 f k ^ {1 - \beta}}, \quad b = \frac {\rho \beta \nu \alpha}{4 d}, \quad c = \frac {(2 - 3 \rho^ {2}) \nu^ {2}}{2 4},
$$

$$
v = \frac {(1 - \beta) ^ {2}}{2 4} \Bigl (\ln \frac {f}{k} \Bigr) ^ {2}, w = \frac {(1 - \beta) ^ {4}}{1 9 2 0} \Bigl (\ln \frac {f}{k} \Bigr) ^ {4}.
$$

For |ζ| > ε (with small ε in code), the lognormal implied vol is

$$
\boxed {\sigma_ {\mathrm{SLN}} (k, f, T) = \frac {\alpha \zeta (1 + (a + b + c) T)}{d (1 + v + w) x (\rho , \zeta)}} \tag {3}
$$

For $| \zeta | \le \varepsilon$ , the code uses the limiting form $\sigma _ { \mathrm { S L N } } = \alpha \big ( 1 + ( a + b + c ) T \big ) / \big ( d ( 1 + v + w ) \big )$ .

ATM root for $\alpha .$ Given observed ATM lognormal vol, pysabr can solve a cubic for α $\left( \mathsf { a l p h a } \mathsf { c . } \ldots \right)$ in the same module). SABRModel instead jointly optimises $( \alpha , \rho , \nu )$ against the whole smile (see below).

Shifted SABR. If $\mathtt { s h i f t } = \ s > 0$ , strikes and forward are evaluated as $k + s$ and $f + s$ (positive underlying), stabilising low/negative-rate environments.

# 3 Parameters in SABRModel

Single expiry. SABRModel.fit uses only the first MarketSlice in the list.

# 4 Calibration objective

For strikes $K _ { i }$ and mids $\sigma _ { i } ^ { \mathrm { m i d } }$ , the code minimises (L-BFGS-B)

$$
\min _ {\alpha , \rho , \nu} \sum_ {i} \left(1 0 0 \sigma_ {\mathrm{model}} (K _ {i}) - 1 0 0 \sigma_ {i} ^ {\mathrm{mid}}\right) ^ {2}, \tag {4}
$$

Table 1: SABR parameters (wrapper volmodels/sabr.py). 

<table><tr><td>Symbol</td><td>Code name</td><td>Role</td></tr><tr><td> $\beta$ </td><td>beta</td><td>Fixed before fit (default 1 = lognormal backbone).</td></tr><tr><td> $\alpha$ </td><td>alpha</td><td>Fitted level (scales overall vol).</td></tr><tr><td> $\rho$ </td><td>rho</td><td>Fitted spot–vol correlation (skew).</td></tr><tr><td> $\nu$ </td><td>volvol</td><td>Fitted vol-of-vol (smile curvature).</td></tr><tr><td> $s$ </td><td>shift</td><td>Optional displacement (default 0).</td></tr></table>

i.e. sum of squared errors in vol expressed in percentage points (the factor 100 matches the pysabr convention in Hagan2002LognormalSABR.fit). Initial guess:

$$
\alpha^ {(0)} = \sigma_ {\mathrm{ATM}} ^ {\mathrm{mid}}, \qquad \rho^ {(0)} = - 0. 3, \qquad \nu^ {(0)} = 0. 3.
$$

Bounds: $\alpha , \nu \geq 1 0 ^ { - 4 } , | \rho | \leq 0 . 9 9 9 9$ . Failed vol evaluations add a large penalty $( 1 0 ^ { 6 } )$ to the objective.

# 5 Worked example: BTC slice

```python
from test_all_models import load_btc_market
from volmodels import SABRModel

market = load_btc_market()
model = SABRModel(beta=1.0, shift=0.0)
model.fit([market])
print(model.fitted_params()) 
```

Representative output (β = 1):

<table><tr><td>Parameter</td><td>Value</td></tr><tr><td> $\alpha$ </td><td> $\approx 0.513$ </td></tr><tr><td> $\rho$ </td><td> $\approx -0.411$ </td></tr><tr><td> $\nu$ </td><td> $\approx 3.163$ </td></tr><tr><td>RMSE (IV vs. mid)</td><td> $\approx 0.0065$ </td></tr></table>

Note. ν can be numerically large when the smile is steep in Hagan’s units; always check fit quality and stability.

# 6 Code map

<table><tr><td>Path</td><td>Content</td></tr><tr><td>volmodel-sabr/pysabr/models/hagan_2002_lognormal_sabr.py</td><td>(??), lognormal_vol, alpha root</td></tr><tr><td>volmodels/sabr.py</td><td>SABRModel: L-BFGS-B fit, vol()</td></tr></table>

Limitations. Hagan’s expansion can mis-price deep wings or long maturities; alternatives (normal SABR, Hagan 2013, Monte Carlo) exist elsewhere in pysabr but are not wired into SABRModel.

![](images/be054ca05119a901d2dea301e91b741a7a9fd8b60b330b5592f64efaa877641e.jpg)

<details>
<summary>line</summary>

| k = ln(K/F) | Implied vol σ |
| ----------- | ------------- |
| -0.6        | 1.0           |
| -0.5        | 0.95          |
| -0.4        | 0.9           |
| -0.3        | 0.8           |
| -0.2        | 0.7           |
| -0.1        | 0.6           |
| 0.0         | 0.5           |
| 0.1         | 0.45          |
| 0.2         | 0.5           |
| 0.3         | 0.6           |
| 0.4         | 0.65          |
</details>

Figure 1: BTC test slice: mids vs. SABR Hagan lognormal expansion.