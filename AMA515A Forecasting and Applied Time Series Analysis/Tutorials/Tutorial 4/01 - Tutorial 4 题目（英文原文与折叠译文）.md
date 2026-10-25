---
course: "AMA515A Forecasting and Applied Time Series Analysis"
source: "Tutorial Exercise 4.pdf"
pages: 2
cssclasses: [ama-inline-translations]
---

# Tutorial 4 题目

原始资料：[Tutorial Exercise 4.pdf](<附件/Tutorial Exercise 4.pdf>)（2 页）。

相关资料：[[00 - Tutorial 4 资料索引]] · [[02 - Tutorial 4 Answers（英文原文与折叠译文）]]

## PDF p.1

Ex.4 Time series <details class="translation-details"><summary>中文译文</summary><span class="translation-body">练习 4：时间序列。</span></details>

### 1.

Find the partial ACF of the AR(2) process given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">求下列 AR(2) 过程的偏自相关函数。</span></details>

$$
X_t=(1/3)X_{t-1}+(2/9)X_{t-2}+a_t
$$

### 2.

Sketch the autocorrelation function of the process <details class="translation-details"><summary>中文译文</summary><span class="translation-body">画出下列过程自相关函数的示意图。</span></details>

$$
y_t=-0.5y_{t-1}+a_t-0.8a_{t-1}
$$

### 3.

The first eight values of the ACF and partial ACF of 60 observations on a quarterly economic index, and of the first differences, are shown below: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">某季度经济指数有 60 个观测值。原序列及其一阶差分的自相关函数和偏自相关函数，前八个值如下：</span></details>

| | Lag | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $X_t$ | $r_k$ | 0.95 | 0.91 | 0.87 | 0.82 | 0.79 | 0.74 | 0.7 | 0.67 |
| | $\phi_{kk}$ | 0.95 | 0.04 | -0.05 | 0.07 | 0 | 0.07 | -0.04 | -0.02 |
| $\nabla X_t$ | $r_k$ | 0.02 | 0.08 | 0.12 | 0.05 | -0.02 | -0.05 | -0.01 | 0.03 |
| | $\phi_{kk}$ | 0.02 | 0.08 | 0.06 | 0.03 | -0.05 | -0.06 | -0.04 | -0.02 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">Lag：滞后阶数。Xₜ 为原序列，∇Xₜ 为一阶差分；rₖ 为样本自相关系数，φₖₖ 为样本偏自相关系数。</span></details>

Identify a model for the series. What can be done in order to make a better job of formulating a 'good' model? <details class="translation-details"><summary>中文译文</summary><span class="translation-body">为该序列识别一个模型。为了更好地建立一个“好”模型，还可以做些什么？</span></details>

### 4.

The following tables presents the SAC, and SPAC of a data set of 150 observations. Tentatively identify a model describing this series. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">下表给出一组含 150 个观测值的数据的样本自相关（SAC）和样本偏自相关（SPAC）。初步识别一个描述该序列的模型。</span></details>

| Lag | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SAC | -0.42 | 0.32 | 0.05 | 0.01 | -0.11 | 0.11 | -0.11 | 0.01 | 0.04 | -0.04 |
| SPAC | -0.42 | 0.18 | 0.29 | 0.07 | -0.26 | -0.07 | 0.04 | 0.03 | 0.04 | -0.02 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头 Lag 为滞后阶数；SAC 为样本自相关，SPAC 为样本偏自相关。</span></details>

### 5.

(a) Show that the following time series $\{X_t\}$ is stationary. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(a) 证明下列时间序列 Xₜ 平稳。</span></details>

$$
X_t=0.7X_{t-1}-0.1X_{t-2}+Z_t,\qquad \{Z_t\}\sim NID(0,\sigma^2)
$$

(b) A stationary time series has a white noise representation, i.e., <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(b) 平稳时间序列具有白噪声表示，即：</span></details>

$$
X_t=\sum_{j=0}^{\infty}\psi_jZ_{t-j},\quad \&\quad\sum_{j=0}^{\infty}|\psi_j|<\infty
$$

Using partial fraction or otherwise, find $\psi_4$ for the time series in (a). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">使用部分分式分解或其他方法，求 (a) 中时间序列的 ψ₄。</span></details>

Hint: Use the backshift operator representation. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">提示：使用滞后算子表示。</span></details>

(Ans: $\psi_4=0.1031$) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（答案：ψ₄ = 0.1031。）</span></details>

> [!note]- 原页对照 · PDF p.1
> ![[附件/tut4-questions-p01.png]]

## PDF p.2

### 6.

Consider the AR(2) process $X_t$ satisfying <details class="translation-details"><summary>中文译文</summary><span class="translation-body">考虑满足下式的 AR(2) 过程 Xₜ：</span></details>

$$
X_t-\phi X_{t-1}-\phi^2X_{t-2}=a_t,\quad a_t\sim NID(0,\sigma^2).
$$

(i) For what values of $\phi$ is this a stationary process? <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(i) φ 取哪些值时，这个过程平稳？</span></details>

(ii) The following sample moments were observed: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(ii) 观测到下列样本矩：</span></details>

$$
\hat{\gamma}(0)=6.06,\quad \hat{\rho}(1)=0.687,\quad \hat{\rho}(2)=0.61
$$

Find estimates of $\phi$ & $\sigma^2$ by solving the Yule-Walker equations. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">通过求解 Yule–Walker 方程，求 φ 和 σ² 的估计值。</span></details>

### 7.

Derive the infinite moving average representation of the model <details class="translation-details"><summary>中文译文</summary><span class="translation-body">推导下列模型的无穷阶移动平均表示。</span></details>

$$
X_t=0.6X_{t-1}+\varepsilon_t+0.3\varepsilon_{t-1},\quad\varepsilon_t\sim WN(0,\sigma^2).
$$

### 8.

Suggest a plausible ARMA model for a series of 100 observations whose first ten sample autocorrelation coefficients are 0.61, 0.47, -0.05, 0.06, -0.21, 0.11, 0.08, 0.05, 0.12, -0.01. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">某序列包含 100 个观测值，其前十个样本自相关系数为 0.61、0.47、−0.05、0.06、−0.21、0.11、0.08、0.05、0.12、−0.01。请提出一个合理的 ARMA 模型。</span></details>

> [!note]- 原页对照 · PDF p.2
> ![[附件/tut4-questions-p02.png]]
