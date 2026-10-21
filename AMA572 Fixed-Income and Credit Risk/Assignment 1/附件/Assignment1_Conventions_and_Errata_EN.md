---
lang: en-US
---

# Assignment 1: Conventions and Errata

This note explains the differences between the complete solutions and the supplied course materials. Full derivations and answers are provided in **Assignment1_Complete_Solutions_EN.pdf** in the same folder.

## 1. Q1: Assignment data versus the lecture exercise

In the assignment, two firms move from B to C and three move from A to B. In the lecture exercise, the corresponding counts are one and one. The exposure times, generator matrix, and transition matrix in the old exercise solution therefore cannot be copied directly.

Following the example and calculations in Lecture 1, “ten months later” is interpreted as **month 10 from the beginning of the year**, not ten months after month 7.

## 2. Q2: The lecture's linear expected-loss convention

The lecture tables multiply each year's discounted loss by an annual default parameter and then sum these terms. The main solution follows this convention: the three-year bond determines the parameter for years 1–3, and the five-year bond determines the parameter for years 4–5:

$$
P_1=3.302518263\%,\qquad P_2=3.637600501\%.
$$

In this linear expression, $P_1$ and $P_2$ are annual default-event probability weights. The lecture also describes them as default intensities or conditional default probabilities. A strictly conditional interpretation, however, requires survival probabilities for preceding years. A continuous-time intensity interpretation additionally requires a specified continuous-time default model. The main solution preserves the lecture convention and explicitly labels the approximation.

### Alternative: exact annual conditional default probabilities

The following illustrates the effect of a different convention. These parameters should not be mixed with the linear weights in the main solution.

Let $q_1$ be the annual conditional default probability in years 1–3 and $q_2$ the corresponding probability in years 4–5. Continue to place each year's default cash flow at midyear, as specified in the assignment. The unconditional default probabilities in years 1–3 are

$$
q_1,\quad(1-q_1)q_1,\quad(1-q_1)^2q_1,
$$

and those in years 4–5 are

$$
(1-q_1)^3q_2,\quad(1-q_1)^3(1-q_2)q_2.
$$

Weighting the discounted loss coefficients $L_n(j-0.5)$ by these probabilities and solving first for the three-year bond and then for the five-year bond gives

$$
q_1\approx3.414070146\%,\qquad q_2\approx4.120247608\%.
$$

The constant intensities with the same one-year survival probabilities are $-\ln(1-q_i)$: approximately 3.473710906% and 4.207535890% per year. This is only a conversion of one-year survival probabilities; it does not replace the midyear-default valuation model with a continuous-default model.

\newpage

## 3. Typographical issues in the lecture exercise solution

The following points were checked against the rendered pages 3–4 of the Lecture 1 exercise solution, including its handwritten annotations.

- The three-year loss table totals $178.4155P_1$, whereas the subsequent printed equation shows $78.4155P_1$. The handwritten annotation restores the leading 1. The printed result of 3.6721% uses the incorrect denominator and should not be carried over.
- The printed five-year table labels every year with $P_2$. The handwritten annotations change the first three rows to $P_1$. The main solution follows this correction: $P_1$ for years 1–3 and $P_2$ for years 4–5.
- The 1.5- and 2.5-year rows in that table contain ordering and numerical alignment issues. The main solution recalculates the remaining cash flows separately at each default date.
- The assignment changes the coupon and interest-rate inputs. The solution uses the assignment's 4.1% coupon, 2.5% risk-free rate, and yields of 4.6% and 4.75%, rather than reusing the old table values.

## 4. Q3: Integration limits and initial asset value

- When integrating over asset value $v$, the limits are $0$ and $D$.
- After substituting $x=\ln v$, the limits become $-\infty$ and $\ln D$; they cannot remain $0$ and $D$. Some intermediate expressions in the supplementary derivation do not update the limits consistently after substitution.
- In equation (16) on page 4 of the annotated supplement, a printed expression contains $\ln V_T$ where the default threshold requires $\ln D$. This is also corrected by hand.
- The assignment appendix specifies $V_0=1$. Thus the final expression for $C(0)$ contains no additional $V_0$ factor. For a general initial value, it is $(1-\alpha)V_0\Phi(-d_1)$.

## 5. Numerical verification

- The Q1 matrix exponential was computed with SciPy and independently checked using uniformization: a Poisson-weighted sum of powers of a stochastic matrix. Nonnegativity, row sums, the absorbing state, and total exposure time were also checked.
- Substituting the unrounded Q2 parameters reproduces the three- and five-year bond price differences of 6.1402312377 and 10.6031508027, respectively.
- The Q3 tax-credit and bankruptcy-cost formulas agree with direct numerical integration of the standard normal density for three parameter sets, covering both $V_0=1$ and a general $V_0>0$.
