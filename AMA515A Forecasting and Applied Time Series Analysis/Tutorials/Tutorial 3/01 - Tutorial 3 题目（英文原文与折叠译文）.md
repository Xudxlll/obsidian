---
course: "AMA515A Forecasting and Applied Time Series Analysis"
source: "Tutorial 3.pdf"
pages: 1
cssclasses: [ama-inline-translations]
---

# Tutorial 3 题目

原始资料：[Tutorial 3.pdf](<附件/Tutorial 3.pdf>)（1 页）。

相关资料：[[00 - Tutorial 3 资料索引]] · [[02 - Tutorial 3 Answers（英文原文与折叠译文）]] · [[03 - Tutorial 3 Solution（手写解答）]]

## PDF p.1

EX.3 Time series <details class="translation-details"><summary>中文译文</summary><span class="translation-body">练习 3：时间序列。</span></details>

### 1.

Verify that the autoregressive process <details class="translation-details"><summary>中文译文</summary><span class="translation-body">验证下列自回归过程的平稳性。</span></details>

$$
X_t=(X_{t-1}+X_{t-2})/12+Z_t
$$

where $\{Z_t\}$ is white noise, is stationary, and find its autocorrelation function. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 Zₜ 为白噪声；并求该过程的自相关函数。</span></details>

### 2.

Plot the autocorrelation function (up to lag 10) of the second order autoregressive process <details class="translation-details"><summary>中文译文</summary><span class="translation-body">画出下列二阶自回归过程的自相关函数，画至滞后 10 阶。</span></details>

$$
X_t=\alpha_1X_{t-1}+\alpha_2X_{t-2}+Z_t,
$$

where $\{Z_t\}$ is white noise, for each of <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 Zₜ 为白噪声；分别考虑以下两组参数。</span></details>

$$
(\alpha_1,\alpha_2)=(0.3,0.5)\ \text{and}\ (0.3,-0.5).
$$

### 3.

Consider the process <details class="translation-details"><summary>中文译文</summary><span class="translation-body">考虑下列过程。</span></details>

$$
X_t=A\cos(wt)+B\sin(wt),\quad t=0,1,2,\ldots,
$$

where A and B are uncorrelated random variables with zero mean and unit variance, $w$ is a constant and $w\in[0,\pi]$. Show that $X_t$ is stationary. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 A 和 B 是互不相关、均值为零且方差为一的随机变量；w 是常数，且在 0 到 π 之间（含端点）。证明 Xₜ 平稳。</span></details>

### 4.

You are given the ARMA process: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">给定下列 ARMA 过程：</span></details>

$$
y_t=12+0.4y_{t-1}+0.1y_{t-2}+\varepsilon_t+0.3\varepsilon_{t-1}-0.2\varepsilon_{t-2}
$$

Find the mean of $y_t$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">求 yₜ 的均值。</span></details>

### 5.

Find the autocorrelation function for the process defined by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">求下列过程的自相关函数。</span></details>

$$
Z_t=5+a_t-0.5a_{t-1}+0.25a_{t-2},
$$

where $\{a_t\}$ is a white noise process. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 aₜ 为白噪声过程。</span></details>

### 6.

For the ARMA(1,2) model <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对于下列 ARMA(1,2) 模型：</span></details>

$$
Z_t=0.8Z_{t-1}+a_t+0.7a_{t-1}+0.6a_{t-2}
$$

Show that (a) $\rho_k=0.8\rho_{k-1}$ for $k\geq3$ and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">证明：(a) 当 k ≥ 3 时，ρₖ = 0.8ρₖ₋₁；以及</span></details>

$$
\text{(b)}\quad \rho_2=0.8\rho_1+0.6\sigma_a^2/\gamma_0.
$$

Here $\gamma_0=E(Z_t^2)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这里 γ₀ = E(Zₜ²)；(b) 要证明 ρ₂ = 0.8ρ₁ + 0.6σₐ²/γ₀。</span></details>

### 7.

For the process <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对于下列过程：</span></details>

$$
y_t=0.3y_{t-1}+0.2y_{t-2}+\varepsilon_t-\theta_1\varepsilon_{t-1}-\theta_2\varepsilon_{t-2}
$$

you are given $\rho_1=0.8,\rho_2=-0.2$. Find $\rho_4$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">已知 ρ₁ = 0.8、ρ₂ = −0.2，求 ρ₄。</span></details>

Hint: Is $y_t$ stationary? <details class="translation-details"><summary>中文译文</summary><span class="translation-body">提示：yₜ 平稳吗？</span></details>

> [!note]- 原页对照 · PDF p.1
> ![[附件/tut3-questions-p01.png]]
