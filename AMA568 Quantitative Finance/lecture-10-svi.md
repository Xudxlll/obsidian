# Lecture Notes

SVI and SSVI implied volatility surfaces

Stochastic Volatility Inspired (codebase: volmodel-svi)

Companion to volmodels.SVIModel / Gatheral & Jacquier (2014)

# Abstract

These notes describe the SVI/SSVI pipeline used in this repository: the raw SVI formula for total variance w(k), the Jump-Wings (JW) parameterisation stored after calibration, a two-stage fit (global SSVI surface + per-slice refinement with calendar penalties), and a worked example on the BTC test slice from test all models.py.

# Contents

# 1 References and role

• Gatheral, J., The Volatility Surface — SVI parameterisations and no-butterfly conditions.   
• Gatheral, J. & Jacquier, A. (2014), Arbitrage-Free SVI Volatility Surfaces, Quantitative Finance.

SVI gives a flexible, low-dimensional smile in log-moneyness with explicit links to arbitragefree “SSVI” surfaces. This implementation targets multi-expiry data but works for a single maturity as well.

# 2 Notation (this codebase)

Table 1: Symbols aligned with svi raw $/$ SVIModel.vol. 

<table><tr><td>Symbol</td><td>Name</td><td>Meaning</td></tr><tr><td>F</td><td>Forward</td><td>Forward for the expiry.</td></tr><tr><td>T</td><td>Time to expiry</td><td>Years.</td></tr><tr><td>K</td><td>Strike</td><td>Option strike.</td></tr><tr><td>k</td><td>Log-moneyness</td><td> $k = \ln(K/F)$  (not divided by  $\sqrt{T}$ ).</td></tr><tr><td>w(k)</td><td>Total implied variance</td><td> $w = \sigma_{\text{impl}}^{2} T$ .</td></tr><tr><td>σ</td><td>Implied vol</td><td> $\sigma(k) = \sqrt{w(k)/T}$ .</td></tr></table>

Contrast. GEDI uses $k = \ln ( K / F ) / \sqrt { T } ;$ ; SVI here uses plain $\ln ( K / F )$ .

# 3 Raw SVI formula

Five parameters $( a , b , m , \rho , \sigma _ { \mathrm { S V I } } )$ satisfy standard box constraints $( b \ge 0 , | \rho | \le 1 , \sigma _ { \mathrm { S V I } } \ge 0$ , and $a + b \sigma _ { \mathrm { S V I } } \sqrt { 1 - \rho ^ { 2 } } \geq 0 )$ . Total variance is

$$
\boxed {w (k) = a + b \left(\rho (k - m) + \sqrt {(k - m) ^ {2} + \sigma_ {\mathrm{SVI}} ^ {2}}\right)} \tag {1}
$$

and implied volatility is $\sigma ( k ) = \sqrt { w ( k ) / T } ~ ( \mathrm { s v i \_ r a w } )$ .

Geometry (intuition). m shifts the smile along k; b scales wing steepness; $\rho$ rotates/skews; σSVI controls curvature near the minimum; a sets the level.

# 4 Jump-Wings (JW) parameterisation

SVIModel stores five numbers per expiry in JW form:

$$
\pmb {\theta} _ {\mathrm{JW}} = (v, \psi , p, c, v _ {t}) ^ {\mathsf {T}}.
$$

Code comments map them to: ATM variance $v ,$ ATM skew $\psi ,$ , put-wing slope $p ,$ call-wing slope $^ { c , }$ and minimum variance $v _ { t }$ . Evaluation uses svi jumpwing: parameters are converted to raw $( a , b , m , \rho , \sigma _ { \mathrm { S V I } } )$ via svi convertparameters, then (??) is applied (svi parameters.py).

# 5 Calibration pipeline (fit svi surface)

# 5.1 Step 1 — Targets

From market mids, build $w _ { i } ^ { \mathrm { m k t } } = ( \sigma _ { i } ^ { \mathrm { m i d } } ) ^ { 2 } T$ on a grid of $( k _ { i } , T _ { i } )$ .

# 5.2 Step 2 — ATM backbone

For each distinct maturity, interpolate $w ^ { \mathrm { m k t } }$ to k = 0 to obtain θ(T ) (ATM total variance term structure).

# 5.3 Step 3 — Global SSVI (fit ssvi)

Fit surface-level parameters controlling a SSVI representation (choice phifun = ’power law’ or ’heston like’ on SVIModel). This yields a global shape (e.g. correlation ρ and auxiliary λ-style parameters) consistent with the no-arbitrage recipes in the cited papers.

# 5.4 Step 4 — JW initial guess

SSVI parameters are mapped to JW scalars per maturity using Lemma 4.1-style formulas in fit svi surface.py (relations among v, ψ, p, c, vt and θ).

# 5.5 Step 5 — Per-slice refinement (fit svi)

For each maturity (processed from long to short in the loop), fit svi minimises the Euclidean norm of errors in total variance (same structure as GEDI slice fit):

$$
\min \left\| \boldsymbol {w} ^ {\mathrm{mkt}} - \boldsymbol {w} ^ {\mathrm{model}} \right\| _ {2}
$$

subject to bounds on $( v , \psi , p )$ and the linear inequality

$$
p + 2 \psi \geq 0 \quad (\text { encoded   as } - p \leq 2 \psi \text { in   code }). \tag {2}
$$

The last two JW entries are reconstructed as c = p + 2ψ and a closed-form $v _ { t }$ from $( v , p , c )$ (see fit svi.py / fit svi surface.py). Neighbouring slices enter via a large penalty (106) if the fitted total variance crosses the previous/next maturity slice (calendar no-arbitrage heuristic).

# 5.6 Optimiser

Per-slice refinement uses scipy.optimize.minimize(..., method=’SLSQP’, ...) (fit svi.py).

# 6 Using SVIModel

```python
from test_all_models import load_btc_market
from volmodels import SVIModel

market = load_btc_market()
model = SVIModel(phifun="power_law")  # or "heston_like"
model.fit([market])
iv = model.vol(market.strikes, market.T) 
```

fitted params() returns JW scalars for the first slice; full array model.parameters has shape (5, nT ).

# 7 Worked example: BTC slice

Same data as load btc market(): F = 69028, T = 17/365, 32 strikes. One run (power law) gives approximately:

<table><tr><td>JW parameter</td><td>Value</td><td></td></tr><tr><td> $v$ </td><td>0.277</td><td>ATM variance level</td></tr><tr><td> $\psi$ </td><td>-0.162</td><td></td></tr><tr><td> $p$ </td><td>0.627</td><td></td></tr><tr><td> $c$ </td><td>0.304</td><td>(=  $p + 2\psi$  after refinement logic)</td></tr><tr><td> $v_{t}$ </td><td>0.244</td><td></td></tr><tr><td>RMSE (IV vs. mid)</td><td>≈ 0.014</td><td></td></tr></table>

Re-run the fit to refresh numbers; SSVI random restarts and SLSQP can cause small variation.

![](images/d0b83c9c7403c268ef1ad89e12e4782ab2ac85cf2d7038672df925931a5c8ce4.jpg)

<details>
<summary>line</summary>

| k = ln(K/F) | Implied vol σ |
| ----------- | ------------- |
| -0.58       | 1.02          |
| -0.50       | 0.95          |
| -0.42       | 0.90          |
| -0.34       | 0.83          |
| -0.26       | 0.78          |
| -0.18       | 0.72          |
| -0.10       | 0.65          |
| -0.02       | 0.58          |
| 0.04        | 0.52          |
| 0.06        | 0.50          |
| 0.08        | 0.49          |
| 0.10        | 0.48          |
| 0.12        | 0.48          |
| 0.14        | 0.49          |
| 0.16        | 0.50          |
| 0.18        | 0.51          |
| 0.20        | 0.52          |
| 0.22        | 0.53          |
| 0.24        | 0.54          |
| 0.26        | 0.55          |
| 0.28        | 0.56          |
| 0.30        | 0.57          |
| 0.32        | 0.58          |
| 0.34        | 0.59          |
| 0.36        | 0.60          |
| 0.38        | 0.61          |
| 0.40        | 0.62          |
</details>

Figure 1: BTC test slice: mids vs. SVI (power law) in $k = \ln ( K / F )$ space.

# 8 Code map

<table><tr><td>Module</td><td>Role</td></tr><tr><td>svi_models.py</td><td>svi_raw, svi_jumpwing, svi_natural</td></tr><tr><td>svi_fit/fit_svi_surface.py</td><td>Two-pass surface calibration</td></tr><tr><td>svi_fit/fit_ssvi.py</td><td>Global SSVI parameters</td></tr><tr><td>svi_fit/fit_svi.py</td><td>Per-slice JW refinement</td></tr><tr><td>volmodels/svi.py</td><td>SVIModel wrapper</td></tr></table>

Package import path: volmodel svi → volmodel-svi (symlink, if configured like GEDI).