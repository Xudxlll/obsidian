---
course: "AMA515A Forecasting and Applied Time Series Analysis"
source: "Tutorial 4 Answers .pdf"
pages: 1
cssclasses: [ama-inline-translations]
---

# Tutorial 4 Answers

原始资料：[Tutorial 4 Answers .pdf](<附件/Tutorial 4 Answers .pdf>)（1 页；原文件名在 Answers 与 .pdf 之间有一个空格，附件保留该名称）。

相关资料：[[00 - Tutorial 4 资料索引]] · [[01 - Tutorial 4 题目（英文原文与折叠译文）]]

## PDF p.1

Ans-Ex4 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">练习 4 答案。</span></details>

### 1.

$$
\phi_{11}=3/7,\quad \phi_{22}=2/9.
$$

Note that $\phi_{11}=\rho_1,\phi_{22}=(\rho_2-\rho_1^2)/(1-\rho_1^2)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意 φ₁₁ = ρ₁，φ₂₂ = (ρ₂ − ρ₁²)/(1 − ρ₁²)。</span></details>

### 2.

For ARMA(1,1) process, i.e., <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对于 ARMA(1,1) 过程，即：</span></details>

$$
y_t=\alpha y_{t-1}+\beta\varepsilon_{t-1}+\varepsilon_t,
$$

its ACF is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其自相关函数为：</span></details>

$$
\begin{aligned}
\rho_1&=(1+\alpha\beta)(\alpha+\beta)/(1+\beta^2+2\alpha\beta)=-0.746,\\
\rho_k&=\alpha\rho_{k-1},\quad k=2,3,\ldots
\end{aligned}
$$

hence you can plot $\rho_k$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此可以画出 ρₖ。</span></details>

### 3.

Possible model is $\nabla X_t=a_t$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">一个可能的模型是 ∇Xₜ = aₜ。</span></details>

The obvious problem here is the sample size is too small. One thing that should be done is to increase the sample size. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这里明显的问题是样本量太小。一项应做的工作是增加样本量。</span></details>

### 4.

MA(2) is reasonable. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">MA(2) 是合理的选择。</span></details>

### 5.

(a) $B=2$ or $5$, which are larger than 1. Hence time series is stationary. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(a) B = 2 或 5，均大于 1。因此该时间序列平稳。</span></details>

(b) Because $(1-0.5B)(1-0.2B)X_t=Z_t$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(b) 因为 (1 − 0.5B)(1 − 0.2B)Xₜ = Zₜ。</span></details>

Coef. of $B^4$ is 0.1031. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">B⁴ 的系数为 0.1031。</span></details>

### 6.

$$
\text{(i)}\quad |\phi|<\frac{-1+\sqrt5}{2}
$$

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">(i) φ 的绝对值小于 (−1 + √5)/2。</span></details>

(ii)

$$
\begin{aligned}
X_t&=\phi_1X_{t-1}+\phi_2X_{t-2}+a_t\\
\Rightarrow X_tX_{t-j}&=\phi_1X_{t-1}X_{t-j}+\phi_2X_{t-2}X_{t-j}+a_tX_{t-j},
\end{aligned}
$$

Consider j=0, 1, 2 and take expectation. $\phi=0.509,\sigma^2=2.98$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">考虑 j = 0、1、2 并取期望，得到 φ = 0.509、σ² = 2.98。</span></details>

### 7.

ARMA(1,1), bookwork.. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">ARMA(1,1)，按教材中的方法处理。</span></details>

### 8.

MA(2) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">二阶移动平均模型 MA(2)。</span></details>

> [!note] 原资料范围
> 第 7 题的原答案只有“ARMA(1,1), bookwork..”，未给出无穷阶展开；此处按原件保留，未补写推导。第 6(ii) 的原答案先用一般 AR(2) 记号 $\phi_1,\phi_2$ 写关系式，再给出 $\phi$ 和 $\sigma^2$ 的数值，笔记保留这一记号顺序。

> [!note]- 原页对照 · PDF p.1
> ![[附件/tut4-answers-p01.png]]
