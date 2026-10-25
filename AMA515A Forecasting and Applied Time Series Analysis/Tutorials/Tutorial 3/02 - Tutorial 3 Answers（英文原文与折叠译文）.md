---
course: "AMA515A Forecasting and Applied Time Series Analysis"
source: "Tutorial 3 Answers.pdf"
pages: 2
cssclasses: [ama-inline-translations]
---

# Tutorial 3 Answers

原始资料：[Tutorial 3 Answers.pdf](<附件/Tutorial 3 Answers.pdf>)（2 页）。

相关资料：[[00 - Tutorial 3 资料索引]] · [[01 - Tutorial 3 题目（英文原文与折叠译文）]] · [[03 - Tutorial 3 Solution（手写解答）]]

## PDF p.1

Ans to Ex.3 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">练习 3 答案。</span></details>

### 1.

$$
\begin{aligned}
1-(1/12)B-(1/12)B^2&=0\\
12-B-B^2&=0\\
B&=-4\ \text{or}\ 3
\end{aligned}
$$

Thus roots are outside unit circle and the process is stationary <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，根均位于单位圆外，该过程平稳。</span></details>

Using difference equation approach, we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">使用差分方程方法，可得：</span></details>

$$
\rho(k)=\frac{45}{77}\left(\frac13\right)^{|k|}+\frac{32}{77}\left(-\frac14\right)^{|k|},\quad k=0,\pm1,\pm2,\ldots
$$

### 2.

| AR parameters | $k$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| (0.3,0.5) | $\rho(k)$ | 0.6 | 0.68 | 0.5 | 0.49 | 0.40 | 0.37 | 0.31 | 0.28 | 0.24 | 0.21 |
| (0.3,-0.5) | | 0.2 | -.44 | 0.23 | 0.15 | 0.16 | -0.027 | -0.09 | -0.013 | 0.04 | 0.019 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表中 AR parameters 为自回归参数，k 为滞后阶数，ρ(k) 为自相关系数；两行分别对应参数 (0.3, 0.5) 与 (0.3, −0.5)。</span></details>

> [!warning] 原资料疑点（照录保留）
> 第二组参数在 $k=3$ 时，印刷表写作 $0.23$；手写 Solution 的 PDF p.2 同一位置写作 $-0.232$。此处保留印刷原值，不将两个版本合并或擅自改正。

### 3.

Check (i) constant mean, (ii) constant variance, and (iii) covariance does not depend on time. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">检查：(i) 均值恒定；(ii) 方差恒定；(iii) 协方差不随时间变化。</span></details>

### 4.

Since the constant 12 does not affect stationarity, we can check stationarity by looking at the process <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由于常数 12 不影响平稳性，可以通过考察下列过程来检查平稳性。</span></details>

$$
y_t=0.4y_{t-1}+0.1y_{t-2}.
$$

Namely we look at the equation $1-0.4B-0.1B^2=0$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">即考察方程 1 − 0.4B − 0.1B² = 0。</span></details>

The roots are outside the unit circle, hence time series is stationary. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">根位于单位圆外，因此该时间序列平稳。</span></details>

Then $E(y_t)=12+0.4E(y_{t-1})+0.1E(y_{t-2})$, which means <details class="translation-details"><summary>中文译文</summary><span class="translation-body">于是 E(yₜ) = 12 + 0.4E(yₜ₋₁) + 0.1E(yₜ₋₂)，即：</span></details>

$$
\mu=12+0.4\mu+0.1\mu
$$

and $\mu=24$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此 μ = 24。</span></details>

### 5.

MA(2), bookwork. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">MA(2)，按教材中的方法处理。</span></details>

$$
\rho(0)=1,\quad \rho(1)=-10/21,\quad \rho(2)=4/21,\quad \rho(k)=0\ \text{for}\ k\geq3.
$$

> [!note]- 原页对照 · PDF p.1
> ![[附件/tut3-answers-p01.png]]

## PDF p.2

### 6.

$$
Z_tZ_{t-k}=0.8Z_{t-1}Z_{t-k}+a_tZ_{t-k}+0.7a_{t-1}Z_{t-k}+0.6a_{t-2}Z_{t-k}\tag{*}
$$

Now because $Z_t$ has $a_t$ as its leading term in its series expansion, and recall <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由于 Zₜ 的级数展开首项为 aₜ，并回顾：</span></details>

$$
\gamma(k)=E(Z_tZ_{t-k})\quad(\because E(Z_t)=0),\qquad \rho_k=\gamma_k/\gamma_0.
$$

Thus for $k\geq3$, the last 3 terms in (\*) has zero expectation and $\rho_k=0.8\rho_{k-1}$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，当 k ≥ 3 时，式 (*) 的后三项期望为零，故 ρₖ = 0.8ρₖ₋₁。</span></details>

For $k=2$, $\gamma_2=0.8\gamma_1+0.6E(a_{t-2}Z_{t-2})$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">当 k = 2 时，γ₂ = 0.8γ₁ + 0.6E(aₜ₋₂Zₜ₋₂)。</span></details>

But <details class="translation-details"><summary>中文译文</summary><span class="translation-body">而：</span></details>

$$
E(a_{t-2}Z_{t-2})=E\left(a_{t-2}(0.8Z_{t-3}+a_{t-2}+0.7a_{t-3}+0.6a_{t-4})\right)=\sigma_a^2.
$$

Thus $\rho_2=0.8\rho_1+0.6\dfrac{\sigma_a^2}{\gamma_0}$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此 ρ₂ = 0.8ρ₁ + 0.6σₐ²/γ₀。</span></details>

Note $\rho_1=0.8+1.6\dfrac{\sigma_a^2}{\gamma_0}$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意 ρ₁ = 0.8 + 1.6σₐ²/γ₀。</span></details>

### 7.

The process is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">该过程为：</span></details>

$$
y_t=0.3y_{t-1}+0.2y_{t-2}+\varepsilon_t-\theta_1\varepsilon_{t-1}-\theta_2\varepsilon_{t-2}\tag{**}
$$

Consider $y_t=0.3y_{t-1}+0.2y_{t-2}$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">考虑 yₜ = 0.3yₜ₋₁ + 0.2yₜ₋₂。</span></details>

Then $B=\left|\dfrac{-3\pm\sqrt{89}}4\right|>1$. Hence time series is stationary and $E(y_t)=0$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">于是 B = |(−3 ± √89)/4| &gt; 1。因此时间序列平稳，且 E(yₜ) = 0。</span></details>

Then take expectation of (\*\*), then we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">再对式 (**) 取期望，可得：</span></details>

$$
\rho_k=0.3\rho_{k-1}+0.2\rho_{k-2},\quad\text{so}\quad \rho_3=0.1\ \&\ \rho_4=-0.01.
$$

> [!note] 原文记号保留
> 上述根的式子沿用原印刷资料的 $B=|\cdots|>1$ 写法。未将其改写为其他记号。

> [!note]- 原页对照 · PDF p.2
> ![[附件/tut3-answers-p02.png]]
