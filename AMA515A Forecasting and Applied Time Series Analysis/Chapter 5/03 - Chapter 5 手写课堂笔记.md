---
course: "AMA515A Forecasting and Applied Time Series Analysis"
chapter: 5
source: "Chapter 5 Notes.pdf"
pages: 8
cssclasses:
  - ama-inline-translations
---

# Chapter 5 手写课堂笔记（全文转录、折叠译文与原页）

> [!info] 阅读方式
> 本篇对应教师独立手写笔记 [Chapter 5 Notes.pdf](<附件/Chapter 5 Notes.pdf>)（共 8 页），按 PDF 页序逐页还原全部英文说明、数学推导、表格与例题演算，英文句子与标题附默认折叠的中文译文；每页附带原页扫描图供核对。原手写中的轻微笔误（如下标或上标漏写、个别帽子符号省略）均照录并在注记中标明。
> [本章资料索引](<05 - Chapter 5 资料索引.md>) · [印刷版讲义](<01 - Chapter 5 讲义（原页）.md>) · [带批注讲义](<02 - Chapter 5 带批注讲义（原页）.md>)

## PDF p.1

**Chapter 5 Notes (p. 1, ①): Minimum MSE Forecast & Forecast Error Derivation** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 5 章手写笔记（第 1 页）：最小均方误差（MSE）预测与预测误差推导。</span></details>

$$
\begin{aligned}
X_{i+l} = X_i(l) &= a_{i+l} + \psi_1 a_{i+l-1} + \psi_2 a_{i+l-2} + \cdots + \psi_{l-1} a_{i+1} \\
&\quad + (\psi_l a_i + \psi_{l+1} a_{i-1} + \psi_{l+2} a_{i-2} + \cdots) \\
-)\quad \hat{X}_i(l) &= \psi_l^* a_i + \psi_{l+1}^* a_{i-1} + \psi_{l+2}^* a_{i-2} + \psi_{l+3}^* a_{i-3} + \cdots \\
\hline
X_i(l) - \hat{X}_i(l) &= a_{i+l} + \psi_1 a_{i+l-1} + \psi_2 a_{i+l-2} + \cdots + \psi_{l-1} a_{i+1} \\
&\quad + (\psi_l - \psi_l^*) a_i + (\psi_{l+1} - \psi_{l+1}^*) a_{i-1} + \cdots \\
&= a_{i+l} + \psi_1 a_{i+l-1} + \psi_2 a_{i+l-2} + \cdots + \psi_{l-1} a_{i+1} \\
&\quad + \sum_{j=l}^{\infty} (\psi_j - \psi_j^*) a_{i-l}
\end{aligned}
$$

*(注：原手写求和项及下方方差式内将 $a_{i+l-j}$ 写作 $a_{i-l}$，且末行求和下限紧凑形似 $j=1$、括号 $(\psi_j-\psi_j^*)$ 漏写平方，照录如下。)*

$$
\begin{aligned}
E\left\{[X_{i+l} - \hat{X}_i(l)]^2\right\} &= E\left\{[e_i(l)]^2\right\} \\
&= V\left[a_{i+l} + \psi_1 a_{i+l-1} + \psi_2 a_{i+l-2} + \cdots + \psi_{l-1} a_{i+1} + \sum_{j=l}^{\infty} (\psi_j - \psi_j^*) a_{i-l}\right] \\
&= (1 + \psi_1^2 + \psi_2^2 + \cdots + \psi_{l-1}^2)\sigma_a^2 + \sum_{j=1}^{\infty} (\psi_j - \psi_j^*)\sigma_a^2
\end{aligned}
$$

If $\psi_j^* = \psi_j,\; j = l, l+1, \cdots,$ then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">若 ψ_j* = ψ_j（j = l, l+1, …），则：</span></details>

$$
\hat{X}_i(l) = \psi_l a_i + \psi_{l+1} a_{i-1} + \psi_{l+2} a_{i-2} + \cdots \tag{5.1}
$$

Thus the mean square error is a minimum. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由此使均方误差（MSE）达到最小。</span></details>

The forecast error at time period $i$ for lead $l$ is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">在时刻 i 对提前期（lead）l 的预测误差为：</span></details>

$$
\begin{aligned}
e_i(l) &= X_{i+l} - \hat{X}_i(l) = X_i(l) - \hat{X}_i(l) \\
&= a_{i+l} + \psi_1 a_{i+l-1} + \psi_2 a_{i+l-2} + \cdots + \psi_{l-1} a_{i+1}. \tag{5.2}
\end{aligned}
$$

> [!example]- 手写笔记 PDF 第 1 页原图
> ![[Chapter 5/附件/ch5-handwritten-p01.png]]

---

## PDF p.2

**Conditional Expectation $\underset{i}{E}$ (②)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">条件期望 E_i（第 2 页）。</span></details>

which gives a value — the expected value at time period $i$ of a certain random variable on or before time period $i$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">它给出某个随机变量在时刻 i（基于时刻 i 及之前信息）的条件期望值。</span></details>

$$
\underset{i}{E}[a_{i+l}] = \begin{cases} 0, & \text{if } l > 0 \quad (\text{for future observations}) \\ a_{i+l}, & \text{if } l \le 0 \quad (\text{for the past observations}) \end{cases}
$$

Hence equation $(5.1)$ gives <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此由式 (5.1) 可得：</span></details>

$$
\underset{i}{E}[\hat{X}_i(l)] = \hat{X}_i(l), \quad l > 0
$$

and $(5.2)$ gives <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由式 (5.2) 可得：</span></details>

$$
\underset{i}{E}[e_i(l)] = 0, \qquad l > 0; \tag{5.3}
$$

Forecast error has zero expected value. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">预测误差的期望为零。</span></details>

$$
\begin{aligned}
\underset{i}{E}[X_{i+l}] &= \underset{i}{E}[X_i(l)] = \hat{X}_i(l), \qquad l > 0; \tag{5.4} \\
\underset{i}{E}[X_{i+l}] &= \underset{i}{E}[X_i(l)] = X_i(l), \qquad l < 0;
\end{aligned}
$$

*(注：第二行手写为 $l < 0$，未加等号横线，实应含 $l \le 0$，照录。)*

forecasts are unbiased. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">预测是无偏的（unbiased）。</span></details>

$$
\begin{aligned}
V[e_i(l)] &= (1 + \psi_1^2 + \psi_2^2 + \cdots + \psi_{l-1}^2)\sigma_a^2 \qquad \text{with } \psi_j^* = \psi_j,\; j = l, l+1, l+2, \cdots \\
&= \left(\sum_{j=0}^{l-1} \psi_j^2\right) \sigma_a^2 \qquad \text{where } \psi_0 = 1
\end{aligned}
$$

> [!example]- 手写笔记 PDF 第 2 页原图
> ![[Chapter 5/附件/ch5-handwritten-p02.png]]

---

## PDF p.3

**Confidence Interval for Forecasts & 5.2 Forecasting Procedure (③)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">预测置信区间与 5.2 预测步骤（第 3 页）。</span></details>

Hence a $100(1-\alpha)\%$ confidence interval for the forecast is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，预测的 100(1−α)% 置信区间为：</span></details>

$$
\hat{X}_i(l) \pm k_{\frac{\alpha}{2}} \sqrt{\left(\sum_{j=0}^{l-1} \psi_j^2\right) \sigma_a^2} \tag{5.5a}
$$

If, for large series (i.e. $n \ge 30$), then replace $\sigma_a^2$ by $\hat{\sigma}_a^2$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">若为大样本序列（即 n ≥ 30），则用 σ̂_a² 替代 σ_a²（注：手写根号内 σ_a² 漏画了帽子符号，照录）：</span></details>

$$
\hat{X}_i(l) \pm z_{\frac{\alpha}{2}} \sqrt{\left(\sum_{j=0}^{l-1} \psi_j^2\right) \sigma_a^2}.
$$

### 5.2 Forecasting Procedure <details class="translation-details"><summary>中文译文</summary><span class="translation-body">5.2 预测步骤。</span></details>

The form of an $\text{ARMA}(p, q)$ process is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">ARMA(p, q) 过程的形式为：</span></details>

$$
\begin{aligned}
X_{i+l} = X_i(l) &= \phi_1 X_{i+l-1} + \phi_2 X_{i+l-2} + \cdots + \phi_p X_{i+l-p} + a_{i+l} \\
&\quad + \theta_1 a_{i+l-1} + \theta_2 a_{i+l-2} + \cdots + \theta_q a_{i+l-q}
\end{aligned}
$$

Take conditional expectation at time period $i$, for $l > 0$, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对 l &gt; 0，在时刻 i 取条件期望：</span></details>

$$
\begin{aligned}
E[X_{i+l}] &= E[X_i(l)] \\
&= \hat{X}_i(l) \\
&= \phi_1 E[X_{i+l-1}] + \phi_2 E[X_{i+l-2}] + \cdots + \phi_p E[X_{i+l-p}] \\
&\quad + 0 + \theta_1 E[a_{i+l-1}] + \theta_2 E[a_{i+l-2}] + \cdots + \theta_q E[a_{i+l-q}] \tag{5.6}
\end{aligned}
$$

Thus, for $1 < l < p \text{ and/or } q$, then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">于是，当 1 &lt; l &lt; p 及／或 q 时：</span></details>

$$
\begin{aligned}
\hat{X}_i(l) &= \phi_1 \hat{X}_i(l-1) + \phi_2 \hat{X}_i(l-2) + \cdots + \phi_{l-1} \hat{X}_i(1) \\
&\quad + \phi_l X_i + \phi_{l+1} X_{i-1} + \cdots + \phi_p X_{i+l-p} \\
&\quad + \theta_l a_i + \theta_{l+1} a_{i-1} + \cdots + \theta_q a_{i+l-q} \tag{5.6*}
\end{aligned}
$$

> [!example]- 手写笔记 PDF 第 3 页原图
> ![[Chapter 5/附件/ch5-handwritten-p03.png]]

---

## PDF p.4

**Updating ARIMA Forecasts (④)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">更新 ARIMA 预测（第 4 页）。</span></details>

**Table 5.1** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">表 5.1（注：原手写中有从 X̂_N(2) 指向 X̂_{N+1}(1) 及从提前 3 期指向 X̂_{N+1}(2) 的左下斜箭头；右下角手写形似 X̂_{N+1}(1)，实应为 X̂_{N+1}(L)）。</span></details>

| $i$ | $X_i$ | $a_i$ | Lead $l$: $1$ | $2$ | $\cdots$ | $L-1$ | $L$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| $N$ | $X_N$ | $a_N$ | $\hat{X}_N(1)$ | $\hat{X}_N(2)$ | | $\hat{X}_N(L-1)$ | $\hat{X}_N(L)$ |
| $N+1$ | $X_{N+1}$ | $a_{N+1}$ | $\hat{X}_{N+1}(1)$ | $\hat{X}_{N+1}(2)$ | | $\hat{X}_{N+1}(L-1)$ | $\hat{X}_{N+1}(1)$ |

When $X_{N+1}$ is available, we obtain (use $(5.2)$) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">当新观测值 X_{N+1} 可得时，由式 (5.2) 得：</span></details>

$$
a_{N+1} = X_{N+1} - \hat{X}_N(1) = X_{N+1} - \hat{X}_{N+1} \tag{5.7}
$$

$$
\hat{X}_{N+1}(l) = \hat{X}_N(l+1) + \psi_l a_{N+1} \tag{5.8}
$$

This follows using $(5.1)$, then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这可由式 (5.1) 推出，即：</span></details>

$$
\hat{X}_{N+1}(l) = \psi_l a_{N+1} + \psi_{l+1} a_N + \psi_{l+2} a_{N-1} + \cdots
$$

and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">以及：</span></details>

$$
\hat{X}_N(l+1) = \psi_{l+1} a_N + \psi_{l+2} a_{N-1} + \cdots
$$

Which on subtraction gives $(5.8)$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">两式相减即得式 (5.8)：</span></details>

$$
\hat{X}_{N+1}(l) - \hat{X}_N(l+1) = \psi_l a_{N+1} \implies \hat{X}_{N+1}(l) = \hat{X}_N(l+1) + \psi_l a_{N+1}
$$

$$
\begin{aligned}
l = 1: \qquad &\hat{X}_{N+1}(1) = \hat{X}_N(2) + \psi_1 a_{N+1} \\
l = 2: \qquad &\hat{X}_{N+1}(2) = \hat{X}_N(3) + \psi_2 a_{N+1} \\
&\vdots
\end{aligned}
$$

> [!example]- 手写笔记 PDF 第 4 页原图
> ![[Chapter 5/附件/ch5-handwritten-p04.png]]

---

## PDF p.5

**Ex. 1 & Ex. 2 (Ch. 5 p. 5, ⑤)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例 1 与例 2（对应讲义第 5 页，第 5 页手写笔记）：AR(2) 预测与 95% 预测区间。</span></details>

**Ex. 1**

$$
\begin{aligned}
X_t - \mu &= \phi_1(X_{t-1} - \mu) + \phi_2(X_{t-2} - \mu) + a_t, \quad a_t \text{ white noise},\; a_t \sim N(0, \sigma^2) \\
X_t &= \mu(1 - \phi_1 - \phi_2) + \phi_1 X_{t-1} + \phi_2 X_{t-2} + a_t \\
&= \theta_0 + \phi_1 X_{t-1} + \phi_2 X_{t-2} + a_t
\end{aligned}
$$

From Ch. 4 p. 16: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">来自第 4 章第 16 页的参数估计值：</span></details>

- $\hat{\phi}_1 = 1.548 \quad (\text{Coefficient of AR } 1)$, $\quad \hat{\sigma}_a^2 = 0.1318$
- $\hat{\phi}_2 = -0.6450 \quad (\text{Coefficient of AR } 2)$
- $\mu = 5.0819 \quad (\text{mean})$
- $\theta_0 = \mu(1 - \hat{\phi}_1 - \hat{\phi}_2) = 5.0819(1 - 1.548 + 0.645) = 0.4929443 \simeq 0.493$

At $t = 121$, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">在 t = 121 处（含红笔补充的 X̂_{121}(1) = X̂_{122} 与 X̂_{121}(2) = X̂_{123} 等价写法）：</span></details>

$$
\begin{aligned}
\hat{X}_t(1) &= \hat{X}_{121}(1) = \hat{X}_{122} = \hat{\theta}_0 + \hat{\phi}_1 X_t + \hat{\phi}_2 X_{t-1} = \hat{\theta}_0 + \hat{\phi}_1 X_{121} + \hat{\phi}_2 X_{120} \\
&= 0.493 + 1.548(6.20) - 0.645(6.63) = 5.81425 \simeq 5.81
\end{aligned}
$$

$$
\begin{aligned}
\hat{X}_t(2) &= \hat{X}_{121}(2) = \hat{X}_{123} = \hat{\theta}_0 + \hat{\phi}_1 \hat{X}_t(1) + \hat{\phi}_2 X_t = \hat{\theta}_0 + \hat{\phi}_1 \hat{X}_{122} + \hat{\phi}_2 X_{121} \\
&= 0.493 + 1.548(5.81) - 0.645(6.20) = 5.48788 \simeq 5.488
\end{aligned}
$$

**Ex. 2**

$$
\begin{aligned}
\hat{\psi}_1 &= \hat{\phi}_1 = 1.548 \\
\hat{\psi}_2 &= \hat{\phi}_1 \hat{\psi}_1 + \hat{\phi}_2 = 1.548^2 - 0.645 = 1.751 \\
\hat{\psi}_3 &= \hat{\phi}_1 \hat{\psi}_2 + \hat{\phi}_2 \hat{\psi}_1 = 1.548(1.751) + (-0.645)(1.548) = 1.7048 \simeq 1.71
\end{aligned}
$$

*(注：原手写此处为 `1.7048 ≃ 1.71`，按精确乘法 `1.548 × 1.751 − 0.645 × 1.548 = 1.712088`，照录原笔记。)*

At $t = 121$, a $95\%$ prediction limit for <details class="translation-details"><summary>中文译文</summary><span class="translation-body">在 t = 121 处，95% 预测区间为（第 3 步预测公式为红笔补充，方框留空代表点预测 X̂_t(3)）：</span></details>

- $\hat{X}_t(1): \quad 5.81 \pm 1.96\sqrt{0.1318} = (5.0984,\; 6.5216)$
- $\hat{X}_t(2): \quad 5.488 \pm 1.96\sqrt{0.1318}\sqrt{(1 + 1.548^2)} = (4.1767,\; 6.7993)$
- *(红笔补充)* $\hat{X}_t(3): \quad \square \pm 1.96\sqrt{0.1318}\sqrt{1 + \hat{\psi}_1^2 + \hat{\psi}_2^2}$

> [!example]- 手写笔记 PDF 第 5 页原图
> ![[Chapter 5/附件/ch5-handwritten-p05.png]]

---

## PDF p.6

**Ex. 3 $\text{ARMA}(1, 1)$ & Ex. 4 $\text{ARIMA}(1, 1, 0)$ (⑥)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例 3 ARMA(1, 1) 与例 4 ARIMA(1, 1, 0)（第 6 页）。</span></details>

**Ex. 3 $\text{ARMA}(1, 1)$**

$$
\begin{aligned}
(1 - \phi B) X_t &= (1 - \theta B) a_t \\
X_t - \phi X_{t-1} &= a_t - \theta a_{t-1} \\
X_t &= \phi X_{t-1} + a_t - \theta a_{t-1} \\
X_{t+l} &= \phi X_{t+l-1} + a_{t+l} - \theta a_{t+l-1}
\end{aligned}
$$

Forecasts are <details class="translation-details"><summary>中文译文</summary><span class="translation-body">预测值为（注：原手写等号右端省略了 X_t(1)、X_t(2)、X_t(l−1) 上的帽子符号，照录）：</span></details>

$$
\begin{aligned}
\hat{X}_t(1) &= \phi X_t - \theta a_t && (l = 1) \\
\hat{X}_t(2) &= \phi X_t(1) && (l = 2) \\
\hat{X}_t(3) &= \phi X_t(2) && (l = 3) \\
\therefore \quad \hat{X}_t(l) &= \phi X_t(l-1) && (l \ge 2)
\end{aligned}
$$

**Ex. 4 $\text{ARIMA}(1, 1, 0) \Rightarrow \text{ARI}(1, 1, 0)$**

$$
\begin{aligned}
(1 - 0.8B)(1 - B) X_{t+l} &= a_{t+l} \\
\Rightarrow (1 - 1.8B + 0.8B) X_{t+l} &= a_{t+l} \\
\Rightarrow X_{t+l} &= 1.8 X_{t+l-1} - 0.8 X_{t+l-2} + a_{t+l} \\
X_t(l) &= 1.8 X_t(l-1) - 0.8 X_t(l-2) + a_{t+l}
\end{aligned}
$$

*(注：第 2 行手写漏写 $0.8B^2$ 的上标 $2$，且下方 $l=2$ 行漏写 $X_t(1)$ 上的帽子符号，照录。)*

$$
\begin{aligned}
l = 1: \qquad &\hat{X}_t(1) = 1.8 X_t - 0.8 X_{t-1} \\
l = 2: \qquad &\hat{X}_t(2) = 1.8 X_t(1) - 0.8 X_t \\
\therefore \qquad &\hat{X}_t(l) = 1.8 \hat{X}_t(l-1) - 0.8 \hat{X}_t(l-2), \quad l = 3, 4, \dots
\end{aligned}
$$

> [!example]- 手写笔记 PDF 第 6 页原图
> ![[Chapter 5/附件/ch5-handwritten-p06.png]]

---

## PDF p.7

**Ex. 5 $\text{IMA}(0, 1, 1)$ & Ex. 6 $\text{IMA}(0, 1, 1)$ with constant (⑦)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例 5 IMA(0, 1, 1) 与例 6 带常数项的 IMA(0, 1, 1)（第 7 页）。</span></details>

**Ex. 5 $\text{IMA}(0, 1, 1)$**

$$
\begin{aligned}
X_t - X_{t-1} &= a_t + \theta a_{t-1} \\
X_t &= X_{t-1} + a_t + \theta a_{t-1} \\
X_{t+l} &= X_{t+l-1} + a_{t+l} + \theta a_{t+l-1} \\
X_t(l) &= X_t(l-1) + a_{t+l} + \theta a_{t+l-1}
\end{aligned}
$$

$$
\begin{aligned}
l = 1: \qquad &\hat{X}_t(1) = X_t + 0 + \theta a_t = X_t + \theta a_t \\
l = 2: \qquad &\hat{X}_t(2) = \hat{X}_t(1) \\
l = 3: \qquad &\hat{X}_t(3) = \hat{X}_t(2) \\
\therefore \qquad &\hat{X}_t(l) = \hat{X}_t(l-1) \qquad \text{for } l > 1
\end{aligned}
$$

**Ex. 6 $\text{IMA}(0, 1, 1)$ with constant**

$$
\begin{aligned}
X_{t+l} - \mu &= X_{t+l-1} + a_{t+l} + \theta a_{t+l-1} \\
X_{t+l} &= \mu + X_{t+l-1} + a_{t+l} + \theta a_{t+l-1} \\
X_t(l) &= \mu + X_t(l-1) + a_{t+l} + \theta a_{t+l-1}
\end{aligned}
$$

$$
\begin{aligned}
l = 1: \qquad &\hat{X}_t(1) = \mu + X_t + \theta a_t \\
l = 2: \qquad &\hat{X}_t(2) = \mu + \hat{X}_t(1) \\
l = 3: \qquad &\hat{X}_t(3) = \mu + \hat{X}_t(2) = 2\mu + \hat{X}_t(1) \\
\therefore \qquad &\hat{X}_t(l) = \mu + \hat{X}_t(l-1) = (l - 1)\mu + \hat{X}_t(1) \qquad \text{for } l > 1
\end{aligned}
$$

> [!example]- 手写笔记 PDF 第 7 页原图
> ![[Chapter 5/附件/ch5-handwritten-p07.png]]

---

## PDF p.8

**Ex. 7 Seasonal Time Series Model $(1, 0, 0)(0, 1, 1)_{12}$ & Ex. 8 (⑧)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例 7 季节时间序列模型 (1,0,0)(0,1,1)_12 与例 8 AR(2) 数值预测（第 8 页）。</span></details>

**Ex. 7 Seasonal time series model $(1, 0, 0)(0, 1, 1)_{12}$**

$$
\begin{aligned}
(1 - \alpha B)(1 - B^{12}) X_t &= (1 - \theta B^{12}) a_t \\
\Rightarrow (1 - \alpha B - B^{12} + \alpha B^{13}) X_t &= (1 - \theta B^{12}) a_t \\
X_t - \alpha X_{t-1} - X_{t-12} + \alpha X_{t-13} &= a_t - \theta a_{t-12} \\
X_t &= \alpha X_{t-1} + X_{t-12} - \alpha X_{t-13} - \theta a_{t-12} + a_t \\
X_{t+l} &= \alpha X_{t+l-1} + X_{t+l-12} - \alpha X_{t+l-13} - \theta a_{t+l-12} + a_{t+l} \\
X_t(l) &= \alpha X_t(l-1) + X_t(l-12) - \alpha X_t(l-13) - \theta a_{t+l-12} + a_{t+l}
\end{aligned}
$$

$l = 1$: *(注：原手写 $X_t(1)$ 与 $X_t(2)$ 行分别省略了 $+a_{t+1}$ 与 $+a_{t+2}$，照录。)*

$$
\begin{aligned}
X_t(1) &= \alpha X_t + X_t(-11) - \alpha X_t(-12) - \theta a_{t-11} \\
\underset{t}{E}(X_{t+1}) &= \hat{X}_t(1) = \alpha X_t + X_{t-11} - \alpha X_{t-12} - \theta a_{t-11}
\end{aligned}
$$

$l = 2$:

$$
\begin{aligned}
X_t(2) &= \alpha X_t(1) + X_t(-10) - \alpha X_t(-11) - \theta a_{t-10} \\
\underset{t}{E}(X_{t+2}) &= \alpha \hat{X}_t(1) + X_{t-10} - \alpha X_{t-11} - \theta a_{t-10} \\
&= \alpha\left[\alpha X_t + X_{t-11} - \alpha X_{t-12} - \theta a_{t-11}\right] + X_{t-10} - \alpha X_{t-11} - \theta a_{t-10} \\
&= \alpha^2(X_t - X_{t-12}) + X_{t-10} - \theta \alpha a_{t-11} - \theta a_{t-10}
\end{aligned}
$$

**Ex. 8**

$$
\begin{aligned}
X_t &= 20.62 + 0.777 X_{t-1} - 0.492 X_{t-2} + a_t \\
X_{t+1} = X_t(1) &= 20.62 + 0.777 X_t - 0.492 X_{t-1} + a_{t+1} \\
\hat{X}_t(1) &= 20.62 + 0.777 X_t - 0.492 X_{t-1} \\
&= 20.62 + 0.777(32.44) - 0.492(26.74) \\
&= 32.6698
\end{aligned}
$$

> [!example]- 手写笔记 PDF 第 8 页原图
> ![[Chapter 5/附件/ch5-handwritten-p08.png]]
