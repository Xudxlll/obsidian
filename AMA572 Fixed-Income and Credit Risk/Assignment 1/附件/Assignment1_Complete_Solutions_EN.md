---
lang: en-US
---

**AMA572 · Assignment 1 — Complete Solutions**  
**Deadline:** September 25, 2026

# Q1. Credit Rating Transition Matrices

Use the state order $(A,B,C,D)$, where $D$ is the absorbing default state. Following the corresponding lecture example, interpret “ten months later” as **month 10 measured from the beginning of the year**.

## 1. Empirical estimator

Count each firm's transition from its initial rating to its year-end rating. The denominator is the number initially in that rating, not the year-end population. The initially B-rated firms that move to A or C remain there for the rest of the year.

| Initial rating | Final A | Final B | Final C | Final D | Initial total |
|:---:|---:|---:|---:|---:|---:|
| A | 17 | 3 | 0 | 0 | 20 |
| B | 2 | 16 | 2 | 0 | 20 |
| C | 0 | 2 | 15 | 3 | 20 |

The empirical estimate is therefore

$$
\boxed{
\widehat P_{\mathrm{emp}}=
\begin{pmatrix}
0.85&0.15&0&0\\
0.10&0.80&0.10&0\\
0&0.10&0.75&0.15\\
0&0&0&1
\end{pmatrix}.}
$$

The last row follows from the assumption that default is absorbing.

## 2. Total time spent in each rating

Let $N_i$ be the total time spent in rating $i$ by all firms, measured in **firm-years**. Include the time spent after entry by firms that migrate into the rating.

$$
\begin{aligned}
N_A
&=17\times1+3\times\frac3{12}+2\times\frac{11}{12}
=\frac{235}{12},\\[4pt]
N_B
&=16\times1+4\times\frac1{12}
+3\times\frac9{12}+2\times\frac5{12}
=\frac{233}{12},\\[4pt]
N_C
&=15\times1+3\times\frac7{12}
+2\times\frac{10}{12}+2\times\frac{11}{12}
=\frac{243}{12}.
\end{aligned}
$$

For example, $N_C$ includes 15 firms that remain in C all year; three that leave C at month 7 (two move to B and one defaults); two that default at month 10; and two that enter C from B at month 1 and remain for 11 months.

\newpage

## 3. Generator-based estimator

Let $M_{ij}$ denote the number of observed transitions from $i$ to $j$. The nonzero counts are

$$
M_{AB}=3,\quad M_{BA}=2,\quad M_{BC}=2,
\quad M_{CB}=2,\quad M_{CD}=3.
$$

For $i\ne j$, estimate the transition intensity by

$$
\widehat\lambda_{ij}=\frac{M_{ij}}{N_i},
\qquad
\widehat\Lambda_{ii}=-\sum_{j\ne i}\widehat\lambda_{ij}.
$$

The estimated generator, in annual units, is

$$
\boxed{
\widehat\Lambda=
\begin{pmatrix}
-\frac{36}{235}&\frac{36}{235}&0&0\\[3pt]
\frac{24}{233}&-\frac{48}{233}&\frac{24}{233}&0\\[3pt]
0&\frac{24}{243}&-\frac{60}{243}&\frac{36}{243}\\[3pt]
0&0&0&0
\end{pmatrix}.}
$$

Numerically,

$$
\widehat\Lambda\approx
\begin{pmatrix}
-0.15319149&0.15319149&0&0\\
0.10300429&-0.20600858&0.10300429&0\\
0&0.09876543&-0.24691358&0.14814815\\
0&0&0&0
\end{pmatrix}.
$$

The one-year transition matrix is the **matrix exponential** $\exp(\widehat\Lambda\times1)$, not the elementwise exponential. Evaluating it using the exact fractions gives

$$
\boxed{
\widehat P_{\mathrm{gen}}\approx
\begin{pmatrix}
0.86463112&0.12857177&0.00646155&0.00033556\\
0.08645026&0.82446825&0.08249711&0.00658438\\
0.00416588&0.07910217&0.78524551&0.13148645\\
0&0&0&1
\end{pmatrix}.}
$$

**Checks.** Each generator row sums to zero. The transition matrix is nonnegative, its rows sum to one up to rounding, and default remains absorbing. The generator model allows multiple transitions within a year, so it can assign a positive A-to-C probability even without an observed direct A-to-C transition.

As a further check, the total time spent in default is

$$
N_D=\frac5{12}+2\times\frac2{12}=\frac9{12},
\qquad
N_A+N_B+N_C+N_D=60\text{ firm-years}.
$$

\newpage

# Q2. Piecewise Implied Default Parameters

Use the **linear expected-loss approximation** in Lecture 1: match the price difference between a risk-free bond and a corporate bond to weighted discounted default losses. Let $P_1$ apply to years 1–3 and $P_2$ to years 4–5. These are annual default weights under the lecture convention, not exact continuous-time hazard rates.

Take face value 100, annual coupon $c=4.1$, recovery amount $R=40$, and continuously compounded risk-free rate $r=0.025$. Scaling all cash flows by the same factor does not change the estimated parameters.

## 1. Three-year bond: estimate $P_1$

Using the quoted continuously compounded yield, the corporate bond price is

$$
\begin{aligned}
B_3
&=4.1e^{-0.046}+4.1e^{-0.046\times2}
+104.1e^{-0.046\times3}\\
&=98.33667697.
\end{aligned}
$$

The price of the risk-free bond with identical promised cash flows is

$$
\begin{aligned}
B_3^{\mathrm{rf}}
&=4.1e^{-0.025}+4.1e^{-0.025\times2}
+104.1e^{-0.025\times3}\\
&=104.47690821.
\end{aligned}
$$

Let $V_n^{\mathrm{rf}}(t)$ be the time-$t$ risk-free value of the remaining promised payments of the $n$-year bond. The default loss discounted to time zero is

$$
L_n(t)=\bigl[V_n^{\mathrm{rf}}(t)-40\bigr]e^{-0.025t}.
$$

| Default time $t$ | $V_3^{\mathrm{rf}}(t)$ | Loss | Discount factor | $L_3(t)$ |
|---:|---:|---:|---:|---:|
| 0.5 | 105.791066 | 65.791066 | 0.987578 | 64.973796 |
| 1.5 | 104.317608 | 64.317608 | 0.963194 | 61.950361 |
| 2.5 | 102.806849 | 62.806849 | 0.939413 | 59.001574 |

For example, at $t=0.5$, the remaining payments are due at years 1, 2, and 3:

$$
V_3^{\mathrm{rf}}(0.5)
=4.1e^{-0.025\times0.5}+4.1e^{-0.025\times1.5}
+104.1e^{-0.025\times2.5}.
$$

Matching the price difference to expected losses gives

$$
104.47690821-98.33667697=185.92573146P_1.
$$

Hence,

$$
\boxed{P_1=0.03302518263\approx3.3025\%\text{ per year}.}
$$

\newpage

## 2. Five-year bond: estimate $P_2$ for years 4–5

The corporate and risk-free bond prices are

$$
\begin{aligned}
B_5
&=4.1\sum_{k=1}^{4}e^{-0.0475k}+104.1e^{-0.0475\times5}
=96.67716974,\\[3pt]
B_5^{\mathrm{rf}}
&=4.1\sum_{k=1}^{4}e^{-0.025k}+104.1e^{-0.025\times5}
=107.28032055.
\end{aligned}
$$

The discounted losses at the possible default dates are as follows.

| Time $t$ | $V_5^{\mathrm{rf}}(t)$ | Loss | Discount factor | $L_5(t)$ | Weight |
|---:|---:|---:|---:|---:|:---:|
| 0.5 | 108.629741 | 68.629741 | 0.987578 | 67.777209 | $P_1$ |
| 1.5 | 107.228144 | 67.228144 | 0.963194 | 64.753773 | $P_1$ |
| 2.5 | 105.791066 | 65.791066 | 0.939413 | 61.804987 | $P_1$ |
| 3.5 | 104.317608 | 64.317608 | 0.916219 | 58.929006 | $P_2$ |
| 4.5 | 102.806849 | 62.806849 | 0.893597 | 56.124034 | $P_2$ |

The sum of discounted loss coefficients for years 1–3 is

$$
67.77720853+64.75377320+61.80498675=194.33596848.
$$

For years 4–5, the sum is

$$
58.92900611+56.12403367=115.05303978.
$$

The five-year valuation must use the previously estimated $P_1$ together with the unknown $P_2$:

$$
107.28032055-96.67716974
=194.33596848P_1+115.05303978P_2.
$$

Substituting $P_1=0.03302518263$ gives

$$
\begin{aligned}
P_2
&=\frac{10.60315080-194.33596848\times0.03302518263}
{115.05303978}\\[4pt]
&=0.03637600501.
\end{aligned}
$$

Thus, under the lecture's linear approximation,

$$
\boxed{P_1\approx3.3025\%\text{ per year},
\qquad P_2\approx3.6376\%\text{ per year}.}
$$

**Check and interpretation.** Substituting the unrounded estimates reproduces expected losses of 6.14023124 and 10.60315080, equal to the respective bond price differences. Since $P_2$ applies only to years 4–5, it cannot be obtained by dividing the five-year price difference by the sum of all five loss coefficients.

\newpage

# Q3. Tax Credit and Bankruptcy Cost under GBM

Equations (1) and (2) on page 4 of Lecture 2 are

$$
A(0)=E^*\!\left[e^{-rT}\kappa D\,\mathbf1_{\{V_T\ge D\}}\right],
$$

$$
C(0)=E^*\!\left[e^{-rT}(1-\alpha)V_T\,\mathbf1_{\{V_T<D\}}\right].
$$

Here $D$ is the face value of debt, $\kappa$ is the tax-credit coefficient, and $\alpha$ is the fraction of asset value retained upon default. Under the risk-neutral measure, the assignment appendix specifies

$$
dV_t=rV_t\,dt+\sigma V_t\,dW_t,\qquad V_0=1.
$$

Assume $T>0$, $D>0$, and $\sigma>0$. Let $\Phi$ denote the standard normal cumulative distribution function.

## 1. Distribution of $\ln V_T$

For $f(v)=\ln v$, we have $f'(v)=1/v$ and $f''(v)=-1/v^2$. Itô's lemma gives

$$
\begin{aligned}
d\ln V_t
&=\frac1{V_t}(rV_t\,dt+\sigma V_t\,dW_t)
+\frac12\left(-\frac1{V_t^2}\right)\sigma^2V_t^2\,dt\\
&=\left(r-\frac12\sigma^2\right)dt+\sigma\,dW_t.
\end{aligned}
$$

Integrating and using $V_0=1$ yields

$$
\ln V_T=\left(r-\frac12\sigma^2\right)T+\sigma W_T.
$$

Since $W_T\sim N(0,T)$,

$$
\ln V_T\sim N\!\left(\left(r-\frac12\sigma^2\right)T,\sigma^2T\right).
$$

## 2. Tax credit $A(0)$

Define

$$
d_2=\frac{-\ln D+(r-\frac12\sigma^2)T}{\sigma\sqrt T},
\qquad d_1=d_2+\sigma\sqrt T.
$$

Using $E^*[\mathbf1_E]=P^*(E)$ and

$$
P^*(V_T<D)
=\Phi\!\left(\frac{\ln D-(r-\frac12\sigma^2)T}{\sigma\sqrt T}\right)
=\Phi(-d_2),
$$

we obtain

$$
\boxed{A(0)=\kappa D e^{-rT}\Phi(d_2).}
$$

This is the tax credit multiplied by the probability of survival to maturity, discounted to time zero.

\newpage

## 3. Bankruptcy cost $C(0)$

Bankruptcy cost depends on asset value at default. We therefore need the **truncated expectation** $E^*[V_T\mathbf1_{\{V_T<D\}}]$; the random variable $V_T$ cannot simply be taken outside the expectation.

Write

$$
m=\left(r-\frac12\sigma^2\right)T,\qquad
s=\sigma\sqrt T,\qquad \ln V_T=m+sZ,\quad Z\sim N(0,1).
$$

The default event is equivalent to $Z<h$, where $h=(\ln D-m)/s=-d_2$. Thus,

$$
\begin{aligned}
E^*[V_T\mathbf1_{\{V_T<D\}}]
&=\int_{-\infty}^{h}e^{m+sz}\frac1{\sqrt{2\pi}}e^{-z^2/2}\,dz\\
&=e^{m+s^2/2}\int_{-\infty}^{h}
\frac1{\sqrt{2\pi}}e^{-(z-s)^2/2}\,dz\\
&=e^{m+s^2/2}\Phi(h-s)\\
&=e^{rT}\Phi(-d_1).
\end{aligned}
$$

The second equality follows by completing the square:

$$
 m+sz-\frac{z^2}{2}
=m+\frac{s^2}{2}-\frac{(z-s)^2}{2}.
$$

Consequently,

$$
\boxed{C(0)=e^{-rT}(1-\alpha)e^{rT}\Phi(-d_1)
=(1-\alpha)\Phi(-d_1).}
$$

**Final results for the specified initial value $V_0=1$:**

$$
\boxed{
\begin{aligned}
A(0)&=\kappa D e^{-rT}
\Phi\!\left(\frac{-\ln D+(r-\frac12\sigma^2)T}{\sigma\sqrt T}\right),\\[6pt]
C(0)&=(1-\alpha)
\Phi\!\left(\frac{\ln D-(r+\frac12\sigma^2)T}{\sigma\sqrt T}\right).
\end{aligned}}
$$

For a general initial value $V_0>0$, the corresponding formulas are

$$
d_{1,2}=\frac{\ln(V_0/D)+(r\pm\frac12\sigma^2)T}{\sigma\sqrt T},
\quad A(0)=\kappa D e^{-rT}\Phi(d_2),
\quad C(0)=(1-\alpha)V_0\Phi(-d_1).
$$

Use the plus sign for $d_1$ and the minus sign for $d_2$. Since the lognormal distribution is continuous, $P^*(V_T=D)=0$; strict and non-strict inequalities therefore give the same expectations here.

**Sources:** Lecture 1, pp. 6–9 and 13–14; Lecture 2, p. 4, and both supplementary derivations. All inputs follow Assignment 1. The companion *Conventions and Errata* explains the approximation in Q2 and the relevant typographical issues.
